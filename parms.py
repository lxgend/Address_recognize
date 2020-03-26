# coding=utf-8
import os
import sys
from loguru import logger

PATH_PJ_ROOT = os.path.dirname(os.path.abspath(__file__))
PATH_DATA = os.path.join(PATH_PJ_ROOT, 'data')
PATH_DICT = os.path.join(PATH_PJ_ROOT, 'dict')

COL_INPUT_RAW = 'input_raw'
COL_INPUT_NORM = 'input_norm'

UNK = 'unk'


COL_PROV = 'province'
COL_CITY = 'city'
COL_DIST = 'district'
COL_ST = 'street'
COL_VIL = 'village'


# logger.add(sys.stderr, format=logformat)
# logger.add(os.path.join(*[PATH_LOG, 'runtime', 'runtime_{time}.log']), rotation='1 week', level='INFO')
# logger.add(os.path.join(PATH_LOG, 'access.log'), format='{time}')