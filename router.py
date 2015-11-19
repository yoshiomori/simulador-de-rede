import sys

from comum import split_resto, string_to_ip, mascara
from threading import Condition


class Interface(object):
    def __init__(self, buffer_entrada):
        self.buffer_entrada = buffer_entrada
        self.buffer_saída = []
        self.ip = None
        self.tamanho_buffer_router = 0

    def set_ip(self, ip):
        self.ip = ip

    def tem_saída(self):
        return len(self.buffer_saída) > 0

    def append_entrada(self, datagrama):
        if len(self.buffer_entrada) >= self.tamanho_buffer_router:
            return  # Não insere se o buffer alcançar o limite
        self.buffer_entrada.append(datagrama)

    def pop_entrada(self):
        return self.buffer_entrada.pop(0)

    def append_saída(self, datagrama):
        self.buffer_saída.append(datagrama)

    def pop_saída(self):
        return self.buffer_saída.pop(0)

    def set_tamanho_buffer(self, tamanho):
        self.tamanho_buffer_router = tamanho


conjunto_interface = {}
conjunto_tabelas = {}
processamento = {}
tamanho_buffer = {}


def set_performance(índice, resto):  # comando set performance do arquivo de entrada
    resto = split_resto(resto)
    processamento[índice] = int(resto[0][:len(resto[0]) - 2])  # gravando o inteiro excluindo us do 100us
    for i, v in zip(resto[1::2], resto[2::2]):  # de 100us 0 1000 1 1000 2 1000 temos i = 0, 1, 2 e v = 1000, 1000, 1000
        tamanho_buffer[índice][i] = v


def set_route(índice, resto):  # comando set route do arquivo de entrada
    par = split_resto(resto)
    par = [(string_to_ip(ip), outro) for ip, outro in par]
    for ip, porta in zip(par[:2*len(conjunto_interface[índice]):2], par[1:2*len(conjunto_interface[índice]):2]):
        conjunto_tabelas[índice][ip] = conjunto_interface[índice][int(porta)]
    for ip, outro_ip in zip(par[2*len(conjunto_interface[índice])::2], par[2*len(conjunto_interface[índice])+1::2]):
        conjunto_tabelas[índice][ip] = string_to_ip(outro_ip)


def set_ip(índice, resto):  # comando set ip do arquivo trace para roteador
    porta_ip = split_resto(resto)
    for porta, ip in [(int(porta), string_to_ip(ip)) for porta, ip in zip(porta_ip[::2], porta_ip[1::2])]:
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
    processamento[índice] = 0
    tamanho_buffer[índice] = {}
    for _ in range(número_interfaces):
        interfaces.append(Interface(buffer_entrada))

    def tem_entrada():
        return len(buffer_entrada) > 0

    c = Condition()
    while True:
        c.acquire()
        c.wait_for(tem_entrada)
        datagrama = buffer_entrada.pop(0)
        ip_destino = int.from_bytes(datagrama[32:64], sys.byteorder)
        while ip_destino & mascara in tabela:
            if type(tabela[ip_destino & mascara]) is Interface:
                tabela[ip_destino & mascara].push(datagrama)
            else:
                ip_destino = tabela[ip_destino & mascara]
