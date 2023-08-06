#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019/2/20
# @Author  : beequants-nick

import time
from cacheout import Cache
from qbase.common import dbsql

cache = Cache(maxsize=64, ttl=60 * 60, timer=time.time, default=None)  # defaults


def get_kline_list(start_time, end_time, symbol, period, num=None):
    cache_key = start_time+'_'+end_time+'_'+symbol+'_'+period
    if cache.has(cache_key):
        return cache.get(cache_key)
    else:
        cache_value = dbsql.get_kline_list(start_time, end_time, symbol, period, num)
        cache.set(cache_key, cache_value)
        return cache_value


