import sys

from comum import split_resto, string_to_ip
from interface import Interface


class InterfaceHost(Interface):
    def __init__(self):
        super().__init__()
        self.buffer_entrada = []

    def tem_entrada(self):
        return len(self.buffer_entrada) > 0

    def append_entrada(self, datagrama):
        if int.from_bytes(datagrama[32:64], sys.byteorder) == self.ip:
            self.buffer_entrada.append(datagrama)

    def pop_entrada(self):
        return self.buffer_entrada.pop(0)

interfaces = {}
roteador = {}
dns = {}


def set_ip_host(nome_host, endereço_ip_computador, endereço_ip_roteador_padrão, endereço_ip_servidor_dns):
    print(nome_host, endereço_ip_computador, endereço_ip_roteador_padrão, endereço_ip_servidor_dns)


def set_ircc(nome_host, nome_servidor):
    print(nome_host, nome_servidor)


def set_ircs(nome_host, nome_servidor):
    print(nome_host, nome_servidor)


def set_dnss(nome_host, nome_servidor):
    print(nome_host, nome_servidor)


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


# função host que deve ser chamada por uma thread
# O argumento índice é proveniente do arquivo de entrada
# O servidor é uma função que deve receber uma referência para um objeto Interface
def faz(índice, servidor):
    interface = Interface()
    interfaces[índice] = interface
    roteador[índice] = None
    dns[índice] = None

    servidor(interface)


def set_host(nome_host):
    print(nome_host)
