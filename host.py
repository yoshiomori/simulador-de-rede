from comum import split_resto, string_to_ip
from interface import Interface


class InterfaceHost(Interface):
    def __init__(self):
        super().__init__()
        self.buffer_entrada = []

    def tem_entrada(self):
        return len(self.buffer_entrada) > 0

    def append_entrada(self, datagrama):
        if datagrama[32:64] == self.ip:
            self.buffer_entrada.append(datagrama)

    def pop_entrada(self):
        return self.buffer_entrada.pop(0)

interfaces = {}
roteador = {}
dns = {}


def set_ip(índice, resto):
    ip_roteador_dns = split_resto(resto)
    if len(ip_roteador_dns):
        raise RuntimeError('Arquivo de entrada inválido')
    if índice not in interfaces or índice not in roteador or índice not in dns:
        print('Host não configurado')
        return
    interfaces[índice].set_ip(string_to_ip(ip_roteador_dns[0]))
    roteador[índice] = string_to_ip(ip_roteador_dns[1])
    dns[índice] = string_to_ip(ip_roteador_dns[2])


# função host que deve ser chamada por uma thread
# O argumento índice é proveniente do arquivo de entrada
# O servidor é uma função que deve receber uma referência para um objeto Interface
def faz(índice, servidor):
    interface = Interface()
    interfaces[índice] = interface
    ip[índice] = None
    roteador[índice] = None
    dns[índice] = None

    servidor(interface)
