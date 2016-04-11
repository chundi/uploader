# -*- coding:utf-8 -*-

from uploader.config import (
    SECRET_KEY,
    LOG_PATH,
    )
import hmac
import hashlib
import urllib
import os

def generate_sign(**kw_args):
    '''
    生成签名，

    Args:
        **kw_args:词典类型参数

    Returns:
        生成的签名字符串，全大写

    Usage:
        sign = generate_sign(arg1 = 'a', arg2 = 2, arg3 = arg3)
    '''
    keys = sorted(kw_args.keys())
    qstr = ''
    for k in keys:
        formatter = '&{0}={1}' if qstr else '{0}={1}'
        qstr = qstr + formatter.format(k, kw_args[k])
    en_qstr = urllib.quote(qstr)
    return hmac.new(SECRET_KEY, en_qstr, hashlib.sha1).hexdigest().upper()

def save_file(fname, buf):
    '''
    保存内容到文件

    Args:
        fname:需要保存的文件名，不带路径，比如123.txt
        buf:要保存的内容，字符串

    Returns:
        1:保存成功
        0:保存失败
    '''
    try:
        _file = None
        if not os.path.exists(LOG_PATH):
            os.makedirs(LOG_PATH)
        log_path = '{0}/{1}'.format(LOG_PATH, fname)
        _file = file(log_path, 'w')
        _file.write(buf)
    except Exception as ex:
        print ex
        return 0
    finally:
        if _file: _file.close()
    return 1

if __name__ == '__main__':
    import time
    ts = int(time.time())
    print ts
    print generate_sign(device_id = 'abc', log_type = 'transaction', ts = ts)

