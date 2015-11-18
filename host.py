class Interface(object):
    def __init__(self):
        self.buffer_entrada = []
        self.buffer_saída = []

    def tem_saída(self):
        return len(self.buffer_saída) > 0

    def tem_entrada(self):
        return len(self.buffer_entrada) > 0

interfaces = {}


# função host que deve ser chamada por uma thread
# O argumento índice é proveniente do arquivo de entrada
# O servidor é uma função que deve receber uma referência para um objeto Interface
def faz(índice, servidor):
    interface = Interface()
    interfaces[índice] = interface
    servidor(interface)
