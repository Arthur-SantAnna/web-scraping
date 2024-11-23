from services.amazon import Amazon
from services.kabum import Kabum
from configs.web_driver_config import WebDriverConfig
from services.database import DatabaseManager


def analise_de_precos(produtos):
    # Analisa os precos e seus comportamentos
    db_manager = DatabaseManager()

    # Busca o menor preço do dia
    db_manager.buscar_menor_preco_dia(produtos)

    # Verifica se algum produto analisado atingiu o preço alvo
    db_manager.executa_verificacao_de_preco_alvo(produtos)

    db_manager.fechar()


def main():
    # Inicializa uma lista vazia de produtos
    produtos = []

    # Configura o WebDriver
    driver = WebDriverConfig.config_chromedriver()
    try:
        # Cria uma instância da classe Amazon
        amazon_scraper = Amazon(driver)
        # Inicia o scraping de produtos da Amazon
        amazon_scraper.scrape_products()
        # Adiciona os produtos da Amazon à lista de produtos
        produtos += amazon_scraper.produtos_analisados() or []

        # Configura novamente o WebDriver para Kabum (opcional se necessário)
        driver = WebDriverConfig.config_chromedriver()

        # Cria uma instância da classe Kabum
        kabum_scraper = Kabum(driver)
        # Inicia o scraping de produtos na Kabum
        kabum_scraper.scrape_products()
        # Adiciona os produtos da Kabum à lista de produtos
        produtos += kabum_scraper.produtos_analisados() or []

    finally:
        # Fecha o WebDriver
        driver.quit()

    # Salva os produtos no banco de dados
    if produtos:
        db_manager = DatabaseManager()
        for produto in produtos:
            db_manager.salvar_produto(produto)
        db_manager.fechar()

    analise_de_precos(produtos)