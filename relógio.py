from comum import resolução_tempo
from datetime import timedelta
from threading import Lock
time = timedelta(0)

sequencia = Lock()


def faz():
    global time
    tempo_por_iteração = timedelta(microseconds=resolução_tempo)
    while True:
        sequencia.acquire()
        time += tempo_por_iteração
        sequencia.release()
