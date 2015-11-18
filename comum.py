import sys

resolução_tempo = 20  # Em milissegundos
mascara = int.from_bytes(bytearray([255, 255, 255, 0]), sys.byteorder)


def split_resto(resto):
    if resto is not str:
        raise TypeError('resto deve ser uma str')
    resto = resto.split(' ')
    while '' in resto:
        resto.remove('')
    return resto


def string_to_ip(ip):
    return [int(v) for v in ip.split('.')]
