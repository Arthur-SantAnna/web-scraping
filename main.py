from controller.amazon import Amazon
from controller.kabum import Kabum
from model.database import DatabaseManager


def analise_de_precos(produtos):
    # Analisa os preços e seus comportamentos
    db_manager = DatabaseManager()

    # Busca o menor preço do dia
    db_manager.buscar_menor_preco_dia(produtos)

    # Verifica se algum produto analisado atingiu o preço alvo
    db_manager.executa_verificacao_de_preco_alvo(produtos)

    db_manager.fechar()


def main():
    # Inicializa uma lista vazia de produtos
    produtos = []

    # Cria uma instância da classe Amazon
    amazon_scraper = Amazon()
    # Inicia o scraping de produtos da Amazon
    amazon_scraper.scrape_products()
    # Adiciona os produtos da Amazon à lista de produtos
    produtos += amazon_scraper.produtos_analisados() or []

    # Cria uma instância da classe Kabum
    kabum_scraper = Kabum()
    # Inicia o scraping de produtos na Kabum
    kabum_scraper.scrape_products()
    # Adiciona os produtos da Kabum à lista de produtos
    produtos += kabum_scraper.produtos_analisados() or []

    # Salva os produtos no banco de dados
    if produtos:
        db_manager = DatabaseManager()
        for produto in produtos:
            db_manager.salvar_produto(produto)
        db_manager.fechar()

    analise_de_precos(produtos)


if __name__ == '__main__':
    main()
