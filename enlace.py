import router
import host
from threading import Condition
from datetime import timedelta
from relógio import time, sequencia

índice_host = []
índice_interface_router = []
índice_duplex_link = []
com_sniffer = []
fds = []
taxas = []
atrasos = []


def set_duplex_link(taxa, atraso):
    taxas.append(taxa)
    atrasos.append(atraso)
    com_sniffer.append(False)
    fds.append(None)


def set_duplex_link_host_host(primeiro, segundo, taxa, atraso):
    primeiro = host.pega_índice(primeiro)
    if primeiro in índice_host:
        raise RuntimeError('%s já tem duplex_link' % primeiro)
    índice_host.append(primeiro)

    segundo = host.pega_índice(segundo)
    if segundo in índice_host:
        raise RuntimeError('%s já tem duplex_link' % segundo)
    índice_host.append(segundo)

    índice_duplex_link.append((primeiro, segundo))

    set_duplex_link(taxa, atraso)


def set_duplex_link_host_router(primeiro, segundo, interface, taxa, atraso):
    primeiro = host.pega_índice(primeiro)
    if primeiro in índice_host:
        raise RuntimeError('%s já tem duplex_link' % primeiro)
    índice_host.append(primeiro)

    segundo = router.pega_índice(segundo)
    if (segundo, interface) in índice_interface_router:
        raise RuntimeError('%s já tem duplex_link' % segundo)
    índice_interface_router.append((segundo, interface))

    índice_duplex_link.append((primeiro, (segundo, interface)))

    set_duplex_link(taxa, atraso)


def set_duplex_link_router_router(primeiro, interface_primeiro, segundo, interface_segundo, taxa, atraso):
    índice_primeiro = router.pega_índice(primeiro)
    if (índice_primeiro, interface_primeiro) in índice_interface_router:
        raise RuntimeError('%s já tem duplex_link' % primeiro)
    índice_interface_router.append((índice_primeiro, interface_primeiro))

    índice_segundo = router.pega_índice(segundo)
    if (índice_segundo, interface_segundo) in índice_interface_router:
        raise RuntimeError('%s já tem duplex_link' % segundo)
    índice_interface_router.append((índice_segundo, interface_segundo))

    índice_duplex_link.append(((índice_primeiro, interface_primeiro), (índice_segundo, interface_segundo)))

    set_duplex_link(taxa, atraso)


def set_sniffer_router_router(nome_primeiro, interface_primeiro, nome_segundo, interface_segundo, nome_arquivo):
    índice_router_primeiro = router.pega_índice(nome_primeiro)
    índice_router_segundo = router.pega_índice(nome_segundo)

    # O índice do enlace entre A e B pode ser achada usando o par (A,B) se o índice de A, em índice_interface_router,
    # for menor do que o índice de B, em índice_interface_router
    i1 = índice_interface_router.index((índice_router_primeiro, interface_primeiro))
    i2 = índice_interface_router.index((índice_router_segundo, interface_segundo))

    chave = ((índice_router_primeiro, interface_primeiro), (índice_router_segundo, interface_segundo)) if i1 < i2 else (
        (índice_router_segundo, interface_segundo), (índice_router_primeiro, interface_primeiro))
    try:
        i = índice_duplex_link.index(chave)
    except ValueError:
        raise RuntimeError('Não existe enlace entre %s.%d %s.%d' % (
            nome_primeiro, interface_primeiro, nome_segundo, interface_segundo))
    com_sniffer[i] = True
    fds[i] = open(nome_arquivo, 'w')


def set_sniffer_host_router(nome_primeiro, nome_segundo, interface, nome_arquivo):
    índice_primeiro = host.pega_índice(nome_primeiro)
    índice_segundo = router.pega_índice(nome_segundo)
    try:
        i = índice_duplex_link.index((índice_primeiro, (índice_segundo, interface)))
    except ValueError:
        raise RuntimeError('Não existe enlace entre %s %s.%d' % (nome_primeiro, nome_segundo, interface))
    com_sniffer[i] = True
    fds[i] = open(nome_arquivo, 'w')


def set_sniffer_host_host(nome_primeiro, nome_segundo, nome_arquivo):
    índice_primeiro = host.pega_índice(nome_primeiro)
    índice_segundo = host.pega_índice(nome_segundo)

    # O índice do enlace entre A e B pode ser achada usando o par (A,B) se o índice de A, em índice_interface_router,
    # for menor do que o índice de B, em índice_interface_router
    i1 = índice_host.index(índice_primeiro)
    i2 = índice_host.index(índice_segundo)

    chave = (índice_primeiro, índice_segundo) if i1 < i2 else (índice_segundo, índice_primeiro)
    try:
        i = índice_duplex_link.index(chave)
    except ValueError:
        raise RuntimeError('Não existe enlace entre %s %s' % (nome_primeiro, nome_segundo))
    com_sniffer[i] = True
    fds[i] = open(nome_arquivo, 'w')


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
            c.wait_for(lambda: time() - agora >= timedelta(len(datagrama) / taxa_transferência))
            sequencia.acquire()
            push_entrada(datagrama)
        sequencia.release()
