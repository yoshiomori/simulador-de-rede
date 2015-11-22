import sys
from comum import split_resto, string_to_ip, mascara
from interface import Interface, Buffer
from relógio import tempo_por_iteração, todas_iterações
from datetime import timedelta


class InterfaceRouter(Interface):
    def __init__(self):
        super().__init__()
        self.buffer_entrada = Buffer()
        self.tamanho_buffer_entrada = 0

    def append_entrada(self, datagrama):
        if len(self.buffer_entrada.buffer) >= self.tamanho_buffer_entrada:
            return  # Não insere se o buffer alcançar o limite
        self.buffer_entrada.append_buffer(datagrama)

    def pop_entrada(self):
        return self.buffer_entrada.pop_buffer()

    def set_tamanho_buffer_entrada(self, tamanho):
        self.tamanho_buffer_entrada = tamanho


conjunto_interfaces = []
conjunto_tabelas = []
todos_tempos_processamento = []

nome_roteadores = []


def pega_índice(nome_router):
    return nome_roteadores.index(nome_router)


def set_router(nome_roteador, número_interfaces):
    if nome_roteador in nome_roteadores:
        raise RuntimeError(nome_roteador, 'já existe')
    nome_roteadores.append(nome_roteador)
    conjunto_interfaces.append([InterfaceRouter() for _ in range(número_interfaces)])
    conjunto_tabelas.append({})
    todos_tempos_processamento.append(timedelta(milliseconds=0))


def set_ip_router(nome_roteador, entrada):
    índice_roteador = pega_índice(nome_roteador)
    for índice_interface, ip in entrada:
        conjunto_interfaces[índice_roteador][índice_interface].set_ip(ip)


def set_performance(nome_roteador, tempo_para_processar, entrada):  # comando set performance do arquivo de entrada
    índice_roteador = pega_índice(nome_roteador)
    todos_tempos_processamento[índice_roteador] = timedelta(milliseconds=tempo_para_processar)
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


def inicializa():
    for índice, nome in enumerate(nome_roteadores):
        for interface in conjunto_interfaces[índice]:
            todas_iterações.append(
                (router, (índice, interface, conjunto_tabelas[índice], todos_tempos_processamento[índice])))


# Cada router tem um índice associado a ele
# O índice de cada router é usado para acessar o seu conjunto de interfaces
# Função que inicializa um router
def router(índice, interface, tabela, tempo_processamento):
    try:
        if tempo_processamento <= timedelta(0):
            datagrama = interface.pop_entrada()
            ip_destino = int.from_bytes(datagrama[32:64], sys.byteorder)
            while ip_destino & mascara in tabela:
                if type(tabela[ip_destino & mascara]) is Interface:
                    tabela[ip_destino & mascara].push(datagrama)
                else:
                    ip_destino = tabela[ip_destino & mascara]
            tempo_processamento = todos_tempos_processamento[índice]
        else:
            tempo_processamento -= tempo_por_iteração
        todas_iterações.append((router, (índice, interface, tabela, tempo_processamento)))
    except TimeoutError:
        pass
