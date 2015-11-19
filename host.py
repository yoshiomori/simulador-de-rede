import sys
from interface import Interface
from relógio import time


class InterfaceHost(Interface):
    def __init__(self):
        super().__init__()
        self.buffer_entrada = []
        self.dns = 0
        self.roteador_padrão = 0

    def set_dns(self, ip):
        self.dns = ip

    def set_roteador_padrão(self, roteador_padrão):
        self.roteador_padrão = roteador_padrão

    def tem_entrada(self):
        return len(self.buffer_entrada) > 0

    def append_entrada(self, datagrama):
        if int.from_bytes(datagrama[32:64], sys.byteorder) == self.ip:
            self.buffer_entrada.append(datagrama)

    def pop_entrada(self):
        return self.buffer_entrada.pop(0)

interfaces = []
índice = []
nome_ircc = []
nome_ircs = []
nome_dnss = []
nome_dnsc = []
eventos = []
clientes = []
comandos = []


def pega_índice(nome_host):
    return índice.index(nome_host)


def set_host(nome_host):
    if nome_host in índice:
        raise RuntimeError(nome_host, 'já existe')
    índice.append(nome_host)
    interfaces.append(InterfaceHost())
    nome_ircc.append('')
    nome_ircs.append('')
    nome_dnsc.append('')
    nome_dnss.append('')


def set_ip_host(nome_host, endereço_ip_computador, endereço_ip_roteador_padrão, endereço_ip_servidor_dns):
    host = pega_índice(nome_host)
    interfaces[host].set_ip(endereço_ip_computador)
    interfaces[host].set_roteador_padrão(endereço_ip_roteador_padrão)
    interfaces[host].set_dns(endereço_ip_servidor_dns)


def set_ircc(nome_host, nome_servidor):
    índice_host = pega_índice(nome_host)
    nome_ircc[índice_host] = nome_servidor


def set_ircs(nome_host, nome_servidor):
    índice_host = pega_índice(nome_host)
    nome_ircs[índice_host] = nome_servidor


def set_dnss(nome_host, nome_servidor):
    índice_host = pega_índice(nome_host)
    nome_dnsc[índice_host] = nome_servidor


def set_ip(nome, endereço_ip_computador, endereço_ip_roteador_padrão, endereço_ip_servidor_dns):
    print(nome, endereço_ip_computador, endereço_ip_roteador_padrão, endereço_ip_servidor_dns)
    # ip_roteador_dns = split_resto(resto)
    # if len(ip_roteador_dns):
    #     raise RuntimeError('Arquivo de entrada inválido')
    # if índice not in interfaces or índice not in roteador or índice not in dns:
    #     print('Host não configurado')
    #     return
    # interfaces[índice].set_ip(string_to_ip(ip_roteador_dns[0]))
    # roteador[índice] = string_to_ip(ip_roteador_dns[1])
    # dns[índice] = string_to_ip(ip_roteador_dns[2])


def simulate(instante_tempo, nome_cliente, comando):
    eventos.append(instante_tempo)
    clientes.append(nome_cliente)
    comandos.append(comando)


# função host que deve ser chamada por uma thread
# O argumento índice é proveniente do arquivo de entrada
# O servidor é uma função que deve receber uma referência para um objeto Interface
def faz(índice, servidor):
    interface = Interface()
    interfaces[índice] = interface
    roteador[índice] = None
    dns[índice] = None

    servidor(interface)
