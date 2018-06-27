import pandas as pd 
import osmnx as ox
import networkx as nx
import numpy as np
import time 
import os 
from multiprocessing import *
from sqlData import *
from get_result import *
pd.options.mode.chained_assignment = None
'''
读取数据数据
'''
v=nx.read_graphml(r'C:\Users\user\Desktop\Project\T\gz.graphml')# osm 数据 
os.chdir(r'C:\Users\user\Desktop\Project\道路数据建模\Model_ywd\Model\new_Data')
df_newTable=pd.read_csv('mergeTable.csv') #读取 泰森多边形&cgi&对应osmid 联表
df_osmid=pd.read_table('point_xy.txt') #读取osmid 坐标
df_o_name=pd.read_csv('osmid_name.csv',encoding='gbk') #读取osmid对应路名

'''
读取node_dict和edge_dict
'''
with open ('node_dict.txt','r') as f :
    node_dict_str=f.read()
with open ('edge_dict.txt','r') as f :
    edge_dict_str=f.read()
node_dict=eval(node_dict_str)
edge_dict=eval(edge_dict_str)



if __name__ == '__main__':
	'''
	获取输入数据，格式化字段名
	'''
	sql='select * from test1086.zjxc_1'
	df=getData(sql)
	df.rename(columns={'lng':'lon'},inplace=True)
	df=df[['start_date_time','msisdn','cgi','lon','lat']].sort_values(['msisdn','start_date_time']).reset_index(drop=True)
	'''
	处理清洗数据
	'''
	print('start clean data')
	first_time=time.time()
	test_data=df.groupby(['msisdn']).apply(get_clean_data).reset_index(drop=True)
	print('waste %s secends'%(time.time()-first_time))
	'''
	清洗后数据与联表匹配
	'''	
	data=pd.merge(test_data,df_newTable,on=['cgi'])
	data=data.drop_duplicates(['msisdn','taisen_id'],keep='first').reset_index(drop=True).reset_index(drop=True)
	'''
	开始处理数据，目前是用单进程进行处理，优化余地在多进程和整体groupby(['msisdn'])
	'''
	msisdn_list=list(set(data.msisdn.tolist()))
	Sucess_res=[]
	Fail_msisdn_list=[]
	cnt=0
	secend_time=time.time()
	print('start  get route...')
		'''
	p=Pool(cpu_count())
	for msisdn in msisdn_list:
	    dft=data[data['msisdn']==msisdn]
	    p.apply_async(getpath,args=(dft,))
	p.close()
	p.join()
	
	'''
	for msisdn in msisdn_list:

	    dft=data[data['msisdn']==msisdn]
	    try:
	        res=getpath(dft)
	        cnt+=1
	        Sucess_res.append(res)
	    except Exception as e:
	        Fail_msisdn_list.append(msisdn)
	    if cnt%1000==0:#每1000个用户进行一次存储
	        try:
	            fnl=pd.concat(T)
	            saveData(fnl,'zjxc_6_20_t2')
	            print(cnt)
	        except Exception as e:
	            print(e)
	print('finish and waste %s secends'%(time.time()-secend_time))
	print('all finish')
