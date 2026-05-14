import json
import time
import requests
import matplotlib.pyplot as plt
import networkx as nx
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from robots_checker import carregar_robots, permitido


def crawl_avancado(url_base, limite, mesmo_dominio=True):
    fila = [url_base]
    visitadas = set()
    resultados = []
    dominio = urlparse(url_base).netloc
    grafo = nx.DiGraph()
    robots = carregar_robots(url_base)

    while fila and len(visitadas) < limite:
        url = fila.pop(0)

        if url in visitadas or not permitido(url, robots):
            continue

        print(f"A visitar: {url}")

        try:
            resposta = requests.get(
                url,
                headers={"User-Agent": "MeuCrawler/2.0"},
                timeout=10
            )

            soup = BeautifulSoup(resposta.text, "html.parser")
            titulo = soup.title.text.strip() if soup.title else "Sem título"

            links = []
            for a in soup.find_all("a", href=True):
                link = urljoin(url, a["href"])

                if mesmo_dominio and urlparse(link).netloc != dominio:
                    continue

                links.append(link)

                if link not in fila and link not in visitadas:
                    fila.append(link)

            headers = {
                f"h{i}": [x.get_text(strip=True) for x in soup.find_all(f"h{i}")]
                for i in range(1, 4)
            }

            paragrafos = [
                p.get_text(strip=True)
                for p in soup.find_all("p")
            ][:5]

            resultados.append({
                "pagina": url,
                "titulo": titulo,
                "links": links[:10],
                "headers": headers,
                "paragrafos": paragrafos
            })

            grafo.add_node(url, label=titulo[:25])

            for l in links[:10]:
                grafo.add_edge(url, l)

            visitadas.add(url)
            time.sleep(1)

        except Exception as erro:
            print(f"Erro: {erro}")

    with open("resultados_bonus.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(grafo)
    nx.draw(grafo, pos, with_labels=False, node_size=500, arrows=True)
    nx.draw_networkx_labels(
        grafo,
        pos,
        nx.get_node_attributes(grafo, "label"),
        font_size=7
    )

    plt.title("Grafo de Navegação")
    plt.savefig("grafo_navegacao.png")
    plt.show()

    return resultados