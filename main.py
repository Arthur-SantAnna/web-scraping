from scraping.amazon import Amazon
from scraping.kabum import Kabum
from model.database import DatabaseManager


def realizar_scraping():
    """
    Realiza o scraping de produtos de todos os sites disponíveis.
    """
    scrapers = [Amazon(), Kabum()]
    produtos = []

    for scraper in scrapers:
        scraper.scrape_products()
        produtos += scraper.produtos_analisados() or []

    return produtos


def salvar_produtos_no_banco(produtos):
    """
    Salva os produtos extraídos no banco de dados.
    """
    if not produtos:
        print("Nenhum produto para salvar no banco de dados.")
        return

    db_manager = DatabaseManager()
    for produto in produtos:
        db_manager.salvar_produto(produto)
    db_manager.fechar()


def analise_de_precos(produtos):
    """
    Analisa os preços e verifica comportamentos no banco de dados.
    """
    if not produtos:
        print("Nenhum produto disponível para análise.")
        return

    db_manager = DatabaseManager()
    db_manager.buscar_menor_preco_dia(produtos)
    db_manager.executa_verificacao_de_preco_alvo(produtos)
    db_manager.fechar()


def main():
    """
    Função principal do programa.
    """
    # Realiza o scraping de produtos
    produtos = realizar_scraping()

    # Salva os produtos no banco de dados
    salvar_produtos_no_banco(produtos)

    # Realiza a análise de preços
    analise_de_precos(produtos)


if __name__ == "__main__":
    main()