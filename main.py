from crawler import crawl_avancado


def main():
    url_inicial = "https://quotes.toscrape.com"
    limite_paginas = 3

    resultado = crawl_avancado(url_inicial, limite_paginas)

    print("\nResumo:")
    for pagina in resultado:
        print(f"Título: {pagina['titulo']}")
        print(f"URL: {pagina['pagina']}")
        print("-" * 40)


if __name__ == "__main__":
    main()