from settings import tamanho_datagrama
from datetime import timedelta
time = timedelta(0)


def relógio(maior_taxa_transferência_entre_enlaces):
    global time
    tempo_por_iteração = timedelta(seconds=tamanho_datagrama / maior_taxa_transferência_entre_enlaces)
    while True:
        time += tempo_por_iteração
