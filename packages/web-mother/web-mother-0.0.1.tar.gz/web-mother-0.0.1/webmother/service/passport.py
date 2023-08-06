# coding:utf-8

from tweb.license import License
import config


class Passport(License):

    def __init__(self, text=None):
        super(Passport, self).__init__(text)

        # 共64个开关可用
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
            "passport_create",  # 20
            "passport_read",
            "passport_update",
            "passport_remove",
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
            "NA",
            "element_create",  # 40
            "element_read",
            "element_update",
            "element_remove",
            "element_submit",
            "element_audit",
            "element_reject",
            "element_activate",
            "element_deactivate",
            "NA",
            "NA",  # 50
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",
            "NA",  # 60
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

        self.authority = 'catalog'  # 发证机构代码
        self.secret = config.TornadoSettings['cookie_secret']  # 发证机构代签名密码
