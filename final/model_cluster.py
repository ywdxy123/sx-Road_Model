import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt



all=pd.read_csv(r'C:\Users\user\Desktop\Project\test\base_guangzhou.csv',encoding='utf8')
test=pd.read_csv(r'C:\Users\user\Desktop\Project\test\base_guangzhou.csv',usecols=[1,2])


all=all.dropna()
test=test.dropna()
dataset=test.astype('float64').as_matrix()

x= StandardScaler().fit_transform(dataset)
db=DBSCAN(eps=0.0004,min_samples=1).fit_predict(x)
all['cluster']=db
all.to_csv('xxx_cgi.csv')