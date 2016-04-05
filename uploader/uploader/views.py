# -*- coding:utf-8 -*-

from pyramid.view import (
    view_config,
    view_defaults,
    )
import hmac
import hashlib
import time
import uuid

SECRET_KEY = '308da8b8b4ea3873cf320be826b622d8'

class BaseView(object):
    def __init__(self, request):
        self.request = request


@view_defaults(route_name = 'upload_token')
class UploadTokenView(BaseView):
    def __init__(self, request):
        super(UploadTokenView, self).__init__(request)

    @view_config(request_method = 'GET', renderer = 'json')
    def get(self):
        device_id = self.request.params.get('device_id', '')
        if not device_id:
            return 'no device_id'
        _uuid = uuid.uuid4()
        token = hmac.new(_uuid.hex, digestmod = hashlib.sha1)
        token = token.hexdigest()
        now = int(time.time())
        data = {}
        data['ts'] = now
        data['token'] = token
        return data

@view_defaults(route_name = 'file')
class UploadFileView(BaseView):
    def __init__(self, request):
        super(UploadFileView, self).__init__(request)

    @view_config(request_method = 'POST', renderer = 'json')
    def post(self):
        return 'done'

