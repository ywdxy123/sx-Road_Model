from sklearn.neighbors import KDTree
import pandas as pd 
import numpy as np
nodes=pd.read_csv('xxxx.csv')
cgi=pd.read_csv('xxxxx.csv')
def get_near_3_point(nodes,cgi):
	data=nodes[['lng','lat']]
	tree=KDTree(data)
	TT=[]
	for i in cgi.index:
	    taisen_id=cgi.loc[i][0]
	    target=[[cgi.loc[i][1],cgi.loc[i][2]]]
	    result=tree.query(target,k=3)
	    T=[taisen_id]
	    for ii in np.array(result)[1][0]:
	        T.append(df_nodes[df_nodes.index==ii]['osmid'].tolist()[0])
	    TT.append(T)
	return TT
if __name__ == '__main__':
	res=get_near_3_point(nodes,cgi)
	res_df=pd.DataFrame(res)
	res_df.columns=['osmid']+['near%s'%i for i in range(1,4)]
	res_df.to_csv('xxxxxx.csv',index=False)
	