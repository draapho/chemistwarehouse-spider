# -*- coding:utf-8 -*-
import os
import re
import sys
import threading
import logging


def singleton(cls):
    instance = cls()
    instance.__call__ = lambda: instance
    return instance

########### debug ##########
def findcaller(func):
    def wrapper(*args, **kwargs):
        import sys
        f = sys._getframe()
        filename = f.f_back.f_code.co_filename
        lineno = f.f_back.f_lineno
        print '######################################'
        print '{}, args: {}, {}'.format(func, args, kwargs)
        print 'called by {}, line {}'.format(filename, lineno)
        print '######################################'
        func(*args, **kwargs)
    return wrapper


def logging_init(level=logging.NOTSET, file=None, append=True):
    _format = '%(asctime)s %(filename)s[%(lineno)d] %(levelname)-8s: %(message)s'
    if file is None:
        logging.basicConfig(level=level,
                            format=_format)
    else:
        if file.lower() == "local":
            file = get_cur_dir() + "\\log_info.txt"
        # default is 'a'=append, 'w'=overwrite
        mode = 'a' if append is True else 'w'
        logging.basicConfig(level=level,
                            format=_format,
                            filename=file,
                            filemode=mode)

        '''
        定义一个StreamHandler，将INFO级别或更高的日志信息打印到标准错误，并将其添加到当前的日志处理对象
        '''
        console = logging.StreamHandler()
        console.setLevel(level)
        formatter = logging.Formatter(_format)
        console.setFormatter(formatter)
        logging.getLogger('').addHandler(console)

########### thread / process ##########
class KThread(threading.Thread):

    def __init__(self, *args, **kwargs):
        threading.Thread.__init__(self, *args, **kwargs)
        self.killed = False

    def start(self):
        """Start the thread."""
        self.__run_backup = self.run
        # Force the Thread to install our trace.
        self.run = self.__run
        threading.Thread.start(self)

    def __run(self):
        """Hacked run function, which installs the trace."""
        sys.settrace(self.globaltrace)
        self.__run_backup()
        self.run = self.__run_backup

    def globaltrace(self, frame, why, arg):
        if why == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, why, arg):
        if self.killed:
            if why == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        self.killed = True


########### timeout ##########
class Timeout(Exception):
    """function run timeout"""


def timeout(timeout, default=None, try_except=False):
    """Timeout decorator, parameter in timeout."""
    def timeout_decorator(func):
        def new_func(oldfunc, result, oldfunc_args, oldfunc_kwargs):
            result.append(oldfunc(*oldfunc_args, **oldfunc_kwargs))

        """Wrap the original function."""
        def func_wrapper(*args, **kwargs):
            result = []
            # create new args for _new_func, because we want to get the func
            # return val to result list
            new_kwargs = {
                'oldfunc': func,
                'result': result,
                'oldfunc_args': args,
                'oldfunc_kwargs': kwargs
            }

            thd = KThread(target=new_func, args=(), kwargs=new_kwargs)
            thd.start()
            thd.join(timeout)
            # timeout or finished?
            isAlive = thd.isAlive()
            thd.kill()

            if isAlive:
                if try_except is True:
                    raise Timeout("{} Timeout: {} seconds.".format(func, timeout))
                return default
            else:
                return result[0]

        func_wrapper.__name__ = func.__name__
        func_wrapper.__doc__ = func.__doc__
        return func_wrapper

    return timeout_decorator


def timeout_call(timeout, func, args=(), kwargs=None, default=None, try_except=False):
    def new_func(oldfunc, result, oldfunc_args, oldfunc_kwargs):
            result.append(oldfunc(*oldfunc_args, **oldfunc_kwargs))

    result = []
    kwargs = {} if kwargs is None else kwargs
    # create new args for _new_func, because we want to get the func
    # return val to result list
    new_kwargs = {
        'oldfunc': func,
        'result': result,
        'oldfunc_args': args,
        'oldfunc_kwargs': kwargs
    }

    thd = KThread(target=new_func, args=(), kwargs=new_kwargs)
    thd.start()
    thd.join(timeout)
    # timeout or finished?
    isAlive = thd.isAlive()
    thd.kill()

    if isAlive:
        if try_except is True:
            raise Timeout("{} Timeout: {} seconds.".format(func, timeout))
        return default
    else:
        return result[0]


########### file / path ##########
def get_cur_dir():
    """
    >>> get_cur_dir()
    'can not sure...'
    """
    path = sys.path[0]

    if os.path.isdir(path):
        return path
    elif os.path.isfile(path):
        return os.path.dirname(path)


########### cook string ##########
def get_number_in_str(str):
    """
    >>> get_number_in_str("good456sdg78")
    ['456', '78']
    """
    match = re.search(r'\d+[\.]?\d+', str)
    return match.group() if match else 0
    # this can get the number from str like "good456sdg78", return ['456','78']
    # return re.findall(r'\d+[\.]?\d+', str)
    # this can get the number seperate in str like "good12sd 45 78 ", return ['45', '78']
    # return re.findall(r'\b\d+[\.]?\d+\b', str)
    # more complicated, can recognize and return [30, -10, 34.12, -12.34, 67.56E+3, -14.23e-2]
    # return re.findall("[-+]?\d+[\.]?\d+[eE]?[-+]?\d*", str)


def trim_str(str):
    """
    >>> trim_str("1, 2  3")
    '1,23'
    """
    # delete all space & tab in the line
    # return re.sub('[\s+]', '', str)
    return re.sub('\'', '', str.strip())


########### main ##########
if __name__ == '__main__':
    import doctest
    doctest.testmod()

    # import time
    # @timeout(5)
    # def count(name):
    #     for i in range(10):
    #         print("{}: {}".format(name, i))
    #         time.sleep(1)
    #     return "finished"
    # try:
    #     print count("thread1")
    #     print count("thread2")
    # except Timeout as e:
    #     print e

    # import time
    # def count(name):
    #     for i in range(10):
    #         print("{}: {}".format(name, i))
    #         time.sleep(1)
    #     return "finished"
    # try:
    #     print timeout_call(5, count, ["thread1"])
    #     print timeout_call(5, count, ["thread2"])
    # except Timeout as e:
    #     print e
