from threading import Thread, enumerate as threads, current_thread, Lock
from multiprocessing import Process


def keepAlive(fc, daemon=True):
    def inner(*args):
        t = Thread(name=fc.__name__, target=fc, args=args, daemon=daemon)
        t.start()

    return inner


def undead(fc, daemon=True):
    def inner(*args):
        p = Process(name=fc.__name__, target=fc, args=args, daemon=daemon)
        p.start()

    return inner
