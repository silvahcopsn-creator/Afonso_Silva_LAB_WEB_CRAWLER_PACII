from crawler import iniciar_crawl


def main():
    url_inicial = "https://example.com"
    limite_paginas = 3

    resultado = iniciar_crawl(url_inicial, limite_paginas)

    print("\nResumo:")
    for pagina in resultado:
        print(f"Título: {pagina['titulo']}")
        print(f"URL: {pagina['pagina']}")
        print("-" * 40)


if __name__ == "__main__":
    main()