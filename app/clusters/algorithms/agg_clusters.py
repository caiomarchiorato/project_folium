from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
import joblib
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot as plt

class AggClustering:
    def __init__ (self, linkage: str = 'ward'):
        self.linkage = linkage
        self.best_n_clusters = None
        self.agg = None
        
    def get_silhouette_score(self, X):
        if 'geometria' in X.columns:
            X = X.drop(columns=['geometria'], axis=1)
        silhouette_scores = []
        for k in range(2, 11):
            agg = AgglomerativeClustering(n_clusters=k, linkage=self.linkage)
            agg.fit_predict(X)
            score = silhouette_score(X, agg.labels_)
            silhouette_scores.append(score)
        self.best_n_clusters = silhouette_scores.index(max(silhouette_scores)) + 2
        return self.best_n_clusters
        
    def fit(self, X):
        print('Fitting Agglomerative clustering')
        if 'geometria' in X.columns:
            X = X.drop(columns=['geometria'], axis=1)
        n_cluster = self.best_n_clusters
        self.agg = AgglomerativeClustering(n_clusters=n_cluster, linkage=self.linkage)
        self.agg.fit_predict(X)
        joblib.dump(self.agg, 'agg_model.pkl')
        
    def get_linkage(self, X):
        if 'geometria' in X.columns:
            X = X.drop(columns=['geometria'], axis=1)
        Z = linkage(X, method=self.linkage)
        return Z

    def get_dendrogram(self, X):
        if 'geometria' in X.columns:
            X = X.drop(columns=['geometria'], axis=1)
        Z = linkage(X, method=self.linkage)
        
        plt.figure(figsize=(10,7))
        dendrogram(Z, truncate_mode='level', p=5)
        plt.title('Dendrogram')
        plt.xlabel('Index Numbers')
        plt.ylabel('Distance')
        plt.show()
