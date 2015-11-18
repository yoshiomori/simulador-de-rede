from threading import Condition
from datetime import timedelta
from relógio import time


def enlace(push_entrada, pop_saída, tem_saída, taxa_transferência, atraso):
    c = Condition()
    while True:
        c.wait_for(tem_saída)
        agora = time()
        c.wait_for(lambda: time() - agora >= timedelta(microseconds=atraso))
        while tem_saída():
            datagrama = pop_saída()
            agora = time()
            c.wait_for(lambda: time() - agora >= timedelta(len(datagrama)/taxa_transferência))
            push_entrada(datagrama)
