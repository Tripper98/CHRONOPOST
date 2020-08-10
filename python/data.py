import pandas as pd 
import numpy as np
import os 
    
'''
shipments = pd.read_csv("python/marketing_data.csv")
print(shipments.describe())

'''
class Data():

    
    # Jiib data 
    # def get_data(self):
    #     self.shipments = pd.read_csv("python/marketing_data.csv")
    #     self.features = self.shipments.columns.tolist()
    #     self.l=os.listdir('./python/data/')
    #     self.li =[x.split('.')[0] for x in self.l]
    #     #print(type(self.li))  
    #     self.ship = pd.read_csv("python/data/ship.csv")
    #     self.ship_parcel = pd.read_csv("python/data/ship_parcel.csv")
    #     self.customer_names = pd.read_csv("python/data/ship_with_names.csv").CUST_NAME.tolist()
        #print(type(self.customer_names)) 

    def get_data(self): 
        self.shipments = pd.read_csv("python/data/shipments.csv")

        self.l=os.listdir('./python/data/')
        self.li =[x.split('.')[0] for x in self.l]

    
    def get_opr_shp():
        shipments = pd.read_csv("python/opr_ship.csv")
        shipments.drop('Unnamed: 0',axis=1, inplace= True)
        shipments = shipments[shipments['TOTAL_PRICE_LOCAL'].notna()]
        shipments = shipments[shipments['TOTAL_VOLUME'].notna()]
        #shipments = shipments[shipments['CUST_ID'].notna()]
        shipments = shipments[shipments['SHIPMENT_TYPE'].notna()]
        shipments.rename(columns={"PAYER_CUST_ID": "CUST_ID"}, inplace=True)
        shipments['CUST_ID'] = shipments['CUST_ID'].astype(np.int64)
        shipments['SHIPMENT_TYPE'] = shipments['SHIPMENT_TYPE'].astype(np.int64)
        shipments["RECEIVER_COUNTRY_ID"] = shipments["RECEIVER_COUNTRY_ID"].fillna(value=-2)
        shipments["SENDER_COUNTRY_ID"] = shipments["SENDER_COUNTRY_ID"].fillna(value=619)
        shipments['RECEIVER_COUNTRY_ID'] = shipments['RECEIVER_COUNTRY_ID'].astype(np.int64)
        shipments['SENDER_COUNTRY_ID'] = shipments['SENDER_COUNTRY_ID'].astype(np.int64)
        return shipments

    def get_opr_shp_pr():
        df = Data.get_opr_shp().groupby('CUST_ID')
        ls = df.CUST_ID.unique().tolist()
        data = {'CUST_ID':[int(x) for x in ls] , \
        'CUST_TOTAL_KG':[df.get_group(int(x)).TOTAL_DESI_KG.sum() for x in ls], \
        'CUST_TOTAL_VOLUME':[df.get_group(int(x)).TOTAL_VOLUME.sum() for x in ls], \
        'CUST_TOTAL_PRICE':[df.get_group(int(x)).TOTAL_PRICE_LOCAL.sum() for x in ls], \
        'NUM_OF_SHP':[df.get_group(int(x)).SHP_ID.count() for x in ls], \
        'NUM_SENDER_COUNTRY' : [df.get_group(int(x)).SENDER_COUNTRY_ID.nunique() for x in ls], \
        'NUM_RECEIVER_COUNTRY' : [df.get_group(int(x)).RECEIVER_COUNTRY_ID.nunique() for x in ls]
       }
        return pd.DataFrame(data)

    def get_scaled_ship(): 
        df = Data.get_opr_shp_pr()
        shp_without_custid = df.drop('CUST_ID',axis=1)
        scaler = StandardScaler()
        return scaler.fit_transform(shp_without_custid)

    def get_gen_customer():
        return pd.read_csv("python/gen_customer.csv")

    def get_gen_customer():
        return pd.read_csv("python/gen_country.csv")
    
    def get_shipmentss(self,nom):
        if nom == 'ship' : 
            return pd.read_csv("python/data/ship.csv")
        else : 
            return pd.read_csv("python/data/ship_parcel.csv")

    # mo9atan #########""
    @staticmethod
    def get_pca(dataframe):
        path = "python/data/"+dataframe+".csv"
        return pd.read_csv(path)[['pca1','pca2','cluster']]
    ############

    @staticmethod
    def get_cluster(nom): 
        if nom == 'ship' : 
            return self.ship.cluster.unique().tolist()
        else : 
            return self.shipments.unique().tolist()

    @staticmethod
    def get_shp_cluster_name(cluster,name_file): 
        
        path = "python/data/"+name_file+".csv"
        shp_names = pd.read_csv(path)
        kk = shp_names.groupby('cluster')
        # clu_int = int(cluster)
        shipmentsf = kk.get_group(int(cluster))
    
        return shipmentsf
    
    @staticmethod
    def get_shp_customer_info(customer,name_file): 
        
        path = "python/data/"+name_file+".csv"
        shp_names = pd.read_csv(path)
        df_aux = shp_names.loc[shp_names['CUST_NAME'] == customer,'CUST_TOTAL_KG':'NUM_OF_SHP'][['NUM_OF_SHP','CUST_TOTAL_PRICE']]
        return df_aux['CUST_TOTAL_PRICE'][0],df_aux['NUM_OF_SHP'][0]
    

    @staticmethod
    def get_top_shps(shipments) : 
        top_cust_shp = shipments.nlargest(5, 'NUM_OF_SHP')['NUM_OF_SHP'].tolist()
        top_cust_name = shipments.nlargest(5, 'NUM_OF_SHP')['CUST_NAME'].tolist()

        return top_cust_shp,top_cust_name

    @staticmethod
    def get_top_volume(shipments) : 
        top_cust_shp = shipments.nlargest(5, 'CUST_TOTAL_VOLUME')['CUST_TOTAL_VOLUME'].tolist()
        top_cust_name = shipments.nlargest(5, 'CUST_TOTAL_VOLUME')['CUST_NAME'].tolist()

        return top_cust_shp,top_cust_name

    @staticmethod
    def get_top_price(shipments) : 
        top_cust_shp = shipments.nlargest(5, 'CUST_TOTAL_PRICE')['CUST_TOTAL_PRICE'].tolist()
        top_cust_name = shipments.nlargest(5, 'CUST_TOTAL_PRICE')['CUST_NAME'].tolist()

        return top_cust_shp,top_cust_name

    @staticmethod
    def get_top_kgs(shipments) : 
        top_cust_kg = shipments.nlargest(5, 'CUST_TOTAL_KG')['CUST_TOTAL_KG'].tolist()
        top_cust_kg_name = shipments.nlargest(5, 'CUST_TOTAL_KG')['CUST_NAME'].tolist()

        return top_cust_kg,top_cust_kg_name

    @staticmethod
    def get_buttom_shps(shipments) : 
        top_cust_shp = shipments.nsmallest(5, 'NUM_OF_SHP')['NUM_OF_SHP'].tolist()
        top_cust_name = shipments.nsmallest(5, 'NUM_OF_SHP')['CUST_NAME'].tolist()

        return top_cust_shp,top_cust_name

    @staticmethod
    def get_buttom_kgs(shipments) : 
        top_cust_kg = shipments.nsmallest(5, 'CUST_TOTAL_KG')['CUST_TOTAL_KG'].tolist()
        top_cust_kg_name = shipments.nsmallest(5, 'CUST_TOTAL_KG')['CUST_NAME'].tolist()

        return top_cust_kg,top_cust_kg_name

    @staticmethod
    def get_buttom_price(shipments) : 
        top_cust_shp = shipments.nsmallest(5, 'CUST_TOTAL_PRICE')['CUST_TOTAL_PRICE'].tolist()
        top_cust_name = shipments.nsmallest(5, 'CUST_TOTAL_PRICE')['CUST_NAME'].tolist()

        return top_cust_shp,top_cust_name

    @staticmethod
    def get_buttom_volume(shipments) : 
        top_cust_kg = shipments.nsmallest(5, 'CUST_TOTAL_VOLUME')['CUST_TOTAL_VOLUME'].tolist()
        top_cust_kg_name = shipments.nsmallest(5, 'CUST_TOTAL_VOLUME')['CUST_NAME'].tolist()

        return top_cust_kg,top_cust_kg_name
    
    @staticmethod
    def get_info(df): 
        return df['NUM_OF_SHP'].mean(),df['CUST_TOTAL_PRICE'].mean()
    
    @staticmethod
    def get_columns_map() :
        return ['TOTAL KG','TOTAL VOLUME','TOTAL PRICE','TOTAL SHIPMENTS']
    
    @staticmethod
    def get_map_data() : 
        return pd.read_csv("python/df_map.csv")

    @staticmethod
    def get_map_data_sender() : 
        return pd.read_csv("python/df_map_sender.csv")

    @staticmethod
    def get_product_customer() : 
        return pd.read_csv("python/data/prod_cust.csv")

    
    
