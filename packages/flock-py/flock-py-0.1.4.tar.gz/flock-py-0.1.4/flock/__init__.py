# encoding: utf8

"""
flock.py
@author Meng.yangyang
@description 文件锁
@created Mon Mar 04 2019 10:42:06 GMT+0800 (CST)
"""

import os
import fcntl
import platform
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
        self.f.seek(0)
        self.f.write('lock')
        self.f.flush()

    def __enter__(self):
        try:
            fcntl.flock(self.f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except IOError as e:
            err = False
            if platform.mac_ver()[0]:
                if e.errno == 35:
                    err = True
            elif platform.system() == 'Linux':
                if e.errno == 11:
                    err = True

            if err:
                raise Exception('Acquire [%s] lock error' %
                                (self.filepath.encode('utf8') if isinstance(self.filepath, unicode) else self.filepath))

    def __exit__(self, exc_type, exc_value, traceback):
        self.f.seek(0)
        self.f.write('unlock')
        self.f.close()


def flock_decorator(filepath):
    def wrapper_decorate(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            if not os.path.exists(os.path.dirname(filepath)):
                os.makedirs(os.path.dirname(filepath))

            f_obj = open(filepath, 'w')
            f_obj.seek(0)
            f_obj.write('lock')
            f_obj.flush()

            try:
                fcntl.flock(f_obj.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return f(*args, **kwargs)
            except IOError as e:
                err = False
                if platform.mac_ver()[0]:
                    if e.errno == 35:
                        err = True
                elif platform.system() == 'Linux':
                    if e.errno == 11:
                        err = True

                if err:
                    raise Exception('Acquire [%s] lock error' % (filepath.encode('utf8') if isinstance(filepath, unicode) else filepath))
            finally:
                f_obj.seek(0)
                f_obj.write('unlock')
                f_obj.close()
        return wrapper
    return wrapper_decorate
