""" the helpers package contains help functions for the application """
import os
from datetime import datetime
import errno
import pytz


def get_time_now(stringify=False):
    """ returns a proper default UTC timezone now time. """

    now = datetime.utcnow().replace(tzinfo=pytz.UTC)
    if stringify:
        return now.strftime('%s')

    return now


def touch(fname, times=None):
    """ touches a file as you would do in bash. """

    with open(fname, 'a'):
        os.utime(fname, times)


def mkdir_p(path):
    """ makes diretory, recursively. """

    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise
