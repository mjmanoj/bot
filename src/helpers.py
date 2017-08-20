"""
the helpers package contains help functions for the application
"""
import threading
import errno
from datetime import datetime
import pytz
import os


# returns a proper default UTC timezone now time.
def get_time_now():
    return datetime.utcnow().replace(tzinfo=pytz.UTC)


# touches a file as you would do in bash.
def touch(fname, times=None):
    with open(fname, 'a'):
        os.utime(fname, times)


# makes diretory, recursively.
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


# set interval to activate a function every certain amount of minutes
def set_interval(func, mins):
    sec = mins * 60000

    def func_wrapper():
        set_interval(func, sec)
        func()

    t = threading.Timer(sec, func_wrapper)
    t.start()
    return t
