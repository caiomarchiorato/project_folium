from app.dataprep.process_data import DateProcessor, Pivoter, DropNan, CategoricalEncoder, SelectiveScaler
from app.clusters.algorithms.kmeans import KMeansClustering
from app.clusters.algorithms.dbscan import DBSCANClustering
from app.clusters.algorithms.agg_clusters import AggClustering
from app.clusters.algorithms.bisecting_kmeans import BisectingKMeansClustering
from app.dataprep.load_data import GeometryDataProcessor
from sklearn.pipeline import Pipeline
from app.data_config import Config
import pandas as pd
import numpy as np

columns_date, columns, categorical_columns, exclude_normalize_columns, estadios = Config.date_columns, Config.columns, Config.categorical_columns, Config.exclude_normalized_columns, Config.estadios
data_safra = Config.safra

processor = GeometryDataProcessor()
data, _ = processor.load_data_geometry(query_name='all_data', safra=data_safra, columns=columns)

pipeline = Pipeline(steps=[
    ('date_processor', DateProcessor(columns_date=columns_date)),
    ('pivoter', Pivoter(pivot_columns=['soma_chuva'], index= ['produtividade', 'dataplantioinicio', 'datacolheitainicio', 'textura','geometria'], pivot_switch=True)),
    ('categorical_encoder', CategoricalEncoder(columns=categorical_columns)),
    ('scaler', SelectiveScaler(exclude_columns=exclude_normalize_columns)),
    ('drop_nan', DropNan())
])

class PipelineProcessor:
    def get_kmeans_on_data():
        processed_data = pipeline.fit_transform(data)
        cluster_processor = KMeansClustering()
        cluster_processor.fit(processed_data)
        processed_data['cluster'] = cluster_processor.predict(processed_data)
        # processed_data = pd.concat([processed_data, geometry], axis=1)
        return processed_data

    def get_dbscan_on_data():
        processed_data = pipeline.fit_transform(data)
        cluster_processor = DBSCANClustering()
        
        eps_values = [0.5]
        # eps_values = np.linspace(0.1, 10, 100)
        min_samples_values = range(2, 11)
        cluster_processor.optimize_dbscan(processed_data, eps_values, min_samples_values)
        
        cluster_processor.fit(processed_data)
        processed_data['cluster'] = cluster_processor.predict(processed_data)
        return processed_data
    
    def get_agg_on_data():
        processed = pipeline.fit_transform(data)
        cluster_processor = AggClustering()
        cluster_processor.get_silhouette_score(processed)
        cluster_processor.fit(processed)
        processed['cluster'] = cluster_processor.agg.labels_
        return processed
    
    # def get_bisecting_kmeans_on_data():
    #     processed = pipeline.fit_transform(data)
    #     cluster_processor = BisectingKMeansClustering()
    #     cluster_processor.fit(processed)
        
    #     processed['cluster'] = cluster_processor.predict(processed)
    #     return processed

def get_clusters(cluster: str):
    if cluster == 'kmeans':
        return PipelineProcessor.get_kmeans_on_data()
    elif cluster == 'dbscan':
        return PipelineProcessor.get_dbscan_on_data()
    elif cluster == 'agg':
        return PipelineProcessor.get_agg_on_data()
    elif cluster == 'bisecting_kmeans':
        return PipelineProcessor.get_bisecting_kmeans_on_data()
    else:
        raise ValueError('Invalid cluster type')
