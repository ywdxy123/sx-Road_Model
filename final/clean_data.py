import pandas as pd 
import numpy as np
def get_vector(a,b):
    return [float(b[0])-float(a[0]),float(b[1])-float(a[1])]

'''
求向量
'''
def test2(df):
    df=df.reset_index(drop=True).astype('object')
    df=df.sort_values(['start_date_time'])
    try:
        l=np.array(get_vector(df['loc'][0],df['loc'][df.index[-1]]))
        lx=np.sqrt(l.dot(l))
        TT=[]
        for i in df.index[:-1]:
            lt=np.array(get_vector(df['loc'][i],df['loc'][i+1]))
            ltx=np.sqrt(lt.dot(lt))
            if ltx!=0:
                TT.append(l.dot(lt)/(lx*ltx))
            else:
                TT.append(0)
        TT.append(1)
        df=pd.concat([df,pd.DataFrame(TT,columns=['vector'])],axis=1)
        df=df[df['vector']>-0.9960878351411849].dropna().reset_index(drop=True)
        return df[['start_date_time','msisdn','cgi','lon','lat']]
    except:
        print(e)
'''
筛选向量
'''
def get_clean_data(df):
    df=df.astype('object')
    df['loc']=df.apply(lambda x:[x['lon'],x['lat']],axis=1)
    try:
        dft=pd.DataFrame(df.groupby(['msisdn']).apply(test2).values,columns=['start_date_time','msisdn','cgi','lon','lat'])
        dft['start_date_time']=pd.to_datetime(dft['start_date_time'])
        dft['tmp']=dft['cgi'].shift(1)
        dft['flag']=(dft['cgi']!=dft['tmp'])
        dft=dft[dft['flag']==True]
        return dft[['start_date_time','msisdn','cgi','lon','lat']].reset_index(drop=True)
    except Exception as e:
        print(e)
'''
打包好的程序


'''