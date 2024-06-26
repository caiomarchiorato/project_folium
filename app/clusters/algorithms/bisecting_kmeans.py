from sklearn.cluster import BisectingKMeans
import pandas as pd

class BisectingKMeansClustering:
    def __init__(self, n_clusters: int=10):
        self.n_clusters = n_clusters
        self.bisecting_kmeans = None
        
    def fit(self, X: pd.DataFrame):
        if 'geometria' in X.columns:
            X = X.drop(columns=['geometria'], axis=1)
        self.bisecting_kmeans = BisectingKMeans(n_clusters=self.n_clusters, random_state=42)
        self.bisecting_kmeans.fit(X)
    
    def predict(self, X: pd.DataFrame):
        if 'geometria' in X.columns:
            X = X.drop(columns=['geometria'], axis=1)
        return self.bisecting_kmeans.predict(X)