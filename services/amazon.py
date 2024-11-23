from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from utils.links import links_amazon
from models.produto import Produto
from colorama import Fore, Style, init


# Inicializa o colorama
init(autoreset=True)


class Amazon:
    def __init__(self, driver):
        self.driver = driver
        self.produtos = []

    # Iterando sobre a lista de links e imprimindo as informações dos produtos
    def scrape_products(self):
        for url in links_amazon:
            product_info = self.fetch_product_info(url)
            if product_info:
                self.produtos.append(product_info)
                print(Fore.YELLOW + f'{product_info}' + Style.RESET_ALL)
            time.sleep(2)  # Pausa para evitar problemas de carregamento

        self.driver.quit()

    def fetch_product_info(self, url):
        self.driver.get(url)

        # Verifica se a página de CAPTCHA está presente e faz refresh até que desapareça
        while True:
            try:
                captcha_present = self.driver.find_element(By.XPATH, '//h4[contains(text(), "Digite os caracteres que você vê abaixo")]')
                if captcha_present:
                    print(Fore.GREEN + "CAPTCHA detected, refreshing the page..." + Style.RESET_ALL)
                    self.driver.refresh()
                    time.sleep(2)  # Pausa para evitar sobrecarga do servidor
            except:
                # Se o CAPTCHA não estiver presente, prossegue com a extração das informações do produto
                break

        try:
            title = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="productTitle"]'))
            ).text
        except Exception as e:
            print(Fore.RED + f"Error fetching title from URL {url}: {e}" + Style.RESET_ALL)
            return None

        try:
            price_whole = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'a-price-whole'))
            ).text
            price_fraction = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(
                    (By.CLASS_NAME, 'a-price-fraction'))
            ).text
            price_str = price_whole.replace('.', '') + '.' + price_fraction
            price = float(price_str)
        except Exception as e:
            print(Fore.RED + f"Error fetching price from URL {url}: {e}" + Style.RESET_ALL)
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
