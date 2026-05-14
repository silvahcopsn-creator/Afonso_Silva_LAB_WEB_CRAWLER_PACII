import json
import time
import requests
import matplotlib.pyplot as plt
import networkx as nx
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from robots import carregar_robots, permitido


def normalizar(url):
    parsed = urlparse(url)
    return f"{parsed.scheme}://{parsed.netloc}{parsed.path.rstrip('/')}"


def crawl_avancado(url_base, limite=10, mesmo_dominio=True):
    fila = [normalizar(url_base)]
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
            r = requests.get(url, headers={"User-Agent": "Crawler/1.0"}, timeout=10)
            soup = BeautifulSoup(r.text, "html.parser")

            titulo = soup.title.text.strip() if soup.title else "Sem título"

            links = set()

            for a in soup.find_all("a", href=True):
                link = normalizar(urljoin(url, a["href"]))

                if mesmo_dominio and urlparse(link).netloc != dominio:
                    continue

                links.add(link)

                if link not in visitadas and link not in fila:
                    fila.append(link)

            headers = {
                f"h{i}": list({h.get_text(strip=True) for h in soup.find_all(f"h{i}")})
                for i in range(1, 4)
            }

            paragrafos = [p.get_text(strip=True) for p in soup.find_all("p")][:5]

            resultados.append({
                "pagina": url,
                "titulo": titulo,
                "links": list(links)[:10],
                "headers": headers,
                "paragrafos": paragrafos
            })

            grafo.add_node(url, label=titulo[:25])

            for l in list(links)[:10]:
                grafo.add_edge(url, l)

            visitadas.add(url)
            time.sleep(1)

        except Exception as e:
            print(f"Erro: {e}")

    with open("resultados_bonus.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=4, ensure_ascii=False)

    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(grafo)
    nx.draw(grafo, pos, with_labels=False, node_size=500, arrows=True)
    nx.draw_networkx_labels(grafo, pos, nx.get_node_attributes(grafo, "label"), font_size=7)

    plt.title("Grafo de Navegação")
    plt.savefig("grafo_navegacao.png")
    plt.show()

    return resultados