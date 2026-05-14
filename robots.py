from urllib.robotparser import RobotFileParser
from urllib.parse import urlparse


def carregar_robots(url):

    dominio = urlparse(url)
    robots_link = f"{dominio.scheme}://{dominio.netloc}/robots.txt"

    parser = RobotFileParser()
    parser.set_url(robots_link)

    try:
        parser.read()
        print(f"robots.txt encontrado: {robots_link}")
        return parser
    except Exception as erro:
        print(f"Erro ao carregar robots.txt: {erro}")
        return None


def permitido(url, parser):
    
    agente = "MeuCrawlerAcademico"

    if parser is None:
        return True

    return parser.can_fetch(agente, url)