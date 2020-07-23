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
        print(type(self.li))  
        self.ship = pd.read_csv("python/data/ship.csv")
        self.ship_parcel = pd.read_csv("python/data/ship_parcel.csv")
        self.customer_names = pd.read_csv("python/data/ship_with_names.csv").CUST_NAME.tolist()
        print(type(self.customer_names)) 

   
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

    @staticmethod
    def get_top_shps(df) : 
        top_cust_shp = df.nlargest(5, 'NUM_OF_SHP')['NUM_OF_SHP'].tolist()
        top_cust_name = df.nlargest(5, 'NUM_OF_SHP')['CUST_NAME'].tolist()

        return top_cust_shp,top_cust_name

    @staticmethod
    def get_top_kgs(df) : 
        top_cust_kg = df.nlargest(5, 'CUST_TOTAL_KG')['CUST_TOTAL_KG'].tolist()
        top_cust_kg_name = df.nlargest(5, 'CUST_TOTAL_KG')['CUST_NAME'].tolist()

        return top_cust_kg,top_cust_kg_name

    @staticmethod
    def get_buttom_shps(df) : 
        top_cust_shp = df.nsmallest(5, 'NUM_OF_SHP')['NUM_OF_SHP'].tolist()
        top_cust_name = df.nsmallest(5, 'NUM_OF_SHP')['CUST_NAME'].tolist()

        return top_cust_shp,top_cust_name

    @staticmethod
    def get_bottom_kgs(df) : 
        top_cust_kg = df.nsmallest(5, 'CUST_TOTAL_KG')['CUST_TOTAL_KG'].tolist()
        top_cust_kg_name = df.nsmallest(5, 'CUST_TOTAL_KG')['CUST_NAME'].tolist()

        return top_cust_kg,top_cust_kg_name

    
    


    
    
