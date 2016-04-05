# -*- coding:utf-8 -*-

from pyramid.view import (
    view_config,
    view_defaults,
    )

class BaseView(object):
    def __init__(self, request):
        self.request = request


@view_defaults(route_name = 'upload_token')
class UploadTokenView(BaseView):
    def __init__(self, request):
        super(UploadTokenView, self).__init__(request)

    @view_config(request_method = 'GET', renderer = 'json')
    def get(self):
        return 'upload_token'

@view_defaults(route_name = 'file')
class UploadFileView(BaseView):
    def __init__(self, request):
        super(UploadFileView, self).__init__(request)

    @view_config(request_method = 'POST', renderer = 'json')
    def post(self):
        return 'done'

