from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options


class WebDriverConfig:
    @staticmethod
    def config_chromedriver():
        # Configuração do driver
        service = Service(executable_path="chromedriver.exe")
        options = Options()
        options.add_argument("--headless")  # Executa o Chrome em modo headless
        options.add_argument("--window-size=750,900")  # Define o tamanho da janela
        driver = webdriver.Chrome(service=service, options=options)
        return driver
