from comum import Slock


class Buffer(object):
    def __init__(self):
        self.buffer = []
        tem_dado = Slock()  # Mutex usado para informar se tem dado no buffer
        tem_dado.acquire()  # Inicialmente não há dados no buffer
        self.tem_dado = tem_dado
        self.buffer_sendo_acessado = Slock()  # Usado para indicar que o buffer está sendo usado
        self.número_máximo_dados = float('inf')

    def append_buffer(self, dado):
        self.buffer_sendo_acessado.acquire()  # Thread pedindo o acesso ao buffer de saída
        if self.número_máximo_dados > len(self.buffer):
            self.buffer.append(dado)
        try:
            self.tem_dado.release()  # informa que há dados na saída
        except RuntimeError:
            pass
        self.buffer_sendo_acessado.release()

    def pop_buffer(self):
        self.tem_dado.acquire()
        self.buffer_sendo_acessado.acquire()  # Thread pedindo o acesso ao buffer
        dado = self.buffer.pop(0)
        if len(self.buffer) > 0:
            # Se for o último dado a ser lido e removido então informo que não há mais dados no buffer
            self.tem_dado.release()
        self.buffer_sendo_acessado.release()
        return dado

    def set_numero_máximo_dados(self, número_máximo_dados):
        self.número_máximo_dados = número_máximo_dados


class Interface(object):
    def __init__(self):
        self.buffer_saída = Buffer()
        self.buffer_entrada = Buffer()
        self.ip = None

    def set_ip(self, ip):
        self.ip = ip

    def append_saída(self, datagrama):
        self.buffer_saída.append_buffer(datagrama)

    def pop_saída(self):
        return self.buffer_saída.pop_buffer()

    def set_tamanho_máximo_buffer_entrada(self, tamanho):
        self.buffer_entrada.set_numero_máximo_dados(tamanho)

    def append_entrada(self, datagrama):
        self.buffer_entrada.append_buffer(datagrama)

    def pop_entrada(self):
        return self.buffer_entrada.pop_buffer()
