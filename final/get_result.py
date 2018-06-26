EARTH_RADIUS=6371 
from math import radians, cos, sin, asin, sqrt,fabs
import pandas as pd 
import networkx as nx

def hav(theta):  
    s = sin(theta / 2)  
    return s * s 
def get_distance_hav(a,b):  
    lat0 = radians(float(a[1]))  
    lat1 = radians(float(b[1]) ) 
    lng0 = radians(float(a[0])  )
    lng1 = radians(float(b[0]))     
    dlng = fabs(lng0 - lng1)  
    dlat = fabs(lat0 - lat1)  
    h = hav(dlat) + cos(lat0) * cos(lat1) * hav(dlng)  
    distance = 2 * EARTH_RADIUS * asin(sqrt(h))     
    return distance
'''
计算距离
'''
def return_length(x):
    try:
        return float(edge_dict[str(x['edge'])])
    except:
        return float(get_distance_hav(node_dict[str(int(x['start']))],node_dict[str(int(x['end']))])*1000)
def speed_caculate(df,edge_dict,node_dict):
    df1=df.dropna()
    try:
        df1['length']=df1.apply(return_length,axis=1)
        speed_test=pd.DataFrame(df1.groupby(['time']).apply(lambda x:x['length'].sum())).reset_index()
        speed_test.columns=['time','length']
        speed_test=speed_test[speed_test['length']!=0].reset_index(drop=True)
        speed_test['time']=pd.to_datetime(speed_test['time'])
        speed_test['tmp']=speed_test['time'].shift(1)
        speed_test['space']=speed_test['time']-speed_test['tmp'] 
        speed_test1=speed_test.dropna()
        speed_test1['space']=speed_test1['space'].apply(lambda x:x.total_seconds()/3600)
        speed_test1['speed']=speed_test1['length']/speed_test1['space']/1000
        return speed_test1
    except Exception as e:
        print(e)
'''
计算速度
'''
def getMin(a):
    T=[]
    for i in a:
        T.append(len(i))
    return a[T.index(min(T))]

def getpath(df,test=False):
    df=df.sort_values(['start_date_time']).reset_index(drop=True)
    if df.shape[0]>3:
        #df=pd.merge(df,df_newTable,on=['cgi'])
        df_t=df[['near_1','near_2','near_3']]
        path_short=[]
        l=len(df_t)
        j=0

        while j<l-1:
            path_temp=[]
            try:
                if len(path_short)==0:    
                    for x in df_t.iloc[j].tolist():
                        for y in df_t.iloc[j+1].tolist():
                            try:
                                path_temp.append(nx.shortest_path(v,source=str(x),target=str(y)))
                            except Exception as e:
                                #print(e)
                                pass
                    path_short.append(getMin(path_temp))
                    del path_temp
                    j+=1
                else:
                    path_temp=[]
                    x=path_short[-1][-1]
                    for y in df_t.iloc[j+1].tolist():
                        try:
                            path_temp.append(nx.shortest_path(v,source=str(x),target=str(y)))
                        except Exception as e:
                            #print(e)
                            pass
                    path_short.append(getMin(path_temp))
                    del path_temp
                    j+=1
            except Exception as e:
                #print(e)
                #break
                pass

        start_time=df.start_date_time.tolist()[0]
        it=iter(list(df.start_date_time.tolist())[1:])
        it1=iter(list(df.cgi.tolist())[1:])
        df_empty=pd.DataFrame(columns=['end','flag'])
        #print(len(path_short))
        for k in path_short:
            if len(k)>1:
                df1=pd.DataFrame(k[:-1],columns=['end'])
            else:
                df1=pd.DataFrame(k,columns=['end'])
            #print(df1)
            #print(df1.shape[0])
            df1['flag']=(df1.index==0)
            df1['time']=next(it)
            #print(df1['time'].iloc[0])
            df1['cgi']=next(it1)
            df_empty=pd.concat([df_empty,df1])
                
        #return df_empty.reset_index(drop=True)
        df_empty['start']=df_empty['end'].shift(1)
        df_empty=df_empty.reset_index(drop=True)
        #return make_result(dt,df_empty)
        if test!=True:
            df_empty=speed_analyse(df_empty,start_time)
        else:
            pass
        df_empty['msisdn']=df.msisdn.iloc[0]
        #df_empty=pd.merge(df_empty,df_)
        return df_empty
    else:
        return None
'''
输出路径
'''
def return_length(x):
    try:
        return float(edge_dict[str(x['edge'])])
    except:
        return float(get_distance_hav(node_dict[str(int(x['start']))],node_dict[str(int(x['end']))])*1000)
def speed_caculate(df,start_time):
    df1=df.dropna()
    try:
        df1['length']=df1.apply(return_length,axis=1)
        speed_test=pd.DataFrame(df1.groupby(['time']).apply(lambda x:x['length'].sum())).reset_index()
        speed_test.columns=['time','length']
        speed_test=speed_test.reset_index(drop=True)
        #speed_test=speed_test[speed_test['length']!=0].reset_index(drop=True)
        speed_test['time']=pd.to_datetime(speed_test['time'])
        #speed_test['tmp']=speed_test['time'].shift(1)
        speed_test['tmp']=pd.Series([start_time]+speed_test.time.tolist()[:-1])
        speed_test['space']=speed_test['time']-speed_test['tmp']
        speed_test1=speed_test.dropna()
        speed_test1['space']=speed_test1['space'].apply(lambda x:x.total_seconds()/3600)
        speed_test['space'].iloc[0]=300
        speed_test1['speed']=speed_test1['length']/speed_test1['space']/1000
        #print(speed_test)
        return speed_test1
    except Exception as e:
        print(e)
        #pass
def speed_analyse(df,start_time):
    res=speed_caculate(df,start_time)
    #time_list=res['tmp'].tolist()
    it=iter(res.speed.tolist())
    #df=df.dropna()
    #print(list(it))
    def g(x):
        if x['flag']==True:
            return next(it)
        else:
            pass
    #print(df.apply(g,axis=1))
    #df=df[df['start'].notnull()]
    df['speed']=df.apply(g,axis=1)
    #print(df['speed'])
    df['speed']=df['speed'].fillna(method='pad')
    return df[['cgi', 'start','end',  'time',  'speed']]
'''
速度计算
'''