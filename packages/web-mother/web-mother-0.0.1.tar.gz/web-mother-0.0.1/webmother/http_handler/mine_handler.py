# coding=utf-8

from tweb import base_handler, myweb
from tornado import gen
from webmother.service.async_wrap import ctrl_mine


class MyIdentitiesHandler(base_handler.BaseHandler):
    """
    获取我的组织列表
    """

    @myweb.authenticated
    @gen.coroutine
    def get(self):
        uid = self.request.headers.get('x-user-id')
        access_token = self.request.headers.get('x-access-token')

        array = yield ctrl_mine.my_identities(uid, access_token)
        return self.write({'list': array})
