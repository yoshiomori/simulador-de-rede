import sys

from comum import split_resto, string_to_ip, mascara
from threading import Condition
from interface import Interface


class InterfaceRouter(Interface):
    def __init__(self):
        super().__init__()
        self.buffer_entrada = []
        self.tamanho_buffer_entrada = 0

    def set_buffer_entrada(self, buffer_entrada):
        self.buffer_entrada = buffer_entrada

    def append_entrada(self, datagrama):
        if len(self.buffer_entrada) >= self.tamanho_buffer_entrada:
            return  # Não insere se o buffer alcançar o limite
        self.buffer_entrada.append(datagrama)

    def pop_entrada(self):
        return self.buffer_entrada.pop(0)

    def set_tamanho_buffer_entrada(self, tamanho):
        self.tamanho_buffer_entrada = tamanho


conjunto_interfaces = []
conjunto_tabelas = []
processamento = []

índice = []


def pega_índice(nome_router):
    return índice.index(nome_router)


def set_router(nome_roteador, número_interfaces):
    if nome_roteador in índice:
        raise RuntimeError(nome_roteador, 'já existe')
    índice.append(nome_roteador)
    conjunto_interfaces.append([InterfaceRouter() for _ in range(número_interfaces)])
    conjunto_tabelas.append({})
    processamento.append(0)


def set_ip_router(nome_roteador, entrada):
    índice_roteador = pega_índice(nome_roteador)
    for índice_interface, ip in entrada:
        conjunto_interfaces[índice_roteador][índice_interface].set_ip(ip)


def set_performance(nome_roteador, tempo_para_processar, entrada):  # comando set performance do arquivo de entrada
    índice_roteador = pega_índice(nome_roteador)
    processamento[índice_roteador] = tempo_para_processar
    for índice_interface, tamanho_buffer in entrada:
        conjunto_interfaces[índice_roteador][índice_interface].set_tamanho_buffer_entrada(tamanho_buffer)


def set_route(nome_roteador, entrada):  # comando set route do arquivo de entrada
    índice_roteador = pega_índice(nome_roteador)
    conjunto_tabelas[índice_roteador] = dict(entrada)


def set_ip(índice, resto):  # comando set ip do arquivo trace para roteador
    porta_ip = split_resto(resto)
    for porta, ip in [(int(porta), string_to_ip(ip)) for porta, ip in zip(porta_ip[::2], porta_ip[1::2])]:
        if len(ip) != 4:
            raise RuntimeError(resto, 'não é válido')
        conjunto_interfaces[índice][porta].set_ip(ip)


# Cada router tem um índice associado a ele
# O índice de cada router é usado para acessar o seu conjunto de interfaces
# Função que inicializa um router
def faz(índice, número_interfaces):
    tabela = {}  # Associo o ip à uma interface
    buffer_entrada = []

    interfaces = [Interface(buffer_entrada) for _ in range(número_interfaces)]
    conjunto_tabelas[índice] = tabela
    conjunto_interfaces[índice] = interfaces
    processamento[índice] = 0
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
