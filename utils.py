import time
import inspect
import os
import requests


def make_header():
    headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; WOW64)'
                       ' AppleWebKit/537.36 (KHTML, like Gecko)'
                       ' Chrome/57.0.2987.98 Safari/537.36'),
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    }
    return headers


def cached_page(url, filename, folder='cached'):
    path = os.path.join(folder, filename)
    os.makedirs(folder, exist_ok=True)

    if os.path.exists(path):
        with open(path, 'rb') as f:
            page = f.read()
            return page
    else:
        headers = make_header()
        response = requests.get(url, headers)
        page = response.content
        with open(path, 'wb') as f:
            f.write(page)
        return page


def log(*args, **kwargs):
    caller_info = caller()
    fmt = '%Y-%m-%d %H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(fmt, value)

    with open('log.log', 'a', encoding='utf-8') as f:
        print(dt, caller_info, '\nLog:', *args, file=f, **kwargs)


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
