from threading import Condition
from datetime import timedelta
from relógio import time, sequencia


def set_duplex_link_host_host(primeiro, segundo, taxa, atraso):
    print(primeiro, segundo, taxa, atraso)


def set_duplex_link_host_router(primeiro, segundo, interface, taxa, atraso):
    print(primeiro, segundo, interface, taxa, atraso)


def set_duplex_link_router_router(primeiro, interface_primeiro, segundo, interface_segundo, taxa, atraso):
    print(primeiro, interface_primeiro, segundo, interface_segundo, taxa, atraso)


def set_duplex_link_router_host(primeiro, interface, segundo, taxa, atraso):
    print(primeiro, interface, segundo, taxa, atraso)


def set_sniffer_router_router(nome_primeiro, interface_primeiro, nome_segundo, interface_segundo, nome_arquivo):
    print(nome_primeiro, interface_primeiro, nome_segundo, interface_segundo, nome_arquivo)


def set_sniffer_host_router(nome_primeiro, nome_segundo, interface, nome_arquivo):
    print(nome_primeiro, nome_segundo, interface, nome_arquivo)


def set_sniffer_host_host(nome_primeiro, nome_segundo, nome_arquivo):
    print(nome_primeiro, nome_segundo, nome_arquivo)


def set_sniffer_router_host(nome_primeiro, interface, nome_segundo, nome_arquivo):
    print(nome_primeiro, interface, nome_segundo, nome_arquivo)


def faz(push_entrada, pop_saída, tem_saída, taxa_transferência, atraso):
    c = Condition()
    while True:
        c.acquire()
        c.wait_for(tem_saída)
        agora = time()
        c.acquire()
        c.wait_for(lambda: time() - agora >= timedelta(microseconds=atraso))
        sequencia.acquire()
        while tem_saída():
            datagrama = pop_saída()
            agora = time()
            sequencia.release()
            c.acquire()
            c.wait_for(lambda: time() - agora >= timedelta(len(datagrama)/taxa_transferência))
            sequencia.acquire()
            push_entrada(datagrama)
        sequencia.release()
