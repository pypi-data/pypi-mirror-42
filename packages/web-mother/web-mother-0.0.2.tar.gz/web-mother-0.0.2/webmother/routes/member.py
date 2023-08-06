# coding=utf-8

import config
from webmother.http_handler import member_handler as h

base = '{}/{}/member'.format(config.VER, config.DOMAIN)
routes = [

    # 组织成员的增删改查
    (rf"/{base}/org/([a-f0-9]*)/user/([a-f0-9]*)", h.MemberHandler),

    # 获取组织的成员列表
    (rf"/{base}/org/([a-f0-9]*)/list", h.MembersHandler),

    # 把组织下的用户移到另一组织之下
    (rf"/{base}/org/([a-f0-9]*)/user/([a-f0-9]*)/move/(\w*)", h.MovingHandler),
]
