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
        """Realiza a raspagem de produtos a partir dos links fornecidos."""
        for url in links_amazon:
            product_info = self._fetch_product_info(url)
            if product_info:
                self.produtos.append(product_info)
                self._log_success(product_info)

    def _fetch_product_info(self, url):
        """Busca informações do produto a partir de uma URL."""
        response = self._make_request(url)
        if not response:
            return None

        soup = BeautifulSoup(response.content, 'html.parser')
        title = self._extract_text(soup, 'span', {'id': 'productTitle'}, "título", url)
        price = self._extract_price(soup, 'span', {'id': 'priceblock_ourprice'}, url)

        if title and price is not None:
            return Produto(titulo=title, preco=price)
        return None

    def _make_request(self, url):
        """Faz a requisição HTTP para obter o conteúdo da página."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            return response
        except requests.RequestException as e:
            print(Fore.RED + f"Erro ao acessar {url}: {e}" + Style.RESET_ALL)
            return None

    def _extract_text(self, soup, tag, attrs, field_name, url):
        """Extrai texto de um elemento HTML, com tratamento de erros."""
        try:
            return soup.find(tag, attrs).get_text(strip=True)
        except AttributeError:
            print(Fore.RED + f"Erro ao encontrar {field_name} no produto {url}" + Style.RESET_ALL)
            return None

    def _extract_price(self, soup, tag, attrs, url):
        """Extrai e converte o preço do produto."""
        price_str = self._extract_text(soup, tag, attrs, "preço", url)
        if not price_str:
            return None

        try:
            price_str = price_str.replace('R$', '').replace('.', '').replace(',', '.').strip()
            return float(price_str)
        except ValueError:
            print(Fore.RED + f"Erro ao converter preço do produto {url}" + Style.RESET_ALL)
            return None

    def listar_produtos(self):
        """Exibe a lista de produtos analisados."""
        if not self.produtos:
            print(Fore.YELLOW + "Nenhum produto foi analisado ainda." + Style.RESET_ALL)
            return

        print("\nLista de produtos analisados:")
        for produto in self.produtos:
            print(Fore.BLUE + f"Name: {produto.titulo}\nR$: {produto.preco:.2f}\n" + Style.RESET_ALL)

    def produtos_analisados(self):
        """Retorna a lista de produtos analisados."""
        if not self.produtos:
            print(Fore.YELLOW + "A lista de produtos está vazia." + Style.RESET_ALL)
            return []
        return self.produtos

    def _log_success(self, produto):
        """Loga um produto analisado com sucesso."""
        print(Fore.YELLOW + f"Produto analisado: {produto}" + Style.RESET_ALL)
