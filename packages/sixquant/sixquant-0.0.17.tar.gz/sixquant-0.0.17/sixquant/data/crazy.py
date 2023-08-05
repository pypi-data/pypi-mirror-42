# -*- coding: UTF-8 -*-

import pandas as pd

from ..constants import CRAZY_HEATMAP_URL, CRAZY_DAILY_ZT, CRAZY_DAILY_ZB, \
    CRAZY_DAILY_LEADERS, CRAZY_DAILY_LEADERS_TOP
from ..utils.request import request_json_obj_date


def get_crazy_heatmap(dt=None, zt=True):
    """
    打板热图
    """
    if zt == False:
        return request_json_obj_date(CRAZY_HEATMAP_URL, dt, "?zt=0")
    return request_json_obj_date(CRAZY_HEATMAP_URL, dt)


def get_crazy_zt_list(dt=None, fields=['price', 'pt', 'turnover',
                                       'major_money', 'money', 'buy_money',
                                       'state', 'reason', 'crazy_time',
                                       'continues', 'times', 'days']):
    """
    实时
    """
    rs = request_json_obj_date(CRAZY_DAILY_ZT, dt)
    if rs is None:
        rs = []

    df = pd.DataFrame(rs, columns=['code', 'price', 'pt', 'turnover',
                                   'major_money', 'money', 'buy_money',
                                   'state', 'reason',
                                   'crazy_time', 'crash_time',
                                   'continues', 'times', 'days'
                                   ])
    df.set_index('code', inplace=True)
    df[['price', 'pt', 'turnover', 'major_money', 'buy_money']] = df[
        ['price', 'pt', 'turnover', 'major_money', 'buy_money']].astype(float)
    df[['continues', 'times', 'days']] = df[['continues', 'times', 'days']].astype(int)
    df.index.name = None

    return df[fields].copy()


def get_crazy_zb_list(dt=None, fields=['price', 'pt', 'turnover', 'major_money', 'crash_time']):
    """
    实时
    """
    rs = request_json_obj_date(CRAZY_DAILY_ZB, dt)
    if rs is None:
        rs = []

    df = pd.DataFrame(rs, columns=['code', 'price', 'pt', 'turnover',
                                   'major_money', 'money', 'buy_money',
                                   'state', 'reason',
                                   'crazy_time', 'crash_time',
                                   'continues', 'times', 'days'
                                   ])
    df.set_index('code', inplace=True)
    df[['price', 'pt', 'turnover', 'major_money']] = df[
        ['price', 'pt', 'turnover', 'major_money']].astype(float)
    df.index.name = None

    return df[fields].copy()


def get_crazy_leaders(dt=None, fields=None, topN=None):
    """
    龙头
    :return:
        DataFrame
            category      板块标识
            category_name 板块名称
            zt            板块涨停数量
            categories    所属板块
            code          股票代码
            name          股票名称
            rank          排名龙几
            state         连板状态
            style         风格：游资
            time          涨停时间
            type          涨停类型
            reason        涨停原因
            turnover      换手率( %)
            buy           当前封单（手）
            buy_money     当前封单（万元）
            high_money    高位封单（万元），8 % 以上位置成交
    """
    rs = request_json_obj_date(CRAZY_DAILY_LEADERS if topN is None else CRAZY_DAILY_LEADERS_TOP, dt)
    if rs is None:
        rs = []

    df = pd.DataFrame(rs, columns=['category', 'category_name', 'zt', 'categories',
                                   'code', 'name',
                                   'rank', 'state', 'style',
                                   'time', 'type', 'reason',
                                   'turnover', 'buy', 'buy_money', 'high_money'
                                   ])
    df.set_index('category', inplace=True)
    df[['turnover', 'buy_money', 'high_money']] = df[['turnover', 'buy_money', 'high_money']].astype(float)
    df[['zt', 'rank', 'buy']] = df[['zt', 'rank', 'buy']].astype(int)
    df.index.name = None

    return df if fields is None else df[fields].copy()


def get_crazy_leaders_top(dt=None, fields=None):
    return get_crazy_leaders(dt=dt, fields=fields, topN=3)
