import pandas as pd
def get_shp_customer_info(customer,name_file): 
        
    path = "python/data/"+name_file+".csv"
    shp_names = pd.read_csv(path)
    df_aux = shp_names.loc[shp_names['CUST_NAME'] == customer,'CUST_TOTAL_KG':'NUM_OF_SHP'][['NUM_OF_SHP','CUST_TOTAL_PRICE']]
    
    return df_aux['CUST_TOTAL_PRICE'],df_aux['NUM_OF_SHP']

dd = get_shp_customer_info('10 RAJEB',"shipments")
print(dd)