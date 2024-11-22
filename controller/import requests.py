import requests
from bs4 import BeautifulSoup

# Função para buscar o preço do produto na Amazon
def get_amazon_price(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        price = soup.find('span', {'id': 'priceblock_ourprice'})
        return price.get_text().strip() if price else "Preço não encontrado"

# Função para buscar o preço do produto no KaBuM!
def get_kabum_price(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        price = soup.find('span', {'class': 'price'})
        return price.get_text().strip() if price else "Preço não encontrado"

# Exemplo de URLs
amazon_url = "https://www.amazon.com.br/dp/B08V4DW1JZ"
kabum_url = "https://www.kabum.com.br/produto/107378/ssd-kingston-a2000-500gb-m2"

# Exibe os preços
print(f"Preço da Amazon: {get_amazon_price(amazon_url)}")
print(f"Preço do KaBuM!: {get_kabum_price(kabum_url)}")
