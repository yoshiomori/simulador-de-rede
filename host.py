import sys
from comum import string_to_ip, ip_to_string
from interface import Interface
import relógio
from datetime import timedelta

interfaces = []
nomes_host = []
nome_ircc = []
nome_ircs = []
nome_dnss = []
nome_dnsc = []
eventos = []
todos_dns = []
todos_ip_router = []
todos_nomes_clientes = {}


def pega_índice(nome_host):
    return nomes_host.index(nome_host)


def set_host(nome_host):
    if nome_host in nomes_host:
        raise RuntimeError(nome_host, 'já existe')
    nomes_host.append(nome_host)
    interfaces.append(Interface())
    nome_ircc.append('')
    nome_ircs.append('')
    nome_dnsc.append('')
    nome_dnss.append('')
    todos_dns.append(b'')
    todos_ip_router.append(b'')


def set_ip_host(nome_host, endereço_ip_computador, endereço_ip_roteador_padrão, endereço_ip_servidor_dns):
    host = pega_índice(nome_host)
    interfaces[host].set_ip(endereço_ip_computador)
    todos_ip_router.append(endereço_ip_roteador_padrão)
    todos_dns.append(endereço_ip_servidor_dns)


def set_ircc(nome_host, nome_servidor):
    índice_host = pega_índice(nome_host)
    nome_ircc[índice_host] = nome_servidor


def set_ircs(nome_host, nome_servidor):
    índice_host = pega_índice(nome_host)
    nome_ircs[índice_host] = nome_servidor


def set_dnss(nome_host, nome_servidor):
    índice_host = pega_índice(nome_host)
    nome_dnsc[índice_host] = nome_servidor


def simulate(instante_tempo, nome_cliente, comando):
    eventos.append((timedelta(seconds=instante_tempo), nome_cliente, comando))


class Socket(object):
    def __init__(self, índice):
        self.índice = índice

    def recebe_de(self):
        datagrama = interfaces[self.índice].pop_entrada()
        return (ip_to_string(int.from_bytes(datagrama[:4], sys.byteorder)),
                int.from_bytes(datagrama[12:14], sys.byteorder)), datagrama[18:]

    def envia_para(self, endereço, mensagem):
        ip, porta = endereço
        if type(mensagem) is not bytes:
            raise RuntimeError('mensagem deve ser bytes, não %s' % type(mensagem))
        pacote = int(6667).to_bytes(2, sys.byteorder) + int(porta).to_bytes(2, sys.byteorder) + int(
            len(mensagem)).to_bytes(2, sys.byteorder) + mensagem
        datagrama = interfaces[self.índice].ip.to_bytes(4, sys.byteorder)
        datagrama += string_to_ip(ip).to_bytes(4, sys.byteorder) + int(17).to_bytes(1, sys.byteorder)
        datagrama += int(10 + len(pacote)).to_bytes(2, sys.byteorder) + int(64).to_bytes(1, sys.byteorder)
        interfaces[self.índice].append_saída(datagrama)


def ircs(índice):
    socket = Socket(índice)
    dns = todos_dns[índice]
    ip_router = todos_ip_router[índice]
    print('Servidor %s está esperando uma mensagem' % nomes_host[índice])
    try:
        endereço, mensagem = socket.recebe_de()
        print(endereço, mensagem.decode())
        mensagem = mensagem.decode()
        mensagem = mensagem.split(' ')
        if mensagem[0] == 'CONNECT':
            socket.envia_para(endereço, 'ok')
        elif mensagem[0] == 'USER':
            socket.envia_para(endereço, 'ok')
        elif mensagem[0] == 'QUIT':
            socket.envia_para(endereço, 'ok')
        relógio.todas_iterações.append((ircs, (índice,)))
    except TimeoutError:
        pass


def dns(índice):
    socket = Socket(índice)
    while True:
        print('Servidor %s está esperando uma mensagem' % nomes_host[índice])
        endereço, mensagem = socket.recebe_de()
        print(endereço, mensagem.decode())
        socket.envia_para(('10.0.0.1', 6667), mensagem)


def ircc_udp_inicializa():
    for instante, nome_cliente, comando in eventos:
        relógio.todas_iterações.append((ircc_udp, (instante, nome_cliente, comando)))


def ircc_udp(instante, nome_cliente, comando):
    if instante <= relógio.time:
        mensagem, sep, resto = comando.partition(' ')
        if mensagem == 'CONNECT':
            host, sep, porta = resto.partition(' ')
            todos_nomes_clientes[nome_cliente] = (host, porta)
        else:
            ip, port = todos_nomes_clientes[nome_cliente]
            if '.' in ip:
                Socket(nome_ircc.index(nome_cliente)).envia_para(todos_nomes_clientes[nome_cliente],
                                                                 mensagem.encode('unicode_escape'))
    else:
        relógio.todas_iterações.append((ircc_udp, (instante - relógio.tempo_por_iteração, nome_cliente, comando)))


def inicializa():
    for índice, nome in enumerate(nome_ircs):
        if nome is not '':
            relógio.todas_iterações.append((ircs, (índice,)))
