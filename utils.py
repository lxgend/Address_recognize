# coding=utf-8
import pandas as pd

from data_processor.data_clean import suffix_clean
from parms import *

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

COL_NM = 'name'
COL_NM_NORM = 'name_norm'

drop_word = ['省直辖县级行政区划', '自治区直辖县级行政区划', '市辖区', '县']


def build_address_dict():
    """"build dict files for jieba"""

    tag = [COL_PROV, COL_CITY, COL_DIST, COL_ST, COL_VIL]

    for i, f in enumerate(tag, start=1):
        df = pd.read_csv(os.path.join(*[PATH_DATA, 'data_raw', f + '.csv']), dtype=object, encoding='utf-8')

        df = df.filter(items=[COL_NM])

        for w in drop_word:
            df = df[df[COL_NM] != w]

        if f == COL_CITY:
            df_city = df

        if f == COL_DIST:
            df_inner = pd.merge(df_city, df, on=[COL_NM], how='inner')
            df = df.append(df_inner, ignore_index=True)
            df = df.drop_duplicates([COL_NM], keep=False)

        df[COL_NM] = df[COL_NM].str.replace('居民委员会', '')
        df[COL_NM] = df[COL_NM].str.replace('民委员会', '')  # 留下村
        df[COL_NM] = df[COL_NM].str.replace('居委会', '')
        df[COL_NM] = df[COL_NM].str.replace('委会', '')  # 留下村
        df[COL_NM] = df[COL_NM].str.replace('办事处', '')
        df['feq'] = pow(10, i)
        df['type'] = f

        # 除了COL_PROV, COL_CITY, 其他都会有重名情况
        df = df.drop_duplicates([COL_NM])
        df.to_csv(os.path.join(PATH_DICT, f + '.txt'), header=False, index=False, sep=' ', encoding='utf-8')

        print(f + ' dict built !')

    tag = [COL_PROV, COL_CITY]
    for i, f in enumerate(tag, start=1):
        df = pd.read_csv(os.path.join(*[PATH_DATA, 'data_raw', f + '.csv']), dtype=object, encoding='utf-8')

        df = df.filter(items=[COL_NM])

        for w in drop_word:
            df = df[df[COL_NM] != w]

        df = suffix_clean(df, COL_NM, COL_NM)
        df[COL_NM] = df[COL_NM].str.replace('市', '')
        df['feq'] = pow(10, i) - 1
        df['type'] = f

        df = df.drop_duplicates([COL_NM])
        df.to_csv(os.path.join(PATH_DICT, f + '_norm.txt'), header=False, index=False, sep=' ', encoding='utf-8')

        print(f + '_norm dict built !')


def build_norm_address_table():

    tag = [COL_PROV, COL_CITY]

    for i, f in enumerate(tag, start=1):
        df = pd.read_csv(os.path.join(*[PATH_DATA, 'data_raw', f + '.csv']), dtype=object, encoding='utf-8')

        for w in drop_word:
            df = df[df[COL_NM] != w]

        df = suffix_clean(df, COL_NM, COL_NM_NORM)
        df[COL_NM_NORM] = df[COL_NM_NORM].str.replace('市', '')

        df.to_csv(os.path.join(PATH_DATA, f + '_norm.csv'), index=False, encoding='utf-8')
        print(f + '_norm csv built !')

    tag = [COL_DIST, COL_ST, COL_VIL]

    for i, f in enumerate(tag, start=1):

        df = pd.read_csv(os.path.join(*[PATH_DATA, 'data_raw', f + '.csv']), dtype=object, encoding='utf-8')

        for w in drop_word:
            df = df[df[COL_NM] != w]


        df[COL_NM_NORM] = df[COL_NM].str.replace('居民委员会', '')
        df[COL_NM_NORM] = df[COL_NM_NORM].str.replace('民委员会', '')  # 留下村
        df[COL_NM_NORM] = df[COL_NM_NORM].str.replace('居委会', '')
        df[COL_NM_NORM] = df[COL_NM_NORM].str.replace('委会', '')  # 留下村
        df[COL_NM_NORM] = df[COL_NM_NORM].str.replace('办事处', '')

        df.to_csv(os.path.join(PATH_DATA, f + '_norm.csv'), index=False, encoding='utf-8')
        print(f + '_norm csv built !')


if __name__ == '__main__':
    build_address_dict()
    build_norm_address_table()
