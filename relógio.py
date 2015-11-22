from datetime import timedelta
from threading import Thread

tempo_por_iteração = timedelta(milliseconds=20)
time = timedelta(0)
final = timedelta(seconds=5)

todas_iterações = []
todos_releases = []


def finish(instante):
    global final
    final = timedelta(seconds=instante)


def faz():
    global time
    todas_iterações_neste_instante_tempo = []
    while time < final:
        while any(todas_iterações):
            todas_iterações_neste_instante_tempo.append(todas_iterações.pop())
        while any(todas_iterações_neste_instante_tempo):
            iteração, argumentos = todas_iterações_neste_instante_tempo.pop()
            Thread(target=iteração, args=argumentos).start()
        time += tempo_por_iteração
    for release in todos_releases:
        try:
            release()
        except RuntimeError:
            pass
