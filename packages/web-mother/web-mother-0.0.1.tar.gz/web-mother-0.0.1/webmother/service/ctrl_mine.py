# coding:utf-8

from webmother.db import mongo as db
from bson.objectid import ObjectId
from webmother.service.identity import Identity
from webmother.service import ctrl_org


def my_identities(uid, access_token):
    """
    获取我的组织列表
    :param uid:
    :param access_token:
    :return:
    """
    cursor = db.org2user.find({'user.uid': ObjectId(uid)}, {'user': 0})

    array = list()
    for item in cursor:
        idt = Identity(item['identity']).parse()
        item['signed_identity'] = idt.signed(item['org_node'], uid, access_token)
        item['identity'] = idt.json

        item['open_id'] = item.pop('_id').__str__()
        item['org'] = ctrl_org._read(item['org'])

        array.append(item)

    return array
