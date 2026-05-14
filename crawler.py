import json
import time
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from robots_checker import carregar_robots, permitido


def extrair_links(html, pagina_atual):
    """
    Retorna todos os links encontrados numa página.
    """
    soup = BeautifulSoup(html, "html.parser")
    encontrados = []

    for link in soup.find_all("a", href=True):
        url_completa = urljoin(pagina_atual, link["href"])
        encontrados.append(url_completa)

    return encontrados


def obter_titulo(html):
    """
    Extrai o título da página.
    """
    soup = BeautifulSoup(html, "html.parser")

    if soup.title:
        return soup.title.text.strip()

    return "Sem título"


def guardar_json(dados, ficheiro="resultados.json"):
    """
    Guarda os resultados em JSON.
    """
    with open(ficheiro, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def iniciar_crawl(url_base, limite):
    """
    Executa o crawler.
    """
    visitadas = set()
    fila = [url_base]
    paginas = []

    parser_robots = carregar_robots(url_base)

    while fila and len(visitadas) < limite:

        url = fila.pop(0)

        if url in visitadas:
            continue

        if not permitido(url, parser_robots):
            print(f"Acesso negado pelo robots.txt: {url}")
            continue

        print(f"A analisar: {url}")

        try:
            resposta = requests.get(
                url,
                headers={"User-Agent": "MeuCrawlerAcademico/1.0"},
                timeout=8
            )

            resposta.raise_for_status()

            titulo = obter_titulo(resposta.text)
            links = extrair_links(resposta.text, url)

            paginas.append({
                "pagina": url,
                "titulo": titulo,
                "links": links[:10]
            })

            for l in links:
                if l not in visitadas and l not in fila:
                    fila.append(l)

            visitadas.add(url)

            time.sleep(1)

        except requests.RequestException as erro:
            print(f"Erro na página {url}: {erro}")

    guardar_json(paginas)

    print(f"\nProcesso terminado: {len(paginas)} páginas guardadas.")
    return paginas


if __name__ == "__main__":
    url_inicio = "https://example.com"
    numero_maximo = 3

    iniciar_crawl(url_inicio, numero_maximo)