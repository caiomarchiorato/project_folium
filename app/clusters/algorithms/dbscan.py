from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score
import pandas as pd

class DBSCANClustering:
    def __init__(self, epf: float=0.5, min_samples: int=5):
        self.epf = epf
        self.min_samples = min_samples
        self.dbscan = DBSCAN(eps=self.epf, min_samples=self.min_samples)
        
    def fit(self, data: pd.DataFrame):
        print('Fitting DBSCAN')
        if 'geometria' in data.columns:
            data = data.drop(columns=['geometria'], axis=1)
        self.dbscan.fit(data)
    
    def predict(self, data: pd.DataFrame):
        if 'geometria' in data.columns:
            data = data.drop(columns=['geometria'], axis=1)
        return self.dbscan.fit_predict(data) if self.dbscan else None
    
    def optimize_dbscan(self, data: pd.DataFrame, eps_values: list, min_samples_values: list):
        if 'geometria' in data.columns:
            data = data.drop(columns=['geometria'], axis=1)
        
        best_score = -1
        best_params = {'eps':None, 'min_samples':None}
        
        for eps in eps_values:
            for min_samples in min_samples_values:
                dbscan = DBSCAN(eps=eps, min_samples=min_samples)
                labels = dbscan.fit_predict(data)
                
                if len(set(labels)) > 1 and len(set(labels)) < len(data):
                    score = silhouette_score(data, labels)
                    if score > best_score:
                        best_score = score
                        best_params['eps'] = eps
                        best_params['min_samples'] = min_samples
        self.eps = best_params['eps']
        self.min_samples = best_params['min_samples']
        self.dbscan = DBSCAN(eps=self.eps, min_samples=self.min_samples)
        
        print(f'Best eps: {self.eps}, Best min_samples: {self.min_samples}, Best score: {best_score:.2f}')