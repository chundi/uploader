# -*- coding:utf-8 -*-

from pyramid.view import (
    view_config,
    view_defaults,
    )
from cgi import FieldStorage
from uploader.config import LOG_TYPES
from uploader.utils import (
    generate_sign,
    save_file,
    )
import time
import datetime


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

