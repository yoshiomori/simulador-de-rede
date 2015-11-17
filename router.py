from settings import tamanho_buffer_router
from threading import Condition


class Interface(object):
    def __init__(self, buffer_entrada):
        self.buffer_entrada = buffer_entrada
        self.buffer_saída = []

    def append_entrada(self, datagrama):
        if len(self.buffer_entrada) >= tamanho_buffer_router:
            return  # Não insere se o buffer alcançar o limite
        self.buffer_entrada.append(datagrama)

    def tem_saída(self):
        return len(self.buffer_saída) > 0


conjunto_interface = {}
conjunto_tabelas = {}


# Cada router tem um índice associado a ele
# O índice de cada router é usado para acessar o seu conjunto de interfaces
# Função que inicializa um router
def router(índice, número_interfaces):
    tabela = {}
    buffer_entrada = []
    interfaces = [Interface(buffer_entrada) for _ in range(número_interfaces)]
    conjunto_tabelas[índice] = tabela
    conjunto_interface[índice] = interfaces
    for _ in range(número_interfaces):
        interfaces.append(Interface(buffer_entrada))

    def tem_entrada():
        return len(buffer_entrada) > 0

    c = Condition()
    while True:
        c.wait_for(tem_entrada)
        datagrama = buffer_entrada.pop(0)
        if datagrama[32:64] in tabela:
            tabela[datagrama[32:64]].push(datagrama)
