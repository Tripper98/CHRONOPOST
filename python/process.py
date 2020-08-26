
import pandas as pd 
import numpy as np

from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from yellowbrick.cluster import KElbowVisualizer
from sklearn.preprocessing import StandardScaler, normalize

from sklearn.decomposition import PCA

class Process : 

    @staticmethod
    def K_means(col_city_type,city_type) :
        
        df = pd.read_csv("python/data/big_df.csv")

        # Group by city || Type of customer 

        df_grouped = df[df[col_city_type]== city_type]

        # Slice data 

        df_resized = df_grouped.loc[:, 'CUST_TOTAL_VOLUME':'NUM_OF_SHP']
        scaler = StandardScaler()
        df_scaled = scaler.fit_transform(df_resized)

        # choose the k number 

        model = KMeans() 
        visualizer = KElbowVisualizer(model, k=(1,20))

        visualizer.fit(df_scaled)        # Fit the data to the visualizer
        k = visualizer.elbow_value_

        # k-means algo

        kmeans = KMeans(k)
        kmeans.fit(df_scaled) #Compute k-means clustering.
        labels = kmeans.labels_ #Labels of each point
        y_kmeans = kmeans.fit_predict(df_scaled)
        df_grouped['cluster'] = labels

        # Pca dude  :)
        pca = PCA(n_components=2)
        principal_comp = pca.fit_transform(df_scaled)
        pca_df = pd.DataFrame(data = principal_comp, columns =['pca1','pca2'])
        pca_df = pd.concat([pca_df,pd.DataFrame({'cluster':labels})], axis = 1)

        return pca_df,df_grouped

