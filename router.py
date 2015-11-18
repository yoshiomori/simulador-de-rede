from settings import tamanho_buffer_router
from threading import Condition


class Interface(object):
    def __init__(self, buffer_entrada):
        self.buffer_entrada = buffer_entrada
        self.buffer_saída = []
        self.ip = None

    def set_ip(self, ip):
        self.ip = ip

    def tem_saída(self):
        return len(self.buffer_saída) > 0

    def append_entrada(self, datagrama):
        if len(self.buffer_entrada) >= tamanho_buffer_router:
            return  # Não insere se o buffer alcançar o limite
        self.buffer_entrada.append(datagrama)

    def pop_entrada(self):
        return self.buffer_entrada.pop(0)

    def append_saída(self, datagrama):
        self.buffer_saída.append(datagrama)

    def pop_saída(self):
        return self.buffer_saída.pop(0)


conjunto_interface = {}
conjunto_tabelas = {}


def set_ip(índice, resto):
    porta_ip = resto.split(' ')
    while '' in porta_ip:
        porta_ip.remove('')
    for porta, ip in [(int(porta), bytearray([int(v) for v in ip.split('.')])) for porta, ip in
                      zip(porta_ip[::2], porta_ip[1::2])]:
        if len(ip) != 4:
            raise RuntimeError(resto, 'não é válido')
        conjunto_interface[índice][porta].set_ip(ip)


# Cada router tem um índice associado a ele
# O índice de cada router é usado para acessar o seu conjunto de interfaces
# Função que inicializa um router
def faz(índice, número_interfaces):
    tabela = {}  # Associo o ip à uma interface
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
        c.acquire()
        c.wait_for(tem_entrada)
        datagrama = buffer_entrada.pop(0)
        if datagrama[32:64] in tabela:
            tabela[datagrama[32:64]].push(datagrama)
