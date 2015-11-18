class Interface(object):
    def __init__(self):
        self.buffer_saída = []
        self.ip = None

    def set_ip(self, ip):
        self.ip = ip

    def tem_saída(self):
        return len(self.buffer_saída) > 0

    def append_saída(self, datagrama):
        self.buffer_saída.append(datagrama)

    def pop_saída(self):
        return self.buffer_saída.pop(0)
