from sqlalchemy import create_engine
import pandas as pd
conn = create_engine('mysql+pymysql://root:hantele@192.168.6.10:5029/test10086?charset=utf8',pool_size=10000)
#conn = create_engine('mysql+pymysql://root:hantele@192.168.6.10:5029/Data_0104?charset=utf8')
def getData(sql_str):
	data=pd.read_sql(sql_str,conn)
	return data
def saveData(df,name):
    pd.io.sql.to_sql(df,name,conn, schema='test10086', if_exists='append',index = False)
    #pd.io.sql.to_sql(df,name,conn, schema='Data_0104', if_exists='append',index = False)
    