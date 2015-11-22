import sys
from re import findall, match

from comum import string_to_ip, ip_to_string
import router
import relógio
import host
import enlace


# from enlace import set_duplex_link
# from comum import set_sniffer


def main():
    import enlace
    arquivo = open(sys.argv[1])
    for linha in arquivo.readlines():
        if match('set\s+host\s+(\w+)\n?', linha):
            nome_host = findall('set\s+host\s+(\w+)\n?', linha).pop()
            host.set_host(nome_host)
        elif match('set\s+router\s+(\w+)\s+(\d+)\n?', linha):
            nome_roteador, número_interfaces = findall('set\s+router\s+(\w+)\s+(\d+)\n?', linha).pop()
            número_interfaces = int(número_interfaces)
            router.set_router(nome_roteador, número_interfaces)
        elif match('set\s+duplex-link\s+(\w+)\s+(\w+)\s+(\w+)bps\s+(\w+)s\n?', linha):
            nome_primeiro, nome_segundo, taxa, atraso = findall(
                'set\s+duplex-link\s+(\w+)\s+(\w+)\s+(\w+)bps\s+(\w+)s\n?', linha).pop()
            p = 0
            if match('(\d+)k', taxa):
                taxa = findall('(\d+)k', taxa).pop()
                p = 3
            elif match('(\d+)M', taxa):
                taxa = findall('(\d+)M', taxa).pop()
                p = 6
            taxa = int(taxa) * 10 ** p

            p = 0
            if match('(\d+)m', atraso):
                atraso = findall('(\d+)m', atraso).pop()
                p = -3
            atraso = int(atraso) * 10 ** p
            enlace.set_duplex_link_host_host(nome_primeiro, nome_segundo, taxa, atraso)
        elif match('set\s+duplex-link\s+(\w+)\s+(\w+)\.(\d+)\s+(\w+)bps\s+(\w+)s\n?', linha):
            nome_primeiro, nome_segundo, interface, taxa, atraso = findall(
                'set\s+duplex-link\s+(\w+)\s+(\w+)\.(\d+)\s+(\w+)bps\s+(\w+)s\n?', linha).pop()
            interface = int(interface)
            p = 0
            if match('(\d+)k', taxa):
                taxa = findall('(\d+)k', taxa).pop()
                p = 3
            elif match('(\d+)M', taxa):
                taxa = findall('(\d+)M', taxa).pop()
                p = 6
            taxa = int(taxa) * 10 ** p

            p = 0
            if match('(\d+)m', atraso):
                atraso = findall('(\d+)m', atraso).pop()
                p = -3
            atraso = int(atraso) * 10 ** p
            enlace.set_duplex_link_host_router(nome_primeiro, nome_segundo, interface, taxa, atraso)
        elif match('set\s+duplex-link\s+(\w+)\.(\d+)\s+(\w+)\.(\d+)\s+(\w+)bps\s+(\w+)s\n?', linha):
            nome_primeiro, interface_primeiro, nome_segundo, interface_segundo, taxa, atraso = findall(
                'set\s+duplex-link\s+(\w+)\.(\d+)\s+(\w+)\.(\d+)\s+(\w+)bps\s+(\w+)s\n?', linha).pop()
            interface_primeiro = int(interface_primeiro)
            interface_segundo = int(interface_segundo)
            p = 0
            if match('(\d+)k', taxa):
                taxa = findall('(\d+)k', taxa).pop()
                p = 3
            elif match('(\d+)M', taxa):
                taxa = findall('(\d+)M', taxa).pop()
                p = 6
            taxa = int(taxa) * 10 ** p

            p = 0
            if match('(\d+)m', atraso):
                atraso = findall('(\d+)m', atraso).pop()
                p = -3
            atraso = int(atraso) * 10 ** p
            enlace.set_duplex_link_router_router(nome_primeiro, interface_primeiro, nome_segundo, interface_segundo, taxa,
                                          atraso)
        elif match('set\s+duplex-link\s+(\w+)\.(\d+)\s+(\w+)\s+(\w+)bps\s+(\w+)s\n?', linha):
            nome_primeiro, interface_primeiro, nome_segundo, taxa, atraso = findall(
                'set\s+duplex-link\s+(\w+)\.(\d+)\s+(\w+)\s+(\w+)bps\s+(\w+)s\n?', linha).pop()
            interface_primeiro = int(interface_primeiro)
            p = 0
            if match('(\d+)k', taxa):
                taxa = findall('(\d+)k', taxa).pop()
                p = 3
            elif match('(\d+)M', taxa):
                taxa = findall('(\d+)M', taxa).pop()
                p = 6
            taxa = int(taxa) * 10 ** p

            p = 0
            if match('(\d+)m', atraso):
                atraso = findall('(\d+)m', atraso).pop()
                p = -3
            atraso = int(atraso) * 10 ** p
            enlace.set_duplex_link_host_router(nome_segundo, nome_primeiro, interface_primeiro, taxa, atraso)
        elif match('set\s+ip\s+(\w+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)\n?', linha):
            nome_host, endereço_ip_computador, endereço_ip_roteador_padrão, endereço_ip_servidor_dns = findall(
                'set\s+ip\s+(\w+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)\n?',
                linha).pop()
            endereço_ip_computador = string_to_ip(endereço_ip_computador)
            endereço_ip_roteador_padrão = string_to_ip(endereço_ip_roteador_padrão)
            endereço_ip_servidor_dns = string_to_ip(endereço_ip_servidor_dns)
            host.set_ip_host(nome_host, endereço_ip_computador, endereço_ip_roteador_padrão, endereço_ip_servidor_dns)
        elif match('set\s+ip\s+(\w+)(\s+\d+\s+\d+\.\d+\.\d+\.\d+)+\n?', linha):
            nome_roteador = findall('set\s+ip\s+(\w+)', linha).pop()
            entrada = [(int(índice_enlace), string_to_ip(endereço_ip)) for índice_enlace, endereço_ip in
                       findall('\s+(\d+)\s+(\d+\.\d+\.\d+\.\d+)', linha)]
            router.set_ip_router(nome_roteador, entrada)
        elif match(
                'set\s+route\s+(\w+)(\s+\d+\.\d+\.\d+\.\d+\s+\d+)+(\s+\d+\.\d+\.\d+\.\d+\s+\d+\.\d+\.\d+\.\d+)*\n?',
                linha):
            nome_roteador = findall('set\s+route\s+(\w+)', linha).pop()
            entrada = [(string_to_ip(endereço_ip), int(enlace)) for endereço_ip, enlace in
                       findall('\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+)\s+', linha)] + [
                          (string_to_ip(primeiro_endereço_ip), string_to_ip(segundo_endereço_ip)) for
                          primeiro_endereço_ip, segundo_endereço_ip in
                          findall('\s+(\d+\.\d+\.\d+\.\d+)\s+(\d+\.\d+\.\d+\.\d+)', linha)]
            router.set_route(nome_roteador, entrada)
        elif match('set\s+performance\s+(\w+)+\s+(\w+)s(\s+\d+\s+\d+)+\n?', linha):
            nome_roteador, tempo_para_processar = findall('set\s+performance\s+(\w+)\s+(\w+)s', linha).pop()
            p = 0
            if match('(\d+)m', tempo_para_processar):
                tempo_para_processar = findall('(\d+)m', tempo_para_processar).pop()
                p = -3
            elif match('(\d+)u', tempo_para_processar):
                tempo_para_processar = findall('(\d+)u', tempo_para_processar).pop()
                p = -6
            tempo_para_processar = int(tempo_para_processar) * 10 ** p
            entrada = [(int(porta), int(tamanho)) for porta, tamanho in findall('\s+(\d+)\s+(\d+)', linha)]
            router.set_performance(nome_roteador, tempo_para_processar, entrada)
        elif match('set\s+ircc\s+(\w+)\s+(\w+)\n?', linha):
            nome_host, nome_cliente = findall('set\s+ircc\s+(\w+)\s+(\w+)\n?', linha).pop()
            host.set_ircc(nome_host, nome_cliente)
        elif match('set\s+ircs\s+(\w+)\s+(\w+)\n?', linha):
            nome_host, nome_servidor = findall('set\s+ircs\s+(\w+)\s+(\w+)\n?', linha).pop()
            host.set_ircs(nome_host, nome_servidor)
        elif match('set\s+dnss\s+(\w+)\s+(\w+)\n?', linha):
            nome_host, nome_servidor = findall('set\s+dnss\s+(\w+)\s+(\w+)\n?', linha).pop()
            host.set_dnss(nome_host, nome_servidor)
        elif match("""set\s+sniffer\s+\w+\.\d+\s+\w+\.\d+\s+".+"\n?""", linha):
            nome_primeiro, interface_primeiro, nome_segundo, interface_segundo, nome_arquivo = findall(
                """set\s+sniffer\s+(\w+)\.(\d+)\s+(\w+)\.(\d+)\s+"(.+)"\n?""", linha).pop()
            interface_primeiro = int(interface_primeiro)
            interface_segundo = int(interface_segundo)
            enlace.set_sniffer_router_router(nome_primeiro, interface_primeiro, nome_segundo, interface_segundo, nome_arquivo)
        elif match('set\s+sniffer\s+\w+\s+\w+\.\d+\s+".+"\n?', linha):
            nome_primeiro, nome_segundo, interface, nome_arquivo = findall(
                'set\s+sniffer\s+(\w+)\s+(\w+)\.(\d+)\s+\"(.+)\"\n?', linha).pop()
            interface = int(interface)
            enlace.set_sniffer_host_router(nome_primeiro, nome_segundo, interface, nome_arquivo)
        elif match('set\s+sniffer\s+\w+\s+\w+\s+".+"\n?', linha):
            nome_primeiro, nome_segundo, nome_arquivo = findall(
                'set\s+sniffer\s+(\w+)\s+(\w+)\s+\"(.+)\"\n?', linha).pop()
            enlace.set_sniffer_host_host(nome_primeiro, nome_segundo, nome_arquivo)
        elif match('set\s+sniffer\s+(\w+)\.(\d+)\s+\w+\s+".+"\n?', linha):
            nome_primeiro, interface, nome_segundo, nome_arquivo = findall(
                'set\s+sniffer\s+(\w+)\.(\d+)\s+(\w+)\s+\"(.+)\"\n?', linha).pop()
            interface = int(interface)
            enlace.set_sniffer_host_router(nome_segundo, nome_primeiro, interface, nome_arquivo)
        elif match('simulate\s+(\d+\.\d+)\s+(\w+)\s+"(.+)"', linha):
            instante_tempo, nome_cliente, comando = findall('simulate\s+(\d+\.\d+)\s+(\w+)\s+"(.+)"', linha).pop()
            instante_tempo = float(instante_tempo)
            host.simulate(instante_tempo, nome_cliente, comando)
        elif match('finish\s+(\d+\.\d+)', linha):
            instante_tempo = findall('finish\s+(\d+\.\d+)', linha).pop()
            instante_tempo = float(instante_tempo)
            relógio.finish(instante_tempo)
    arquivo.close()
    host.ircc_udp_inicializa()
    host.inicializa()
    router.inicializa()
    enlace.inicializa()
    relógio.faz()


if __name__ == '__main__':
    main()
