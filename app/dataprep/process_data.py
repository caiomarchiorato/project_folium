from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
import pandas as pd

class DateProcessor(BaseEstimator, TransformerMixin):
    def __init__(self, columns_date: list[str]=None):
        self.columns_date = columns_date
        
    def fit(self, X: pd.DataFrame, y=None):
        return self
    
    def transform(self, X: pd.DataFrame):
        X = X.copy()
        for column in self.columns_date:
            if column in X.columns:
                X[column] = pd.to_datetime(X[column], format='%Y-%m-%d').dt.dayofyear
        return X
    
class Pivoter(BaseEstimator, TransformerMixin):
    def __init__(self, pivot_columns: list[str], index: list[str], pivot_switch: bool):
        self.pivot_columns = pivot_columns
        self.index = index
        self.pivot_switch = pivot_switch
        
    def fit(self, X: pd.DataFrame, y=None):
        return self
    
    def transform(self, X: pd.DataFrame):
        X = X.copy()
        if self.pivot_switch:
            df_pivoted = X.pivot_table(index=self.index, 
                                    columns='estadio', 
                                    values=self.pivot_columns).reset_index()
            df_pivoted.columns = [f"{col[0]}_{col[1]}" if col[1] else col[0] for col in df_pivoted.columns.values]
            X = df_pivoted.copy()
            # X.drop(columns=['fazenda','setor','talhao'], inplace=True)
            X.dropna(inplace=True)
        else:
            X = X.dropna()
        return X

class DropNan(BaseEstimator, TransformerMixin):    
    def fit(self, X: pd.DataFrame, y=None):
        return self
    
    def transform(self, X: pd.DataFrame):
        X = X.copy()
        X.dropna(inplace=True)
        return X

class CategoricalEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, columns: list[str]=None):
        self.columns = columns
    
    def fit(self, X: pd.DataFrame, y=None):
        return self
    
    def transform(self, X: pd.DataFrame):
        X = X.copy()
        for col in self.columns:
            if len(X[col].unique()) > 5:
                le = LabelEncoder()
                X[col] = le.fit_transform(X[col])
            else:
                X = pd.get_dummies(X, columns=[col], dtype=int)
        return X
    
class SelectiveScaler(BaseEstimator, TransformerMixin):
    def __init__(self, exclude_columns: list[str]=None):
        self.exclude_columns = exclude_columns if exclude_columns is not None else []
        self.scaler = StandardScaler()
    
    def fit(self, X: pd.DataFrame, y=None):
        self.columns_to_scale = [col for col in X.columns if col not in self.exclude_columns]
        if self.columns_to_scale:
            self.scaler.fit(X[self.columns_to_scale])
        return self
    
    def transform(self, X: pd.DataFrame):
        X = X.copy()
        if self.columns_to_scale:
            X[self.columns_to_scale] = self.scaler.transform(X[self.columns_to_scale])
        return X
    