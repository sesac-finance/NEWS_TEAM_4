import pandas as pd
from gensim.models.doc2vec import Doc2Vec
import matplotlib.pyplot as plt
from tqdm import tqdm

def load_model(model_name, data):
    corpus_vector = []
    model= Doc2Vec.load(model_name)
    for doc in data:
        corpus_vector.append(model.infer_vector(doc.split()))
    return corpus_vector

def dbscan(corpus_vector):
    """Function to form dbscan clusters and display them"""
#     eps = 0.005# how close points should be to each other to be considered a part of a cluster 
#     min_samples = 3# the minimum number of points to form a dense region  
#     dbscan = DBSCAN( eps=eps, min_samples=min_samples,metric = "cosine" ) 
#     dbscan_model = dbscan.fit(corpus_vector)
    
    pca = PCA(n_components=2)
    result = pca.fit_transform(corpus_vector)
    print(result.shape)
    db = DBSCAN(eps=0.01, min_samples=3)
    dbscan_model = db.fit(result)
    #Forming the clusters

    core_samples_mask = np.zeros_like(dbscan_model.labels_, dtype=bool)
    core_samples_mask[dbscan_model.core_sample_indices_] = True
    labels1 = dbscan_model.labels_
    n_clusters_ = len(set(labels1)) - (1 if -1 in labels1 else 0) # Number of clusters in labels
    # print(labels1)
    print(len(labels1))
    # print(n_clusters_) # number of clusters
    
    clusters1 = {} # a dictionary for different cluster 
    for c, i in enumerate(labels1):
        if i == -1:
            continue
        elif i in clusters1:
            clusters1[i].append( data[c] )
        else:
            clusters1[i] = [data[c]]

    # for c in clusters1: # print the different clusters
    #     # print("Cluster No."+" "+str(c)+" "+str(clusters1[c]))
    #     # print()
    
    return clusters1
    
def plot_dbscan(X , eps, min_samples):
    pca = PCA(n_components=2)
    result = pca.fit_transform(X)
    print(result.shape)
    db = DBSCAN(eps=eps, min_samples=min_samples)
    db.fit(result)
    y_pred = db.fit_predict(result)
    plt.scatter(result[:,0], result[:,1],c=y_pred, cmap='Paired')
    plt.title("DBSCAN")
    


df = pd.read_csv('/Users/stillssi/Desktop/NEWS_TEAM_4/MDL/testmodel/sample_df.csv')
data = []
for i in df['Content'].values:
    data.append(i)

corpus_vector = load_model("/Users/stillssi/Desktop/NEWS_TEAM_4/MDL/testmodel/trainedMDL",data)

from sklearn.decomposition import PCA
from sklearn.cluster import DBSCAN
import numpy as np

cluster1 = dbscan(corpus_vector)

df['sim'] =''
for i in range(len(df)):
    for j in cluster1:
        if df["Content"].loc[i] in j:
            df['sim'].loc[i] = j
            pass

print(df)