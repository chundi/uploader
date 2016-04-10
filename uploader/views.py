# -*- coding:utf-8 -*-

from pyramid.view import (
    view_config,
    view_defaults,
    )
from cgi import FieldStorage
import hmac
import hashlib
import time
import datetime
import urllib

SECRET_KEY = '308da8b8b4ea3873cf320be826b622d8'
#LOG_PATH = '/var/www/example.com/data'
LOG_PATH = '/tmp'
LOG_TYPES = ['debug', 'transaction']


class BaseView(object):
    def __init__(self, request):
        self.request = request


@view_defaults(route_name = 'log')
class UploadLogView(BaseView):
    def __init__(self, request):
        super(UploadLogView, self).__init__(request)

    @view_config(request_method = 'POST', renderer = 'json')
    def post(self):
        client_sign = self.request.params.get('sign', '')
        device_id = self.request.params.get('device_id', '')
        log_type = self.request.params.get('log_type', '')
        ts = self.request.params.get('ts', '')

        # 检查参数是否未传，或传值为空
        if not client_sign or not device_id or not log_type or not ts:
            return 'arguments missing'

        # 检查传入log类型是否在要求范围内
        if log_type not in LOG_TYPES:
            return 'log type error'

        # 检查传入时间是否是数字类型
        if not ts.isdigit():
            return 'time format error'

        # 查检上传时间与当前时间间隔是否超过5分钟
        if int(time.time()) - int(ts) > 300:
            return 'timeout'

        # 验证签名
        sign = generate_sign(device_id = device_id, log_type = log_type, ts = ts)
        if sign != client_sign.upper():
            return 'permission denied'

        # 获取上传的log参数，getall方法会返回一个列表，如果没有该参数，也会返回一个空的列表
        log_files = self.request.POST.getall('log')
        if not log_files:
            return 'no log file'

        # 检查log是否为文件对象
        log_file = log_files[0]
        if not isinstance(log_file, FieldStorage):
            return 'not actual file'

        # 生成日志文件名
        today = datetime.datetime.now().date()
        fname = today.strftime('{0}-%Y%m%d'.format(log_type))

        # 保存文件
        res = save_file(fname, log_file.file.read())

        if not res:
            return 'upload error'
        return 'success'


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
        log_path = '{0}/{1}'.format(LOG_PATH, fname)
        _file = file(log_path, 'w')
        _file.write(buf)
        _file.close()
    except Exception as ex:
        print ex
        return 0
    finally:
        if _file: _file.close()
    return 1

if __name__ == '__main__':
    ts = int(time.time())
    print ts
    print generate_sign(device_id = 'abc', log_type = 'transaction', ts = ts)

