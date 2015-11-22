import router
import host
from datetime import timedelta
from relógio import time, tempo_por_iteração, todas_iterações

índice_host = []
índice_interface_router = []
índice_duplex_link = []
com_sniffer = []
fds = []
taxas = []
atrasos = []


def set_duplex_link(taxa, atraso):
    taxas.append(taxa)
    atrasos.append(timedelta(microseconds=atraso))
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

    índice_duplex_link.append((host.interfaces[primeiro], host.interfaces[segundo]))

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

    índice_duplex_link.append((host.interfaces[primeiro], router.conjunto_interfaces[segundo][interface]))

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

    índice_duplex_link.append((router.conjunto_interfaces[índice_primeiro][interface_primeiro],
                               router.conjunto_interfaces[índice_segundo][interface_segundo]))

    set_duplex_link(taxa, atraso)


def set_sniffer_router_router(nome_primeiro, interface_primeiro, nome_segundo, interface_segundo, nome_arquivo):
    índice_router_primeiro = router.pega_índice(nome_primeiro)
    índice_router_segundo = router.pega_índice(nome_segundo)

    # O índice do enlace entre A e B pode ser achada usando o par (A,B) se o índice de A, em índice_interface_router,
    # for menor do que o índice de B, em índice_interface_router
    i1 = índice_interface_router.index((índice_router_primeiro, interface_primeiro))
    i2 = índice_interface_router.index((índice_router_segundo, interface_segundo))

    chave = (router.conjunto_interfaces[índice_router_primeiro][interface_primeiro],
             router.conjunto_interfaces[índice_router_segundo][interface_segundo]) if i1 < i2 else (
        router.conjunto_interfaces[índice_router_segundo][interface_segundo],
        router[índice_router_primeiro][interface_primeiro])
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
        i = índice_duplex_link.index(
            (host.interfaces[índice_primeiro], router.conjunto_interfaces[índice_segundo][interface]))
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


def inicializa():
    for índice, par in enumerate(índice_duplex_link):
        primeiro, segundo = par
        todas_iterações.append(
            (
                enlace,
                (índice, primeiro.append_entrada, segundo.pop_saída, lambda: len(segundo.buffer_saída.buffer), None,
                 atrasos[índice], None)))
        todas_iterações.append(
            (
                enlace,
                (índice, segundo.append_entrada, primeiro.pop_saída, lambda: len(primeiro.buffer_saída.buffer), None,
                 atrasos[índice], None)))


def enlace(índice, append_entrada, pop_saída, tem_saída, tempo_para_envio, atraso, datagrama):
    if tem_saída():
        if atraso:
            todas_iterações.append(
                (enlace, (índice, append_entrada, pop_saída, tem_saída, tempo_para_envio, atraso - tempo_por_iteração,
                          datagrama)))
        else:
            if tempo_para_envio is None:
                datagrama = pop_saída()
                todas_iterações.append((enlace, (
                    índice, append_entrada, pop_saída, tem_saída, timedelta(seconds=len(datagrama) / taxas[índice]),
                    atraso,
                    datagrama)))
            elif tempo_para_envio >= timedelta(0):
                todas_iterações.append((enlace, (
                    índice, append_entrada, pop_saída, tem_saída, tempo_para_envio - tempo_por_iteração, atraso,
                    datagrama)))
            else:
                append_entrada(datagrama)
                todas_iterações.append(
                    (enlace, (índice, append_entrada, pop_saída, tem_saída, None, atrasos[índice], b'')))
    else:
        todas_iterações.append(
            (enlace,
             (índice, append_entrada, pop_saída, tem_saída, tempo_para_envio, atraso - tempo_por_iteração, datagrama)))
