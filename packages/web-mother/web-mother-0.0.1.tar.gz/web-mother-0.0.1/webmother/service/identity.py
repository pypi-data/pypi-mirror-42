# coding:utf-8

from tweb.license import License
import config


class Identity(License):

    def __init__(self, text=None):
        super(Identity, self).__init__(text)

        # 共40个开关可用
        self.SWITCH = [
            "create",  # 0
            "read",
            "update",
            "remove",
            "submit",
            "audit",
            "reject",
            "activate",
            "deactivate",
            "NA",
            "NA",  # 10
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "member_create",  # 20
            "member_read",
            "member_update",
            "member_remove",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",  # 30
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA"
        ]
        # 共10个数值域可用
        self.NUMBER = [
            "NA",  # 0
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA"
        ]
        # 共10个范围域可用
        self.RANGE = [
            "NA",  # 0
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA"
        ]

        self.authority = 'org'  # 发证机构代码
        self.secret = config.TornadoSettings['cookie_secret']  # 发证机构代签名密码
