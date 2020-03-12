# coding=utf-8
import pandas as pd
import jieba.analyse
import jieba.posseg as pseg
from parms import *




tag_list = [COL_PROV, COL_CITY, COL_DIST, COL_ST, COL_VIL]

for d in tag_list:
    jieba.load_userdict(os.path.join(PATH_DICT, d + '.txt'))




print( pseg.cut('广东省深圳市龙岗区平湖'))