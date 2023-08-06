# coding:utf-8

from webmother.db import mongo as db
from tweb.json_util import filter_keys
from tweb.error_exception import ErrException, ERROR
from tweb import time
from bson.objectid import ObjectId
from webmother.service.identity import Identity
import re
from webmother.service import ctrl_catalog
from webmother.service.passport import Passport


# 组织节点状态以及状态迁移定义
class Status:
    removed = -10  # 已删除
    editing = 0  # 编辑中
    auditing = 10  # 待审(审核中)
    sleeping = 20  # 休眠中
    activated = 30  # 已激活

    status_map = {
        editing: {'submit': auditing, 'remove': removed},
        auditing: {'reject': editing, 'audit': sleeping, 'remove': removed},
        sleeping: {'activate': activated, 'remove': removed},
        activated: {'deactivate': sleeping}
    }

    @staticmethod
    def trans(cur_status, action):
        """
        在当前状态，进行操作将会得到新的状态
        :param cur_status: 当前状态
        :param action: 操作名称
        :return: 新的状态
        """

        valid_actions = Status.status_map.get(cur_status)
        if valid_actions is None:
            raise ErrException(ERROR.E40022, extra=f'current status is {cur_status}, forbid change status')

        new_status = valid_actions.get(action)
        if new_status is None:
            raise ErrException(ERROR.E40022, extra=f'current status is {cur_status}, wrong action [{action}]')

        return new_status


def create(oid, org_meta, *auth_args):
    """
    向oid节点中添加org_meta描述的子节点
    """
    o = _read(oid)

    # 授权检查
    Identity().verify(*auth_args).operable(o.get('node'), 'create')
    # END

    name = org_meta.pop('name').lower()
    if not re.match(r'^[\w]{0,19}$', name):
        raise ErrException(ERROR.E40000, extra='name should be letter, number, _, and beginning with letter')

    parent_node = o['node']

    org_meta['node'] = f'{parent_node}/{name}'
    org_meta['parent'] = ObjectId(oid)

    if db.org.find_one({'node': org_meta['node'], 'status': {'$gte': 0}}) is not None:
        raise ErrException(ERROR.E40020)

    org_meta['status'] = Status.editing
    now = time.millisecond()
    org_meta['created'] = now
    org_meta['updated'] = now

    result = db.org.insert_one(org_meta)
    return _read(result.inserted_id)


def read(oid, *auth_args):
    o = _read(oid)

    # 授权检查
    Identity().verify(*auth_args).operable(o.get('node'), 'read')
    # END

    return o


def _read(oid, raw=False):
    o = db.org.find_one({'_id': ObjectId(oid), 'status': {'$gte': 0}})
    if o is None:
        raise ErrException(ERROR.E40400, extra=f'the org({oid}) not existed')

    if not raw:
        o['oid'] = o.pop('_id').__str__()
        if 'parent' in o:
            o['parent'] = o['parent'].__str__()

    return o


def update(oid, org_meta, *auth_args):
    """
    :param oid: 组织节点id
    :param org_meta: 组织信息
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """
    o = _read(oid)

    # 授权检查
    Identity().verify(*auth_args).operable(o.get('node'), 'update')
    # END

    if o['status'] not in (Status.editing, Status.auditing, Status.sleeping, Status.activated):
        raise ErrException(ERROR.E40021)

    new_data = filter_keys(org_meta, {
        'display': 1,
        'icon': 1
    })

    new_data['status'] = Status.editing
    new_data['updated'] = time.millisecond()

    db.org.update_one({'_id': ObjectId(oid)}, {'$set': new_data})
    return _read(oid)


def change_status(oid, action, *auth_args):
    """
    :param oid: 组织节点id
    :param action: 操作（提交，过审，驳回，激活，去激活，删除等）
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """
    o = _read(oid)

    # 授权检查
    Identity().verify(*auth_args).operable(o.get('node'), action)
    # END

    cur_status = o.get('status')
    new_status = Status.trans(cur_status, action)

    new_data = {
        'status': new_status,
        'updated': time.millisecond()
    }

    db.org.update_one({'_id': ObjectId(oid)}, {'$set': new_data})

    return {'id': oid, 'status': new_status, 'old_status': cur_status}


def children(oid, *auth_args):
    o = _read(oid)

    # 授权检查
    Identity().verify(*auth_args).operable(o.get('node'), 'read')
    # END

    cursor = db.org.find({'parent': ObjectId(oid), 'status': {'$gte': 0}})
    array = list()
    for item in cursor:
        item['oid'] = item.pop('_id').__str__()
        if 'parent' in item:
            item['parent'] = item['parent'].__str__()

        array.append(item)
    return array


def move(oid, oid_to, *auth_args):
    """
    把oid标示的节点移到oid_to标示的节点之下
    :param oid: 被移动节点ID
    :param oid_to: 新的父节点ID
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """
    o = _read(oid, raw=True)
    o_to = _read(oid_to, raw=True)

    if o['parent'] == oid_to:
        raise ErrException(ERROR.E40000, extra='the same node, not need move')

    # 授权检查
    Identity().verify(*auth_args).operable(o['node'], 'remove', 'member_update')
    Identity().verify(*auth_args).operable(o_to['node'], 'create', 'member_create')
    # END

    if o['status'] not in (Status.editing, Status.auditing, Status.sleeping, Status.activated):
        raise ErrException(ERROR.E40021)

    now = time.millisecond()

    name = o['node'].split('/').pop()
    node = f'{o_to["node"]}/{name}'

    if db.org.find_one({'node': node, 'status': {'$gte': 0}}) is not None:
        raise ErrException(ERROR.E40020)

    tmp_o = {
        'node': node,
        'parent': ObjectId(oid_to),
        'status': Status.auditing,
        'updated': now
    }

    tmp_o2u = {
        'org_node': node,
        'updated': now
    }

    # 还需要同步修改与此节点相关catalog2org记录，因为里面记录了节点的node值。多个地方更新需要用到事务！
    with db.start_session() as s:
        s.start_transaction()
        db.org2user.update_many({'org': ObjectId(oid)}, {'$set': tmp_o2u})
        db.org.update_one({'_id': ObjectId(oid)}, {'$set': tmp_o})
        s.commit_transaction()

    return _read(oid)


def our_passports(oid, *auth_args):
    """
    获取组织拥有授权的分类节点列表(需有该组织的会员资格)
    :param oid: 组织ID
    :param auth_args: 鉴权参数：(signed, nonce), 即("签名的授权字符串", "临时一致性标示，需与生成签名时使用的nonce相同")
    :return:
    """

    nonce = auth_args[1]

    o = _read(oid)

    # 授权检查, 检查用户是否属于该组织，或者该组织的父组织，否则没有权限查询组织拥有的分类节点
    Identity().verify(*auth_args).operable(o.get('node'), 'member_read')
    # END

    cursor = db.catalog2org.find({'org': ObjectId(oid)}, {'org': 0})

    array = list()
    for item in cursor:
        pp = Passport(item['passport']).parse()
        item['signed_passport'] = pp.signed(item['catalog_node'], oid, nonce)
        item['passport'] = pp.json

        item['ppid'] = item.pop('_id').__str__()
        item['catalog'] = ctrl_catalog._read(item['catalog'])

        array.append(item)

    return array
