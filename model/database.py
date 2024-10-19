import sqlite3
from datetime import datetime, date
from model.produto import Produto
from colorama import Fore, Style, init
from enviar_email import enviar_email


# Inicializa o colorama
init(autoreset=True)


class DatabaseManager:
    def __init__(self, db_name="produtos.db"):
        self.connection = sqlite3.connect(db_name)
        self.create_tables()

    def create_tables(self):
        with self.connection:
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS produtos (
                    id INTEGER PRIMARY KEY,
                    titulo TEXT NOT NULL UNIQUE,
                    preco_alvo REAL
                )
            """)
            self.connection.execute("""
                CREATE TABLE IF NOT EXISTS precos (
                    id INTEGER PRIMARY KEY,
                    produto_id INTEGER,
                    preco REAL NOT NULL,
                    data_hora TEXT NOT NULL,
                    FOREIGN KEY (produto_id) REFERENCES produtos (id)
                )
            """)
    def novo_produto(self, produto: Produto):
        try:
            with self.connection:
                cursor = self.connection.cursor()
                cursor.execute("INSERT INTO produtos (titulo, preco, preco_alvo) VALUES (?, ?, ?)", (produto.titulo, produto.preco, produto.preco_alvo))
                produto_id = cursor.lastrowid
                self.salvar_preco(produto_id, produto.preco)
        except Exception as e:
            print(f"Erro ao inserir produto no banco de dados: {e}")
        
    def salvar_produto(self, produto: Produto):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("SELECT id FROM produtos WHERE titulo = ?", (produto.titulo,))
            produto_existente = cursor.fetchone()

            if produto_existente:
                produto_id = produto_existente[0]
            else:
                preco_alvo = float(input(f"Digite o preço alvo para o produto '{produto.titulo}'. Valor atual: R$: {produto.preco} (ex: 99.99): ").replace(',', '.'))
                cursor.execute("INSERT INTO produtos (titulo, preco_alvo) VALUES (?, ?)", (produto.titulo, preco_alvo))
                produto_id = cursor.lastrowid

            self.salvar_preco(produto_id, produto.preco)

    def salvar_preco(self, produto_id, preco):
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with self.connection:
            self.connection.execute(
                "INSERT INTO precos (produto_id, preco, data_hora) VALUES (?, ?, ?)",
                (produto_id, preco, data_hora)
            )

    def definir_preco_alvo(self, titulo_produto, preco_alvo):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("UPDATE produtos SET preco_alvo = ? WHERE titulo = ?", (preco_alvo, titulo_produto))
            self.connection.commit()

    def buscar_menor_preco_dia(self, produtos):
        print('\n*** OS MENORES PREÇOES DO DIA ***\n')
        for produto in produtos:
            if not isinstance(produto, Produto):
                raise ValueError("Esperado um objeto da classe Produto.")

            titulo_produto = produto.titulo

            query = """
            SELECT 
                pr.data_hora, p.titulo, pr.preco
            FROM 
                produtos p
            INNER JOIN precos pr 
                ON p.id = pr.produto_id
            WHERE 
                p.titulo = ?
                AND DATE(pr.data_hora) = DATE('now', 'localtime')
            ORDER BY 
                pr.preco ASC
            LIMIT 1
            """

            with self.connection:
                cursor = self.connection.cursor()
                try:
                    cursor.execute(query, (titulo_produto,))
                    resultado = cursor.fetchone()
                except sqlite3.Error as e:
                    print(f"Erro ao executar a consulta: {e}")
                    return None

            if resultado:
                print(Fore.BLUE + f'{resultado[1]}' + Style.RESET_ALL)
                print(f"Preço: {resultado[2]}\nData e Hora: {resultado[0]}\n")
            else:
                print(f"\nNenhum preço encontrado para o produto '{titulo_produto}' hoje.\n")

    def verifica_preco_alvo(self, titulo_produto):
        with self.connection:
            cursor = self.connection.cursor()
            cursor.execute("""
            SELECT 
                data_hora, titulo, preco, preco_alvo
            FROM 
                produtos INNER JOIN precos 
                    ON produtos.id = precos.produto_id
            WHERE 
                produtos.titulo = ?
                AND DATE(precos.data_hora) = DATE('now', 'localtime')
            ORDER BY 
                precos.data_hora DESC
            LIMIT 1;
            """, (titulo_produto,))
            resultado = cursor.fetchone()

        if resultado:
            data_hora, titulo, preco_atual, preco_alvo = resultado
            preco_atual = float(preco_atual)
            preco_alvo = float(preco_alvo)
            # print(Fore.GREEN + 'Email enviado' + Style.RESET_ALL)
            if preco_alvo is not None and preco_atual <= preco_alvo:
                print(Fore.GREEN + f"O preço alvo foi atingido para o produto '{titulo_produto}'!!! Preço atual: R${preco_atual}. Preço alvo: R${preco_alvo}." + Style.RESET_ALL)
                produto = Produto(titulo_produto, preco_atual)
                produto.set_preco_alvo(preco_alvo)
                return produto
            else:
                print(Fore.LIGHTRED_EX + f"O produto '{titulo_produto}' ainda acima do preço alvo. Preço atual: R${preco_atual}. Preço alvo: R${preco_alvo}." + Style.RESET_ALL)
                return None
        else:
            print(f"Nenhum preço encontrado para o produto '{titulo_produto}'.")
            return None

    def executa_verificacao_de_preco_alvo(self, produtos):
        print('\n*** VERIFICA SE O PREÇO ALVO FOI ATINGIDO ***\n')
        for produto in produtos:
            preco_alvo_atingido = self.verifica_preco_alvo(produto.titulo)
            if preco_alvo_atingido:
                enviar_email(preco_alvo_atingido)

    def fechar(self):
        self.connection.close()
