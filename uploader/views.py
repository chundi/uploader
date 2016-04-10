# -*- coding:utf-8 -*-

import sys
from pyramid.view import (
    view_config,
    view_defaults,
    )
from cgi import FieldStorage
import hmac
import hashlib
import time

reload(sys)
sys.setdefaultencoding('utf8')

SECRET_KEY = '308da8b8b4ea3873cf320be826b622d8'

LOG_PATH = '/tmp'

class BaseView(object):
    def __init__(self, request):
        self.request = request

@view_defaults(route_name = 'log')
class UploadFileView(BaseView):
    def __init__(self, request):
        super(UploadFileView, self).__init__(request)

    @view_config(request_method = 'POST', renderer = 'json')
    def post(self):
        log_files = self.request.POST.getall('log')
        if not log_files:
            return 'no log file'
        log_file = log_files[0]
        if not isinstance(log_file, FieldStorage):
            return 'not actual file'
        try:
            fname = log_file.filename
            buf = log_file.file.read()
            log_path = '{0}/{1}'.format(LOG_PATH, fname)
            _file = file(log_path, 'w')
            _file.write(buf)
            _file.close()
        except Exception as ex:
            print ex
            return 'upload error: {0}'.format(str(ex))
        return 'success'

