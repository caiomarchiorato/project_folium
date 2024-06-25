from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import joblib

class KMeansClustering:
    def __init__(self):
        self.best_n_clusters = None
        self.kmeans = None

    def get_elbow_curve(self, X):
        distortions = []
        for k in range(2, 11):
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit(X)
            distortions.append(kmeans.inertia_)
        self.best_n_clusters = distortions.index(min(distortions)) + 2
        return self.best_n_clusters
    
    def get_silhouette_score(self, X):
        if 'geometria' in X.columns:
            X = X.drop(columns=['geometria'], axis=1)
        silhouette_scores = []
        for k in range(2, 11):
            kmeans = KMeans(n_clusters=k, random_state=42)
            kmeans.fit_predict(X)
            score = silhouette_score(X, kmeans.labels_)
            silhouette_scores.append(score)
        
        self.best_n_clusters = silhouette_scores.index(max(silhouette_scores)) + 2
        return self.best_n_clusters
    
    def fit(self, X):
        print('Fitting KMeans')
        if 'geometria' in X.columns:
            print('Dropping geometria')
            X = X.drop(columns=['geometria'], axis=1)
        n_cluster = self.get_elbow_curve(X)
        self.kmeans = KMeans(n_clusters=n_cluster, random_state=42)
        self.kmeans.fit(X)
        #save the model 
        joblib.dump(self.kmeans, 'kmeans_model.pkl')
        
    
    def predict(self, X):
        if 'geometria' in X.columns:
            print('Dropping geometria')
            X = X.drop(columns=['geometria'], axis=1)
        return self.kmeans.predict(X) if self.kmeans else None

    def get_centroids(self):
        return self.kmeans.cluster_centers_ if self.kmeans else None