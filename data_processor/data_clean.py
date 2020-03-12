# coding=utf-8
import unicodedata

from parms import *


def input_normalize(df, col_origin):
    # 全角转半角
    df[COL_INPUT_NORM] = df[col_origin].apply(lambda x: unicodedata.normalize('NFKC', str(x)))

    # 保留汉字，字母，数字，逗号，句号
    df[COL_INPUT_NORM] = df[COL_INPUT_NORM].str.replace(r'[^(\u4e00-\u9fa5a-zA-Z0-9)]', '')

    return df, COL_INPUT_NORM


def suffix_clean(df, col_raw, col_norm):
    df[col_norm] = df[col_raw].str.replace('省', '')
    df[col_norm] = df[col_norm].str.replace('壮族自治区', '')
    df[col_norm] = df[col_norm].str.replace('回族自治区', '')
    df[col_norm] = df[col_norm].str.replace('维吾尔自治区', '')
    df[col_norm] = df[col_norm].str.replace('自治区', '')
    df[col_norm] = df[col_norm].str.replace('特别行政区', '')
    return df
