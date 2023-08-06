# coding:utf-8

from webmother.db import mongo as db
from tweb.error_exception import ErrException, ERROR
from tweb import time
from bson.objectid import ObjectId
from webmother.service.identity import Identity
from webmother.service import ctrl_org


def member_create(oid, uid, mmb_meta, *auth_args):
    """
    向组织中添加用户
    :param oid: 组织ID
    :param uid: 用户ID
    :param mmb_meta: 会员元数据，包含用户信息以及授权信息
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """
    o = ctrl_org._read(oid)

    # 授权检查
    idt = Identity().verify(*auth_args).operable(o.get('node'), 'member_create')
    # END

    node = o['node']
    cursor = db.org2user.find({'user.uid': ObjectId(uid)}, {'user': 0})
    for item in cursor:
        other = item['org_node']
        # 如果已经加入到其某级父组织，则无需再加入
        if node.find(other) == 0:
            raise ErrException(ERROR.E40020, extra=f'user({uid}) have been in org({other})')

        # 如果已经加入到其某级子组织，则移动到该级组织
        if other.find(node) == 0:
            return move(item['org'], uid, oid, *auth_args)

    tpm_idt = Identity().update(o['node'], uid, mmb_meta.get('identity'), idt)

    user = mmb_meta.get('user')
    if user is None:
        user = {'nickname': 'Unknown'}

    user['uid'] = ObjectId(uid)

    db.org2user.insert_one({
        "org": ObjectId(oid),
        "org_node": o['node'],
        "identity": tpm_idt.text,
        "user": user,
        "created": time.millisecond()
    })

    return _member_read(oid, uid)


def member_read(oid, uid, *auth_args):
    o = ctrl_org.read(oid, *auth_args)

    # 授权检查
    Identity().verify(*auth_args).operable(o.get('node'), 'member_read')
    # END

    return _member_read(oid, uid)


def _member_read(oid, uid):
    o2u = db.org2user.find_one({'org': ObjectId(oid), 'user.uid': ObjectId(uid)}, {'org': 0})
    if o2u is None:
        raise ErrException(ERROR.E40400)

    o2u['open_id'] = o2u.pop('_id').__str__()
    o2u['user']['uid'] = o2u['user']['uid'].__str__()
    o2u['identity'] = Identity(o2u['identity']).parse().json

    return o2u


def member_update(oid, uid, mmb_meta, *auth_args):
    o = ctrl_org.read(oid, *auth_args)

    # 授权检查
    idt = Identity().verify(*auth_args).operable(o.get('node'), 'member_update')
    # END

    o2u = db.org2user.find_one({'org': ObjectId(oid), 'user.uid': ObjectId(uid)})
    if o2u is None:
        raise ErrException(ERROR.E40400)

    temp = dict()

    if 'identity' in mmb_meta:
        temp['identity'] = Identity().update(o['node'], uid, mmb_meta.get('identity'), idt).text

    if 'user' in mmb_meta:
        user = mmb_meta.get('user')
        if 'uid' in user:
            user.pop('uid')
        u = o2u['user']
        u.update(user)
        temp['user'] = u

    if len(temp) > 0:
        temp['updated'] = time.millisecond()
        db.org2user.update_one({'_id': o2u['_id']}, {'$set': temp})

    return _member_read(oid, uid)


def member_remove(oid, uid, *auth_args):
    """
    从组织中移除用户
    :param oid: 组织ID
    :param uid: 用户ID
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """
    o = ctrl_org._read(oid)

    # 授权检查
    Identity().verify(*auth_args).operable(o.get('node'), 'member_remove')
    # END

    db.org2user.delete_one({'org': ObjectId(oid), 'user.uid': ObjectId(uid)})

    return {}


def move(oid, uid, oid_to, *auth_args):
    """
    把oid组织下的uid用户移到oid_to标示的组织之下
    :param oid: 原组织ID
    :param uid: 用户ID
    :param oid_to: 新组织ID
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """
    o = ctrl_org._read(oid, raw=True)
    o_to = ctrl_org._read(oid_to, raw=True)

    if oid == oid_to:
        raise ErrException(ERROR.E40000, extra='the same node, not need move')

    # 授权检查
    Identity().verify(*auth_args).operable(o['node'], 'member_remove')
    Identity().verify(*auth_args).operable(o_to['node'], 'member_create')
    # END

    tmp_p = {
        'org': ObjectId(oid_to),
        'org_node': o_to['node'],
        'updated': time.millisecond()
    }

    db.org2user.update_one({'org': ObjectId(oid), 'user.uid': ObjectId(uid)}, {'$set': tmp_p})

    return _member_read(oid_to, uid)


def members_query(oid, *auth_args):
    o = ctrl_org._read(oid)

    # 授权检查
    Identity().verify(*auth_args).operable(o.get('node'), 'member_read')
    # END

    cursor = db.org2user.find({'org': ObjectId(oid)}, {'org': 0})

    array = list()
    for item in cursor:
        item['open_id'] = item.pop('_id').__str__()
        item['user']['uid'] = item['user']['uid'].__str__()
        item['identity'] = Identity(item['identity']).parse().json
        array.append(item)

    return array
