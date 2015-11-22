import sys
import threading, sys
import relógio
mascara = int.from_bytes(bytearray([255, 255, 255, 0]), sys.byteorder)


def split_resto(resto):
    if resto is not str:
        raise TypeError('resto deve ser uma str')
    resto = resto.split(' ')
    while '' in resto:
        resto.remove('')
    return resto


def string_to_ip(ip):
    return int.from_bytes(bytearray([int(v) for v in ip.split('.')]), sys.byteorder)


def ip_to_string(ip):
    return '.'.join([str(u) for u in ip.to_bytes(4, sys.byteorder)])


class Slock(object):
    def __init__(self):
        self.lock = threading.Lock()
        relógio.todos_releases.append(self.lock.release)

    def acquire(self):
        self.lock.acquire()
        if relógio.time >= relógio.final:
            raise TimeoutError()

    def release(self):
        self.lock.release()
