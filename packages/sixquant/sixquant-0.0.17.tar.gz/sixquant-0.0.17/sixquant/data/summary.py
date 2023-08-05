# coding=utf-8

import pandas as pd

from ..constants import SUMMARY_LIST_URL
from ..utils.request import request_json_obj

"""
股票概述信息
"""


def get_summary_list(ys=None,
                     fields=['rank', 'financial_rank',
                             'np', 'npr',
                             'npg', 'npg_s2', 'npg_y1', 'npg_y2', 'npg_y3',
                             'nr',
                             'nrg', 'nrg_s2', 'nrg_y1', 'nrg_y2', 'nrg_y3',
                             'pe_ttm', 'roe_ttm']):
    """
    得到股票基本信息列表
    :return: DataFrame
        code            股票代码
        rank            综合排名
        financial_rank  财务排名
        np              扣非净利润：上季（亿）
        npr             扣非净利润率：上季
        npg             扣非净利润：上季同比增长
        npg_s2          扣非净利润：上上季同比增长
        npg_y1          扣非净利润：去年同比增长
        npg_y2          扣非净利润：前年同比增长
        npg_y3          扣非净利润：大前年同比增长
        nr              净营收：上季（亿）
        nrg             净营收：上季同比增长
        nrg_s2          净营收：上上季同比增长
        nrg_y1          净营收：去年同比增长
        nrg_y2          净营收：前年同比增长
        nrg_y3          净营收：大前年同比增长
        pe_ttm          市盈率 TTM
        roe_ttm         净资产收益率 ROE TTM
    """
    url = SUMMARY_LIST_URL
    if ys is not None:
        url += '/' + ys
    rs = request_json_obj(url)
    if rs is None:
        rs = []

    df = pd.DataFrame(rs, columns=['code',
                                   'rank', 'financial_rank',
                                   'np', 'npr',
                                   'npg', 'npg_s2', 'npg_y1', 'npg_y2', 'npg_y3',
                                   'nr',
                                   'nrg', 'nrg_s2', 'nrg_y1', 'nrg_y2', 'nrg_y3',
                                   'pe_ttm', 'roe_ttm'])
    df.set_index('code', inplace=True)
    df = df.astype(float)
    df[['rank', 'financial_rank']] = df[['rank', 'financial_rank']].astype(int)
    df.index.name = None

    if fields is not None:
        return df[fields].copy()

    return df
