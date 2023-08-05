# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：    zssdb.py
   Author :       Zhang Fan
   date：         2019/1/10
   Description :
-------------------------------------------------
"""
__author__ = 'Zhang Fan'

import pyssdb
from zretry import retry

_retry_func_list = []


def _except_retry(func):
    _retry_func_list.append(func.__name__)
    return func


class ssdb_inst():
    def __init__(self, host: str or list, port=8888, cluster=False, collname='test', password=None,
                 decode_responses=True,
                 retry_interval=1, max_attempt_count=5,
                 **kw):
        '''
        创建一个ssdb客户端
        :param host: 服务器ip
        :param port: 服务器端口
        :param cluster: 是否为集群
        :param collname: 文档名
        :param password: 密码
        :param decode_responses: 是否自动解码, 默认为utf8
        :param retry_interval: 尝试等待时间
        :param max_attempt_count: 最大尝试次数
        :param kw: 其他参数
        '''
        if cluster:
            raise Exception('暂不支持集群连接')
        else:
            self._conn = pyssdb.Client(host=host, port=port, **kw)

        if password:
            self._conn.auth(password)

        self.decode_responses = decode_responses
        self.collname = collname

        for retry_func_name in _retry_func_list:
            func = getattr(self, retry_func_name)
            decorator = retry(interval=retry_interval, max_attempt_count=max_attempt_count)(func)
            setattr(self, retry_func_name, decorator)

    def change_coll(self, collname):
        self.collname = collname

    # region 其他操作
    @_except_retry
    def _get_names(self, func, limit=65535):
        return self._result_list_handler(func('', '', limit))

    @_except_retry
    def _get_names_iter(self, func, batch_size=100):
        start = ''
        while True:
            datas = func(start, '', batch_size)
            if not datas:
                return

            for name in datas:
                yield self._result_handler(name)

            start = datas[-1]

    # endregion

    # region 数据处理
    def _result_handler(self, result):
        return result.decode('utf8') if self.decode_responses and isinstance(result, bytes) else result

    def _result_list_handler(self, result):
        return [self._result_handler(value) for value in result]

    def _list_to_mapping(self, result):
        result_dict = dict()
        for index in range(0, len(result), 2):
            k = self._result_handler(result[index])
            v = self._result_handler(result[index + 1])
            result_dict[k] = v
        return result_dict

    def _mapping_to_list(self, mapping: dict):
        values = list()
        for k, v in mapping.items():
            values.append(k)
            values.append(v)
        return values

    # endregion

    # region 列表操作
    @_except_retry
    def list_push(self, *values, front=True):
        # 放入一个字符串, 返回队列总数
        if front:
            return self._conn.qpush_front(self.collname, *values)
        else:
            return self._conn.qpush_back(self.collname, *values)

    @_except_retry
    def list_pop(self, front=True):
        # 无数据时返回None
        if front:
            return self._result_handler(self._conn.qpop_front(self.collname))
        else:
            return self._result_handler(self._conn.qpop_back(self.collname))

    @_except_retry
    def list_count(self, collname=None):
        return self._conn.qsize(collname or self.collname)

    # @_except_retry
    def list_get_datas(self, collname=None, limit=65535):
        # 返回一个list, 包含ssdb中该list的所有数据
        return self._result_list_handler(self._conn.qrange(collname or self.collname, 0, limit))

    @_except_retry
    def list_iter(self, collname=None, batch_size=100):
        # 迭代返回一个list中所有的数据
        collname = collname or self.collname
        start = 0
        while True:
            datas = self._conn.qrange(collname, start, batch_size)
            if not datas:
                return

            for data in datas:
                yield self._result_handler(data)

            start += len(datas)

    @_except_retry
    def list_names(self, limit=65535):
        # 返回所有的list文档名
        return self._get_names(self._conn.qlist, limit)

    @_except_retry
    def list_names_iter(self, batch_size=100):
        # 迭代返回所有的list文档名
        yield from self._get_names_iter(self._conn.qlist, batch_size)

    @_except_retry
    def list_clear(self, collname=None):
        # 删除这个list, 返回是否成功
        return self._conn.qclear(collname or self.collname) == b'1'

    # endregion

    # region 集合操作
    @_except_retry
    def set_add(self, key, score: int = 1):
        # 新增返回1, 修改返回0
        return self._conn.zset(self.collname, key, score)

    @_except_retry
    def set_add_values(self, mapping: dict or list or tuple or set, score=1):
        # 设置多个数据, key作为键, value作为权重, 返回新增多少条数据
        if isinstance(mapping, dict):
            value = self._mapping_to_list(mapping)
        elif isinstance(mapping, (list, tuple, set)):
            value = list()
            for key in mapping:
                value.append(key)
                value.append(score)
        else:
            raise TypeError('mapping must be of type (dict, list, tuple, set)')
        return self._conn.multi_zset(self.collname, *value)

    @_except_retry
    def set_remove(self, *keys):
        # 删除多个值, 返回删除的数量
        return self._conn.multi_zdel(self.collname, *keys)

    @_except_retry
    def set_count(self, collname=None):
        return self._conn.zsize(collname or self.collname)

    @_except_retry
    def set_has(self, value):
        # 是否存在某个值
        return self._conn.zexists(self.collname, value) == b'1'

    @_except_retry
    def set_get(self, key, default=None):
        # 返回一个数据的权重值, 权重值为整数
        return self._conn.zget(self.collname, key) or default

    @_except_retry
    def set_keys(self, collname=None, limit=65535):
        # 返回一个列表, 包含set中所有的key
        return self._result_list_handler(self._conn.zkeys(collname or self.collname, '', '', '', limit))

    @_except_retry
    def set_get_values(self, *keys):
        # 获取多个数据的权重, 返回一个字典
        return self._list_to_mapping(self._conn.multi_zget(self.collname, *keys))

    @_except_retry
    def set_get_datas(self, collname=None, limit=65535):
        # 返回一个dict, 包含ssdb中该set的所有数据
        return self._list_to_mapping(self._conn.zrange(collname or self.collname, 0, limit))

    @_except_retry
    def set_iter(self, collname=None, batch_size=100):
        # 迭代返回一个set中所有的数据, 每次返回的是一个元组(键, 权重)
        collname = collname or self.collname
        start = 0
        while True:
            datas = self._conn.zrange(collname, start, batch_size)
            if not datas:
                return

            for index in range(0, len(datas), 2):
                k = self._result_handler(datas[index])
                v = int(self._result_handler(datas[index + 1]))
                yield k, v

            start += len(datas) // 2

    @_except_retry
    def set_names(self, limit=65535):
        # 返回所有的set文档名
        return self._get_names(self._conn.zlist, limit)

    @_except_retry
    def set_names_iter(self, batch_size=100):
        # 迭代返回所有的set文档名
        yield from self._get_names_iter(self._conn.zlist, batch_size)

    @_except_retry
    def set_clear(self, collname=None):
        # 删除这个set, 返回是否成功
        return self._conn.zclear(collname or self.collname) == b'1'

    # endregion

    # region 哈希操作
    @_except_retry
    def hash_set(self, key, value):
        # 设置数据, 返回0表示修改,返回1表示创建
        return int(self._conn.hset(self.collname, key, value))

    @_except_retry
    def hash_set_values(self, mapping: dict):
        # 设置多个数据, 返回成功数量
        values = self._mapping_to_list(mapping)
        return self._conn.multi_hset(self.collname, *values)

    @_except_retry
    def hash_get(self, key):
        # 获取一个key的值, 失败返回None
        return self._result_handler(self._conn.hget(self.collname, key))

    @_except_retry
    def hash_get_values(self, *keys):
        # 获取多个key的值, 返回一个字典
        return self._list_to_mapping(self._conn.multi_hget(self.collname, *keys))

    @_except_retry
    def hash_remove(self, *keys):
        # 删除多个键, 返回实际删除数量
        return self._conn.multi_hdel(self.collname, *keys)

    @_except_retry
    def hash_incrby(self, key, amount=1):
        # 自增, 返回自增后的整数
        return self._conn.hincr(self.collname, key, amount)

    @_except_retry
    def hash_count(self, collname=None):
        # 返回元素数量
        return self._conn.hsize(collname or self.collname)

    @_except_retry
    def hash_has(self, key):
        # 是否存在某个键
        return self._conn.hexists(self.collname, key) == b'1'

    @_except_retry
    def hash_keys(self, collname=None, limit=65535):
        # 返回一个列表, 包含hash中所有的key
        return self._result_list_handler(self._conn.hkeys(collname or self.collname, '', '', limit))

    @_except_retry
    def hash_get_datas(self, collname=None):
        # 返回一个字典, 一次性获取该hash中的所有数据
        return self._list_to_mapping(self._conn.hgetall(collname or self.collname))

    @_except_retry
    def hash_iter(self, collname=None, batch_size=100):
        # 迭代返回一个hash中所有的数据, 每次返回的是一个元组(键, 值)
        collname = collname or self.collname
        start = ''
        while True:
            datas = self._conn.hscan(collname, start, '', batch_size)
            if not datas:
                return

            for index in range(0, len(datas), 2):
                k = self._result_handler(datas[index])
                v = self._result_handler(datas[index + 1])
                yield k, v

            start = datas[-2]

    @_except_retry
    def hash_names(self, limit=65535):
        # 返回所有的hash文档名
        return self._get_names(self._conn.hlist, limit)

    @_except_retry
    def hash_names_iter(self, batch_size=100):
        # 迭代返回所有的hash文档名
        yield from self._get_names_iter(self._conn.hlist, batch_size)

    @_except_retry
    def hash_clear(self, collname=None):
        # 删除这个hash, 返回是否成功
        return self._conn.hclear(collname or self.collname) == b'1'

    # endregion
