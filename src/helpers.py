"""
general helpers for the application
"""
import threading
import errno
import os


def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def set_interval(func, mins):
    sec = mins * 60000

    def func_wrapper():
        set_interval(func, sec)
        func()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t
