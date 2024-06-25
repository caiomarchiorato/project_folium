import pandas as pd
from app.dataprep.query_execution import load_create_data
from typing import Tuple, Optional
from sklearn.preprocessing import LabelEncoder

class GeometryDataProcessor():
    def __init__(self, data=None):
        self.data = data
    
    def __data_filter(self, data: pd.DataFrame, safra:list[str] ,columns: Optional[list[str]]=None) -> pd.DataFrame:
        data = data.dropna(subset=['geometria']).reset_index(drop=True)
        # data = data.drop_duplicates(subset=['geometria'])
        data = data[data['safra'].isin(safra)]
        data = data[data['ocupacao'] == 'Soja']
        if columns:
            data = data[columns]
        return data
    
    def rd2(self, x):
        return round(x, 2)
        
    def load_data_geometry(self, query_name: str, safra: list, columns: Optional[list[str]] =None) -> Tuple[pd.DataFrame, list[dict]] : 
        self.data = load_create_data(query_name = query_name)
        self.data['geometria'] = self.data['geometria'].replace('''{"type": "Polygon","coordinates":[EMPTY]}''', None)
        data = self.__data_filter(self.data, safra ,columns)
        
        geometria = data['geometria']
        return data, geometria
# ===========================================

class StandardDataProcessor():
    def __init__(self, data=None):
        self.data = data

    def load_data(self, query_name: str) -> pd.DataFrame:   
        self.data = load_create_data(query_name = query_name)
        return self.data
    
    def categorical_encoder(self, data: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
        for col in columns:
            if len(data[col].unique()) > 5:
                le = LabelEncoder()
                data[col] = le.fit_transform(data[col])
            else:
                data = pd.get_dummies(data, columns=[col], dtype=int)
        return data
    
    def Pivoter(self, data, pivot_columns, index, pivot_switch):
        if pivot_switch:
            df_pivoted = data.pivot_table(index=index, 
                                    columns='estadio', 
                                    values=pivot_columns).reset_index()

            df_pivoted.columns = [f"{col[0]}_{col[1]}" if col[1] else col[0] for col in df_pivoted.columns.values]

            data = df_pivoted.copy()
            #dropna with subset of all columns with 'graus_dias_score' in the name
            # data.dropna(subset=[col for col in data.columns if 'graus_dias_score' in col], inplace=True)
            data.dropna(inplace=True)
            # data.drop(columns=['fazenda', 'talhao', 'safra'], inplace=True)
        else:
            data = data.dropna()
        return data