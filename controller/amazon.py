import requests
from bs4 import BeautifulSoup
from controller.links import links_amazon
from model.produto import Produto
from colorama import Fore, Style, init


# Inicializa o colorama
init(autoreset=True)


class Amazon:
    def __init__(self):
        self.produtos = []

    def scrape_products(self):
        for url in links_amazon:
            product_info = self.fetch_product_info(url)
            if product_info:
                self.produtos.append(product_info)
                print(Fore.YELLOW + f'{product_info}' + Style.RESET_ALL)

    def fetch_product_info(self, url):
        # Faz uma requisição para pegar o conteúdo da página
        response = requests.get(url)

        if response.status_code != 200:
            print(Fore.RED + f"Erro ao acessar {url}: Código de status {response.status_code}" + Style.RESET_ALL)
            return None

        # Usa BeautifulSoup para analisar o HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        try:
            # Pega o título do produto
            title = soup.find('span', {'id': 'productTitle'}).get_text(strip=True)
        except AttributeError:
            print(Fore.RED + f"Erro ao encontrar título no produto {url}" + Style.RESET_ALL)
            return None

        try:
            # Pega o preço do produto
            price_str = soup.find('span', {'id': 'priceblock_ourprice'}).get_text(strip=True)
        except AttributeError:
            print(Fore.RED + f"Erro ao encontrar preço no produto {url}" + Style.RESET_ALL)
            return None

        try:
            # Limpeza e conversão do preço
            price_str = price_str.replace('R$', '').replace('.', '').replace(',', '.').strip()
            price = float(price_str)
        except ValueError:
            print(Fore.RED + f"Erro ao converter preço do produto {url}" + Style.RESET_ALL)
            return None

        return Produto(titulo=title, preco=price)

    # Exibe a lista de produtos analisados
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
