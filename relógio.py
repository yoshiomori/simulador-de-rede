from comum import tamanho_mínimo_datagrama
from datetime import timedelta
time = timedelta(0)


def faz(maior_taxa_transferência_entre_enlaces):
    global time
    tempo_por_iteração = timedelta(seconds=tamanho_mínimo_datagrama / maior_taxa_transferência_entre_enlaces)
    while True:
        time += tempo_por_iteração
