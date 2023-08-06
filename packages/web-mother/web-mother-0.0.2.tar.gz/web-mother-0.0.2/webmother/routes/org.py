# coding=utf-8

import config
from webmother.http_handler import org_handler as h

base = '{}/{}/org'.format(config.VER, config.DOMAIN)
routes = [
    # 组织的增删改查
    (rf"/{base}/([a-f0-9]*)", h.OrgHandler),
    # 组织的状态操作
    (rf"/{base}/([a-f0-9]*)/do/(\w*)", h.StatusHandler),

    # 查询子节点
    (rf"/{base}/([a-f0-9]*)/children", h.ChildrenHandler),

    # 移动节点
    (rf"/{base}/([a-f0-9]*)/move/([a-f0-9]*)", h.MovingHandler),

    # 查询组织拥有哪些资源的许可证/通行证，许可范围有多大
    (rf"/{base}/([a-f0-9]*)/passports", h.OurPassportsHandler),

]
