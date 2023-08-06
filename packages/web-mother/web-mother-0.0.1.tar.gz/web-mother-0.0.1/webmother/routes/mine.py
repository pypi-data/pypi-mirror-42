# coding=utf-8

import config
from webmother.http_handler import mine_handler as h

base = '{}/pls/mng/mine'.format(config.VER)
routes = [
    # 获取我的组织列表
    (rf"/{base}/identities", h.MyIdentitiesHandler),
]
