# coding:utf-8

from webmother.db import mongo as db
from tweb.error_exception import ErrException, ERROR
from tweb import time
from bson.objectid import ObjectId
from webmother.service import ctrl_catalog, ctrl_org
from webmother.service.passport import Passport


def passport_create(cid, oid, pp_meta, *auth_args):
    """
    分类与组织建立绑定关系
    :param cid: 分类节点ID
    :param oid: 组织ID
    :param pp_meta: 授权描述信息
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """
    c = ctrl_catalog.read(cid, *auth_args)

    # 授权检查
    pp = Passport().verify(*auth_args).operable(c.get('node'), 'passport_create')
    # END

    # 如果该组织已经在某级父目录中得到授权，无需重复授权
    node = c['node']
    cursor = db.catalog2org.find({'org': ObjectId(oid)}, {'org': 0})
    for item in cursor:
        cn = item['catalog_node']
        if node.find(cn) == 0:
            raise ErrException(ERROR.E40020, extra=f'org({oid}) has got passport at parent catalog({cn})')

    tmp_pp = Passport()
    # 如果没有设置权限描述对象，则默认所有授权处于关闭状态
    if pp_meta is not None and 'passport' in pp_meta:
        tmp_pp = tmp_pp.update(cid, oid, pp_meta['passport'], pp)

    now = time.millisecond()
    data = {
        "catalog": ObjectId(cid),
        "catalog_node": c['node'],
        "org": ObjectId(oid),
        "passport": tmp_pp.text,
        "created": now,
        "updated": now
    }

    db.catalog2org.insert_one(data)
    return _passport_read(cid, oid)


def passport_read(cid, oid, *auth_args):
    c = ctrl_catalog.read(cid, *auth_args)

    # 授权检查
    Passport().verify(*auth_args).operable(c.get('node'), 'passport_read')
    # END

    return _passport_read(cid, oid)


def _passport_read(cid, oid):
    c2o = db.catalog2org.find_one({'catalog': ObjectId(cid), 'org': ObjectId(oid)})
    if c2o is None:
        raise ErrException(ERROR.E40400)

    c2o['ppid'] = c2o.pop('_id').__str__()
    c2o['catalog'] = c2o['catalog'].__str__()
    c2o['org'] = ctrl_org._read(c2o['org'])
    c2o['passport'] = Passport(c2o['passport']).parse().json

    return c2o


def passport_update(cid, oid, pp_meta, *auth_args):
    """
    更新组织对分类以及分类下资源的授权
    :param cid: 分类节点ID
    :param oid: 组织ID
    :param pp_meta: 授权描述信息
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """
    c = ctrl_catalog.read(cid, *auth_args)

    # 授权检查
    pp = Passport().verify(*auth_args).operable(c.get('node'), 'passport_update')
    # END

    c2o = db.catalog2org.find_one({'catalog': ObjectId(cid), 'org': ObjectId(oid)})
    if c2o is None:
        raise ErrException(ERROR.E40400)

    if pp_meta is None or 'passport' not in pp_meta:
        raise ErrException(ERROR.E40000, extra='no body for passport meta object')

    c2o['passport'] = Passport(c2o.get('passport')).update(c['node'], oid, pp_meta['passport'], pp).text
    c2o['updated'] = time.millisecond()

    db.catalog2org.update_one({'_id': c2o['_id']}, {'$set': c2o})

    return _passport_read(cid, oid)


def passport_remove(cid, oid, *auth_args):
    """
    解除分类与组织的关系
    :param cid: 分类节点ID
    :param oid: 组织ID
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """
    c = ctrl_catalog.read(cid, *auth_args)

    # 授权检查
    pp = Passport().verify(*auth_args).operable(c.get('node'), 'passport_remove')
    # END

    # 将所有开关关闭，数值设为0，范围设为0~0
    Passport().update(c['node'], oid, {}, pp)

    db.catalog2org.delete_one({'catalog': ObjectId(cid), 'org': ObjectId(oid)})

    return {}


def passports_query(cid, *auth_args):
    """
    获取分类节点的被授权的组织列表
    :param cid:
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """
    c = ctrl_catalog.read(cid, *auth_args)

    # 授权检查
    Passport().verify(*auth_args).operable(c.get('node'), 'passport_read')
    # END

    cursor = db.catalog2org.find({'catalog': ObjectId(cid)}, {'catalog': 0})
    array = list()
    for item in cursor:
        item['ppid'] = item.pop('_id').__str__()
        item['org'] = ctrl_org._read(item['org'])
        item['passport'] = Passport(item['passport']).parse().json
        array.append(item)

    return array
