# coding=utf-8
import pandas as pd

from data_processor.data_clean import suffix_clean
from parms import *

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


def build_address_dict():
    """"build dict files for jieba"""

    drop_word = ['省直辖县级行政区划', '自治区直辖县级行政区划', '市辖区']

    tag = [COL_PROV, COL_CITY, COL_DIST, COL_ST, COL_VIL]

    for i, f in enumerate(tag, start=1):
        df = pd.read_csv(os.path.join(PATH_DATA, f + '.csv'), dtype=object, encoding='utf-8')

        df = df.filter(items=['name'])


        for w in drop_word:
            df = df[df['name'] != w]

        if f == COL_CITY:
            df_city = df

        if f == COL_DIST:
            df_inner = pd.merge(df_city, df, on=['name'], how='inner')
            df = df.append(df_inner, ignore_index=True)
            df = df.drop_duplicates(['name'], keep=False)

        df['name'] = df['name'].str.replace('居民委员会', '')
        df['name'] = df['name'].str.replace('民委员会', '')  # 留下村
        df['name'] = df['name'].str.replace('居委会', '')
        df['name'] = df['name'].str.replace('委会', '')     # 留下村
        df['name'] = df['name'].str.replace('办事处', '')
        df['feq'] = pow(10, i)
        df['type'] = f

        df = df.drop_duplicates(['name'])
        df.to_csv(os.path.join(PATH_DICT, f + '.txt'), header=False, index=False, sep=' ', encoding='utf-8')

        print(f + ' dict built !')

    tag = [COL_PROV, COL_CITY]
    for i, f in enumerate(tag, start=1):
        df = pd.read_csv(os.path.join(PATH_DATA, f + '.csv'), dtype=object, encoding='utf-8')

        df = df.filter(items=['name'])

        for w in drop_word:
            df = df[df['name'] != w]

        df = suffix_clean(df, 'name')
        df['name'] = df['name'].str.replace('市', '')
        df['feq'] = pow(10, i) - 1
        df['type'] = f

        df = df.drop_duplicates(['name'])
        df.to_csv(os.path.join(PATH_DICT, f + '_norm.txt'), header=False, index=False, sep=' ', encoding='utf-8')

        print(f + '_norm dict built !')


if __name__ == '__main__':
    build_address_dict()
