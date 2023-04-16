from multiprocessing import Process
from threading import Thread


def keepAlive(daemon=True):
    def outter(fc):
        def inner(*args):
            t = Thread(name=fc.__name__, target=fc, args=args, daemon=daemon)
            t.start()

        return inner

    return outter


def undead(daemon=True):
    def outter(fc):
        def inner(*args):
            p = Process(name=fc.__name__, target=fc, args=args, daemon=daemon)
            p.start()

        return inner

    return outter
