# coding=utf-8

import config
from webmother.http_handler import mine_handler as h

base = '{}/{}/mine'.format(config.VER, config.DOMAIN)
routes = [
    # 获取我的组织列表
    (rf"/{base}/identities", h.MyIdentitiesHandler),
]
