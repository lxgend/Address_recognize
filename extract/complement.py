# coding=utf-8
import pandas as pd
from data_processor.data_clean import cols_norm
from parms import *

df_loc = pd.read_csv(os.path.join(PATH_DATA, 'location_map.csv'), dtype=object, encoding='utf-8')
tag_list = [COL_PROV, COL_CITY, COL_DIST, COL_ST, COL_VIL]


# def norm_map(df):
#     for col in tag_list:
#         mask = (df[col] != UNK)
#         df_tmp = df_loc.drop_duplicates([col], keep='last')
#
#
#         def func(row):
#
#
#         df.loc[mask: col] = df.loc[mask: col].apply(
#             lambda x: df_tmp.loc[df_tmp[col + '_norm'] == x, col] if x in df_tmp[col + '_norm'].unique() else x, axis=1)
#     return df


def prov_complement(df):
    # 补全prov
    df_tmp = df_loc.drop_duplicates([COL_CITY], keep='last')
    mask = (df[COL_PROV] == UNK) & (df[COL_CITY] != UNK)
    df.loc[mask, COL_PROV] = df.loc[mask, COL_CITY].map(df_tmp.set_index(COL_CITY)[COL_PROV])
    df[COL_PROV] = df[COL_PROV].fillna(UNK)

    mask = (df[COL_PROV] == UNK) & (df[COL_CITY] != UNK)
    df.loc[mask, COL_PROV] = df.loc[mask, COL_CITY].map(df_tmp.set_index(COL_CITY + '_norm')[COL_PROV])
    df[COL_PROV] = df[COL_PROV].fillna(UNK)

    return df


def complement_middle(df, col_sup, col_sub, col_mid):
    col_tmp = 'tmp'
    # 通过两边补中间
    mask = (df[col_mid] == UNK) & (df[col_sup] != UNK) & (df[col_sub] != UNK)

    df_loc[col_tmp] = df_loc[col_sup].str.cat(df_loc[col_sub])
    df_loc_idx = df_loc.drop_duplicates([col_tmp], keep='last')

    df[col_tmp] = df[col_sup].str.cat(df[col_sub])
    df.loc[mask, col_mid] = df.loc[mask, col_tmp].map(df_loc_idx.set_index(col_tmp)[col_mid])

    mask = df[col_mid].isnull()
    df_loc[col_tmp] = df_loc[col_sup + '_norm'].str.cat(df_loc[col_sub])
    df_loc_idx = df_loc.drop_duplicates([col_tmp], keep='last')
    df.loc[mask, col_mid] = df.loc[mask, col_tmp].map(df_loc_idx.set_index(col_tmp)[col_mid])
    df[col_mid] = df[col_mid].fillna(UNK)

    df = df.drop([col_tmp], axis=1)
    return df


def complement_stgy(df):
    df = cols_norm(df=df, cols=tag_list)
    df = prov_complement(df)

    # 补全city
    df = complement_middle(df=df, col_sup=COL_PROV, col_sub=COL_DIST, col_mid=COL_CITY)
    df = complement_middle(df=df, col_sup=COL_PROV, col_sub=COL_ST, col_mid=COL_CITY)

    # 补全dc
    df = complement_middle(df=df, col_sup=COL_PROV, col_sub=COL_ST, col_mid=COL_DIST)
    df = complement_middle(df=df, col_sup=COL_CITY, col_sub=COL_ST, col_mid=COL_DIST)
    df = complement_middle(df=df, col_sup=COL_CITY, col_sub=COL_VIL, col_mid=COL_DIST)

    # 补全 st
    df = complement_middle(df=df, col_sup=COL_CITY, col_sub=COL_VIL, col_mid=COL_ST)
    df = complement_middle(df=df, col_sup=COL_DIST, col_sub=COL_VIL, col_mid=COL_ST)
    return df


def sql_complement(df):
    from sqlalchemy import create_engine
    engine = create_engine('sqlite:///' + PATH_DATA + '/data.sqlite')
    df_tmp = pd.read_sql_query(COL_PROV, engine)

    mask = (df[COL_PROV] == UNK) & (df[COL_CITY] != UNK)
    mask = (df[COL_PROV] != UNK) & (df[COL_CITY] == UNK) & (df[COL_DIST] == UNK)
