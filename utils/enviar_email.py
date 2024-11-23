import smtplib
import email.message
import json
from colorama import Fore, Style, init


# Inicializa o colorama
init(autoreset=True)


def busca_credenciais():
    with open('D:\\credenciais\\credenciais.json', 'r') as file:
        credenciais = json.load(file)
    return credenciais['email_credentials']


def enviar_email(produto):
    credenciais = busca_credenciais()

    corpo_email = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {{
                font-family: Arial, sans-serif;
                font-size: 16px;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
                border: 1px solid #ddd;
                border-radius: 5px;
                background-color: #f9f9f9;
            }}
            h1 {{
                color: #4CAF50;
            }}
            p {{
                line-height: 1.5;
            }}
            .highlight {{
                font-weight: bold;
                color: #333;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📉 O Preço Alvo Foi Atingido!</h1>
            <p>O produto <span class="highlight">{produto.titulo}</span> atingiu o preço alvo de <span class="highlight">R$ {produto.preco_alvo}</span>.</p>
            <p>Atualmente, ele está custando <span class="highlight">R$ {produto.preco}</span>.</p>
        </div>
    </body>
    </html>
    """

    msg = email.message.Message()
    msg['Subject'] = "Alerta de Preço - Web Scraping"
    msg['From'] = credenciais['From']
    msg['To'] = credenciais['To']
    password = credenciais['password']
    msg.add_header('Content-Type', 'text/html')
    msg.set_payload(corpo_email)

    s = smtplib.SMTP('smtp.gmail.com: 587')
    s.starttls()
    # Login Credentials for sending the mail
    s.login(msg['From'], password)
    s.sendmail(msg['From'], [msg['To']], msg.as_string().encode('utf-8'))
    print(Fore.GREEN + 'Email enviado' + Style.RESET_ALL)

