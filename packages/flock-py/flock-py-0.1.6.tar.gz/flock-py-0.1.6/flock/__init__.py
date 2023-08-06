# encoding: utf8

"""
flock.py
@author Meng.yangyang
@description 文件锁
@created Mon Mar 04 2019 10:42:06 GMT+0800 (CST)
"""

import os
import fcntl
import functools

__all__ = ('FLock', 'flock_decorator')


class FLock(object):
    """
    文件锁
    """

    def __init__(self, filepath):
        """
        :param filepath 文件路径
        """
        self.filepath = filepath
        if not os.path.exists(os.path.dirname(filepath)):
            os.makedirs(os.path.dirname(filepath))

        self.f = open(filepath, 'w')

    def __enter__(self):
        try:
            fcntl.flock(self.f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError:
            raise Exception('Acquire [%s] lock error' %
                            (self.filepath.encode('utf8') if isinstance(self.filepath, unicode) else self.filepath))

    def __exit__(self, exc_type, exc_value, traceback):
        if self.f:
            self.f.close()


def flock_decorator(filepath):
    def wrapper_decorate(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if not os.path.exists(os.path.dirname(filepath)):
                os.makedirs(os.path.dirname(filepath))

            try:
                f_obj = None
                f_obj = open(filepath, 'w')
                fcntl.flock(f_obj.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return f(*args, **kwargs)
            except IOError:
                raise Exception('Acquire [%s] lock error' %
                                (filepath.encode('utf8') if isinstance(filepath, unicode) else filepath))
            finally:
                if f_obj:
                    f_obj.close()
        return wrapper
    return wrapper_decorate
