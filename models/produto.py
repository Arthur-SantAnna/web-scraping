class Produto:
    def __init__(self, titulo, preco):
        self.titulo = titulo
        self.preco = preco
        self.preco_alvo = None

    def set_preco_alvo(self, preco_alvo):
        self.preco_alvo = preco_alvo

    def __str__(self):
        return f"Produto(titulo='{self.titulo}', preco='{self.preco}')"
