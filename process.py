# coding=utf-8
import jieba
import pandas as pd

from data_processor.data_clean import input_normalize
from extract.complement import complement_stgy
from extract.tokenizer import extract_entity
from parms import *

tag_list = [COL_PROV, COL_CITY, COL_DIST, COL_ST, COL_VIL]


def io_controller(df_input, col_input_raw):
    df_input, col_input_norm = input_normalize(df=df_input, col_origin=col_input_raw)

    df_input = extract_entity(df_input, col_input_norm)
    df_input = complement_stgy(df_input)

    tag_list.append(col_input_norm)

    df_input[col_input_norm] = df_input[tag_list].agg(''.join, axis=1)
    df_input[col_input_norm] = df_input[col_input_norm].str.replace(UNK, '')

    df_input[col_input_norm] = df_input[col_input_norm].apply(lambda x: ''.join(sorted(set(jieba.cut(x)), key=x.index)))

    return df_input


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    txt1 = '玉山镇朝阳西路168号'

    df = pd.DataFrame([['中山市中堂镇鹤田村']], columns=[COL_INPUT_RAW])
    df = io_controller(df, COL_INPUT_RAW)

    logger.debug(df)





