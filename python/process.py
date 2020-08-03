from data import Data
from sklearn.cluster import KMeans
from sklearn.datasets import make_blobs
from yellowbrick.cluster import KElbowVisualizer


ship_scaled = Data.get_scaled_ship()

def kmeans_segmentation(nmb_cluster): 
    kmeans = KMeans(nmb_cluster)
    kmeans.fit(ship_scaled) #Compute k-means clustering.
    labels = kmeans.labels_ #Labels of each point

shipments = Data.get_opr_shp_pr()

print(shipments.head(),"\n",shipments.shape)