import threading


def set_interval(func, mins):
    sec = mins * 60000

    def func_wrapper():
        set_interval(func, sec)
        func()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t
