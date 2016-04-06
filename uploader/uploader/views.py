# -*- coding:utf-8 -*-

from pyramid.view import (
    view_config,
    view_defaults,
    )
import hmac
import hashlib
import time
import uuid
import sqlite3

SECRET_KEY = '308da8b8b4ea3873cf320be826b622d8'
sqlite_uri = '/tmp/uploader.db'

class BaseView(object):
    def __init__(self, request):
        self.request = request

def execute_sql(sql, *argv):
    try:
        cursor = ''
        conn = sqlite3.connect(sqlite_uri)
        cursor = conn.cursor()
        res = cursor.execute(sql, *argv)
        conn.commit()
        return res.rowcount
    except Exception, ex:
        print ex
        conn.rollback()
        return None
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def query_sql(sql, *argv):
    try:
        cursor = ''
        conn = sqlite3.connect(sqlite_uri)
        cursor = conn.cursor()
        res = cursor.execute(sql, *argv)
        conn.commit()
        return res.fetchall()
    except Exception, ex:
        print ex
        conn.rollback()
        return []
    finally:
        if cursor: cursor.close()
        if conn: conn.close()

def init_db():
    sql = "create table if not exists upload_token(id integer primary key not null, device_id varchar(64), token varchar(64), ts timestamp default (datetime('now', 'localtime')));"
    execute_sql(sql)

def generate_upload_token():
    return uuid.uuid4().hex

def save_upload_token(device_id, token):
    sql = "insert into upload_token (device_id, token) values (?, ?);"
    res = execute_sql(sql, (device_id, token))
    return 1

def get_upload_token(device_id):
    sql = "select token from upload_token where device_id = ? order by id desc limit 1;"
    res = query_sql(sql, (device_id,))
    if len(res) > 0: res = res[0][0]
    return res

def check_upload_token(device_id, sign):
    return ''


@view_defaults(route_name = 'upload_token')
class UploadTokenView(BaseView):
    def __init__(self, request):
        super(UploadTokenView, self).__init__(request)

    @view_config(request_method = 'GET', renderer = 'json')
    def get(self):
        device_id = self.request.params.get('device_id', '')
        if not device_id:
            return 'no device_id'
        token = generate_upload_token()
        save_upload_token(device_id, token)
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

if __name__ == '__main__':
    init_db()
    print get_upload_token('123')

