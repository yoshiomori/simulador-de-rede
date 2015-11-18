def split_resto(resto):
    if resto is not str:
        raise TypeError('resto deve ser uma str')
    resto = resto.split(' ')
    while '' in resto:
        resto.remove('')
    return resto


def string_to_ip(ip):
    return bytearray([int(v) for v in ip.split('.')])
