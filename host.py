class Interface(object):
    def __init__(self):
        self.buffer_entrada = []
        self.buffer_saída = []

    def tem_saída(self):
        return len(self.buffer_saída) > 0

    def tem_entrada(self):
        return len(self.buffer_entrada) > 0

interfaces = {}
ip = {}
roteador = {}
dns = {}


def set_ip(índice, ip_host, roteador_padrão, dns_padrão):
    if índice not in ip or índice not in roteador or índice not in dns:
        print('Host não configurado')
        return
    ip[índice] = bytearray([int(v) for v in ip_host.split('.')])
    roteador[índice] = bytearray([int(v) for v in roteador_padrão.split('.')])
    dns[índice] = bytearray([int(v) for v in dns_padrão.split('.')])


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
