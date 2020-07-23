import pandas as pd 
import os 
    
'''
df = pd.read_csv("python/marketing_data.csv")
print(df.describe())

'''
class Data():

    
    # Jiib data 
    def get_data(self):
        self.df = pd.read_csv("python/marketing_data.csv")
        self.features = self.df.columns.tolist()
        self.l=os.listdir('./python/data/')
        self.li =[x.split('.')[0] for x in self.l]
        self.ship = pd.read_csv("python/data/ship.csv")
        self.ship_parcel = pd.read_csv("python/data/ship_parcel.csv")

    def get_dfs(self,nom):
        if nom == 'ship' : 
            return pd.read_csv("python/data/ship.csv")
        else : 
            return pd.read_csv("python/data/ship_parcel.csv")

    @staticmethod
    def get_cluster(nom): 
        if nom == 'ship' : 
            return self.ship.cluster.unique().tolist()
        else : 
            return self.ship_parcel.cluster.unique().tolist()

    @staticmethod
    def get_shp_cluster_name(cluster): 
        
        shp_names = pd.read_csv("python/data/ship_with_names.csv")
        kk = shp_names.groupby('cluster')
        # clu_int = int(cluster)
        dff = kk.get_group(int(cluster))
        dff.drop('Unnamed: 0', axis = 1, inplace= True)
        #print(dff.head())

        return dff


    
    


    
    
