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
    def get_info_cust(name_file,cust) :

        path = "python/data/"+name_file+".csv"
        test = pd.read_csv(path)
        x = test[test['CUST_NAME']== cust]['CUST_TOTAL_PRICE'].tolist()
        y = test[test['CUST_NAME']== cust]['NUM_OF_SHP'].tolist()
     
        return x[0],y[0]

    
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
        return pd.read_csv("python/prod_cust.csv")

    @staticmethod
    def get_product_data(name_product) : 
        prod_ship = pd.read_csv("python/products_time_series.csv")
        grouped_by_prod = prod_ship.groupby('PROD_NAME')
        grouped_prod_date = grouped_by_prod.get_group(name_product).groupby('DATE')
        sl = grouped_prod_date.DATE.unique().astype(str).str[2:12].tolist()
        datatata = {'DATE' :[x for x in sl] , \
                'TOTAL KG':[grouped_prod_date.get_group(str(x)).TOTAL_DESI_KG.sum() for x in sl], \
                'TOTAL VOLUME':[grouped_prod_date.get_group(str(x)).TOTAL_VOLUME.sum() for x in sl], \
                'TOTAL PRICE':[grouped_prod_date.get_group(str(x)).TOTAL_PRICE_LOCAL.sum() for x in sl], \
                'TOTAL SHIPMENTS':[grouped_prod_date.get_group(str(x)).CUST_ID.count() for x in sl] }
        shipments_products_ = pd.DataFrame(datatata)
        return shipments_products_

    @staticmethod
    def get_cities() : 
        return pd.read_csv("python/data/big_df.csv").City.unique()

    @staticmethod
    def get_types() : 
        return ['A','B','C']

    @staticmethod
    def get_names_groupe() : 
        return ['City','Type Of Customer']

    
    
    
