from selenium.common import TimeoutException, NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utils.links import links_kabum
from models.produto import Produto
from colorama import Fore, Style, init


# Inicializa o colorama
init(autoreset=True)


class Kabum:
    def __init__(self, driver):
        self.driver = driver
        self.produtos = []

    # Iterando sobre a lista de links e imprimindo as informações dos produtos
    def scrape_products(self):
        for url in links_kabum:
            product_info = self.fetch_product_info(url)
            if product_info:
                self.produtos.append(product_info)
                print(Fore.YELLOW + f'{product_info}' + Style.RESET_ALL)
            time.sleep(2)  # Pausa para evitar problemas de carregamento

        self.driver.quit()

    def fetch_product_info(self, url):
        self.driver.get(url)

        try:
            title = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="container-purchase"]/div[1]/div/h1'))
            ).text
        except Exception as e:
            print(Fore.RED + f"Error fetching title from URL {url}: {e}" + Style.RESET_ALL)
            return None

        price_str = None
        try:
            # Primeiro XPath para o preço
            price_str = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="blocoValores"]/div[2]/div[1]/div/h4'))
            ).text
        except (TimeoutException, NoSuchElementException):
            try:
                # Segundo XPath para o preço
                price_str = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="blocoValores"]/div[3]/div[1]/div/h4'))
                ).text
            except (TimeoutException, NoSuchElementException) as e:
                print(Fore.RED + f"Error fetching price from URL {url}: {e}" + Style.RESET_ALL)
                return None

        try:
            # Limpeza e conversão do preço
            price_str = price_str.replace('R$', '').replace('.', '').replace(',', '.').strip()
            price = float(price_str)
        except ValueError as e:
            print(Fore.RED + f"Error converting price from URL {url}: {e}" + Style.RESET_ALL)
            return None

        return Produto(titulo=title, preco=price)

    # Exibi a lista de produtos analisados
    def listar_produtos(self):
        print("\nLista de produtos analisados:")
        for produto in self.produtos:
            print(Fore.BLUE + f'Name: {produto.titulo}\nR$:{produto.preco}\n' + Style.RESET_ALL)

    # Retorna a lista de produtos analisados
    def produtos_analisados(self):
        if not self.produtos:
            print('A lista de produtos está vazia.')
            return False
        else:
            return self.produtos
