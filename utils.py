import time
import inspect


def log(*args, **kwargs):
    caller_info = caller()
    fmt = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(fmt, value)

    with open('log.log', 'a', encoding='utf-8') as f:
        print(dt, caller_info, 'Log:', *args, file=f, **kwargs)


def caller():
    frame_info = inspect.stack()
    filename = frame_info[2][1]
    lineno = frame_info[2][2]
    caller_func = frame_info[2][3]
    info = 'filename:{} lineno:{} function={}'.format(
        filename, lineno, caller_func
    )
    return info


def foo():
    log('test in foo')


if __name__ == '__main__':
    foo()
    log('test')
    log('test log')
    log('')
    log()
