class Interface(object):
    def __init__(self):
        self.buffer_entrada = []
        self.buffer_saída = []
        self.ip = None

    def set_ip(self, ip):
        self.ip = ip

    def tem_saída(self):
        return len(self.buffer_saída) > 0

    def tem_entrada(self):
        return len(self.buffer_entrada) > 0

    def append_entrada(self, datagrama):
        if datagrama[32:64] == self.ip:
            self.buffer_entrada.append(datagrama)

    def pop_entrada(self):
        return self.buffer_entrada.pop(0)

    def append_saída(self, datagrama):
        self.buffer_saída.append(datagrama)

    def pop_saída(self):
        return self.buffer_saída.pop(0)

interfaces = {}
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
