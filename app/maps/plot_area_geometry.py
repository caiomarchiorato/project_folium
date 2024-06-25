import folium
import json

class GeometryMapClusters():
    def __init__(self, cluster_colors):
        self.cluster_colors = cluster_colors
    
    def plot_geometry_of_clusters(self, data, map):
        for index, row in data.iterrows():
            coordenadas = json.loads(row['geometria'])['coordinates'][0]  
            coordenadas_corrigidas = [[coord[1], coord[0]] for coord in coordenadas]
            cluster = row['cluster']
            cor = self.cluster_colors[cluster % len(self.cluster_colors)]
            folium.Polygon(locations=coordenadas_corrigidas, color=cor, fill_color=cor, fill_opacity=0.7).add_to(map)
        
        return map