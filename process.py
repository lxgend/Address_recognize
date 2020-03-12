# coding=utf-8
import pandas as pd
from data_processor.data_clean import input_normalize
from extract.tokenizer import extract_entity
from parms import *

def io_controller(df_input, col_input_raw):

    df_input, col_input_norm = input_normalize(df=df_input, col_origin=col_input_raw)

    df_input = extract_entity(df_input, col_input_norm)

    return df_input


if __name__ == '__main__':
    pd.set_option('display.max_columns', None)
    pd.set_option('display.max_rows', None)

    df = pd.DataFrame([['东莞市中堂镇鹤田村']], columns = [COL_INPUT_RAW])
    df = io_controller(df, COL_INPUT_RAW)





    print(df)


