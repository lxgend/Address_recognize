# coding=utf-8
import pandas as pd
from parms import *

""""build dict files for jieba"""

files = ['province', 'city', 'area', 'street', 'village']

for i, f in enumerate(files, start=1):
    df = pd.read_csv(os.path.join(PATH_DATA, f + '.csv'), dtype=object, encoding='utf-8')

    # df = df.head()
    df = df.filter(items=['name'])
    df['name'] = df['name'].str.replace('居委会', '')
    df['name'] = df['name'].str.replace('办事处', '')
    df['feq'] = 9 * pow(10, i)
    df['type'] = f

    df.to_csv(os.path.join(PATH_DICT, f + '.txt'), header=False, index=False, sep=' ', encoding='utf-8')

    print(f + ' dict  built !')
