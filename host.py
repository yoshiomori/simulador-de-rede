class Interface(object):
    def __init__(self):
        self.buffer_entrada = []
        self.buffer_saída = []

    def pop(self):
        return self.buffer_saída.pop(0)

    def push(self, datagrama):
        self.buffer_entrada.append(datagrama)

    def tem_saída(self):
        return len(self.buffer_saída) > 0

    def tem_entrada(self):
        return len(self.buffer_entrada) > 0

interfaces = {}


# função host que deve ser chamada por uma thread
# O argumento índice é proveniente do arquivo de entrada
# O servidor é uma função que deve receber uma referência para um objeto Interface
def host(índice, servidor):
    interface = Interface()
    interfaces[índice] = interface
    servidor(interface)
