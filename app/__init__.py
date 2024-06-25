from flask import Flask, render_template
from app.data_config import Config
from app.pipeline import get_clusters
from app.maps.plot_area_geometry import GeometryMapClusters
import json
import folium
# ===========================================
# Preparing the data
# ===========================================
columns = Config.columns
clusters = get_clusters(cluster='kmeans')
cluster_colors = Config.cluster_colors

# ===========================================
# Creating the map
# ===========================================

app = Flask(__name__)
@app.route('/')
def index():
    centroid_lon = clusters['geometria'].apply(eval).tolist()[1]['coordinates'][0][0][0]
    centroid_lat = clusters['geometria'].apply(eval).tolist()[1]['coordinates'][0][0][1]
    m = folium.Map(location=[centroid_lat, centroid_lon], tiles="OpenStreetMap", zoom_start=12)
    
    geo_map_processor = GeometryMapClusters(cluster_colors=cluster_colors)
    map = geo_map_processor.plot_geometry_of_clusters(data=clusters, map=m)
    
    map.save('app/templates/map.html')
    return render_template('map.html')

if __name__ == '__main__':
    app.run(debug=True) 