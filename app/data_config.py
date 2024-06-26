from branca.colormap import LinearColormap
import pandas as pd

class Config:
    def __init__(self):
        pass
    
    def config_colormap_produtividade(data: pd.DataFrame, color_target: str=None) -> LinearColormap:
        colormap = LinearColormap(colors=["#00FF00", "#66FF00", "#CCFF00", "#FFCC00", "#FF6600", "#FF0000"],
                                index=data['produtividade'].quantile([0.166, 0.333, 0.5, 0.666, 0.833]),
                                vmin=data['produtividade'].min(), vmax=data[color_target].max())
        colormap.caption = "Produtividade de Soja (kg/ha)"
        colormap.title_color = "white"
        return colormap

    estadios = ["r5-r6", "r4-r5", "r3-r4-2","r5", "r3-r4-2"]
    
    columns = ['estadio','soma_chuva','produtividade', 'textura', 'geometria','dataplantioinicio', 'datacolheitainicio']
    
    date_columns = ['dataplantioinicio', 'datacolheitainicio']

    exclude_normalized_columns = ['geometria']

    categorical_columns = ['textura']
    cluster_colors = ['#e41a1c', '#377eb8', '#4daf4a', '#984ea3', '#ff7f00', '#ffff33', '#a65628', '#f781bf']
    
    safra = ['Safra 23/24', 
            'Safra 21/22', 'Safra 22/23'
            ]
