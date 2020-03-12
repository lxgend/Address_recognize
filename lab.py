# coding=utf-8
import pandas as pd

from parms import *

from sqlalchemy import create_engine

engine= create_engine('sqlite:///'+PATH_DATA+'/data.sqlite')
frame = pd.read_sql(COL_PROV, engine)


print(frame)


# SELECT name FROM world
# WHERE population >= 200000000