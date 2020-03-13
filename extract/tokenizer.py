# coding=utf-8
import jieba.analyse
import jieba.posseg as pseg


from parms import *

for d in os.listdir(PATH_DICT):
    jieba.load_userdict(os.path.join(PATH_DICT, d))

tag_list = [COL_PROV, COL_CITY, COL_DIST, COL_ST, COL_VIL]


def get_token_and_flag(df, col_norm):
    col_cut = 'cut_tmp'
    col_cut_flag = 'cut_flag'

    # 此列是list:   pair(word,tag)
    df[col_cut] = df[col_norm].apply(lambda x: pseg.lcut(x))

    # 此列是list: tag
    df[col_cut_flag] = df[col_cut].apply(lambda x: list(w.flag for w in x))
    return df, col_cut, col_cut_flag


def extract_entity(df, col_norm):
    df, col_cut, col_cut_flag = get_token_and_flag(df, col_norm)

    for tag in tag_list:
        col_entity_idx = 'idx_' + tag

        # 获取特定tag的index,  无此tag则index=999
        df[col_entity_idx] = df[col_cut_flag].apply(lambda x: x.index(tag) if tag in x else 999)

        # 根据tag index，获取tag对应的word， 如果index=999, 则entity = unk
        df[tag] = df.apply(
            lambda x: x[col_cut][int(x[col_entity_idx])].word if x[col_entity_idx] != 999 else UNK,
            axis=1)

        df = df.drop([col_entity_idx], axis=1)

    df = df.drop([col_cut, col_cut_flag], axis=1)

    return df
