# -*- coding:utf-8 -*-

from pyramid.view import (
    view_config,
    view_defaults,
    )
import hmac
import hashlib
import time

SECRET_KEY = '308da8b8b4ea3873cf320be826b622d8'

class BaseView(object):
    def __init__(self, request):
        self.request = request

@view_defaults(route_name = 'file')
class UploadFileView(BaseView):
    def __init__(self, request):
        super(UploadFileView, self).__init__(request)

    @view_config(request_method = 'POST', renderer = 'json')
    def post(self):
        return 'done'

if __name__ == '__main__':
    init_db()
    print get_upload_token('123')

