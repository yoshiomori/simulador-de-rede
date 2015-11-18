from threading import Condition
from datetime import timedelta
from relógio import time, sequencia


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
