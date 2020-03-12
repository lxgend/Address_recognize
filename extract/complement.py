# coding=utf-8
import pandas as pd
from sqlalchemy import create_engine

from parms import *

engine = create_engine('sqlite:///' + PATH_DATA + '/data.sqlite')

tag_list = [COL_PROV, COL_CITY, COL_DIST, COL_ST, COL_VIL]

def geo_complement(df, col_prov, col_city):
    df_pc = sql

    mask = (df[col_prov] == UNK) & (df[col_city] != UNK)
    df.loc[mask, col_prov] = df.loc[mask, col_city].map(df_pc.set_index('city')['prov'])

    df.update(df[[col_prov, col_city]]).fillna(UNK)

    return df


def sql_complement(df):



    df_tmp = pd.read_sql_query(COL_PROV, engine)

    mask = (df[COL_PROV] == UNK) & (df[COL_CITY] != UNK)


    mask = (df[COL_PROV] != UNK) & (df[COL_CITY] == UNK ) & (df[COL_DIST] == UNK )


