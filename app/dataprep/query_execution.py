import os
import pandas as pd
from pyathena import connect

def load_env_variables(filename):
    variables = {}
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                key, value = line.split('=', 1)
                variables[key.strip()] = value.strip()
    return variables

def execute_query(query_path: str):
    env_variables = load_env_variables('app/dataprep/.env')

    S3_STAGING_DIR = env_variables.get('S3_STAGING_DIR')
    AWS_ACCESS_KEY = env_variables.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET_KEY = env_variables.get('AWS_SECRET_ACCESS_KEY')
    AWS_REGION = env_variables.get('AWS_REGION')
    try:
        with open(query_path, 'r') as file:
            sql_query = file.read()
        conn = connect(aws_access_key_id=AWS_ACCESS_KEY,
                    aws_secret_access_key=AWS_SECRET_KEY,
                    region_name=AWS_REGION,
                    s3_staging_dir=S3_STAGING_DIR)
        
        cursor = conn.cursor()
        cursor.execute(sql_query)
        
        col_names = [col[0] for col in cursor.description]
        results = cursor.fetchall()
        
        return col_names, results
    except Exception as e:
        print(e)
        return None, None

def create_dataframe_from_query(sql_query: str) -> pd.DataFrame:
    #importando os resultados 
    try:
        col_names, result = execute_query(sql_query)
        if col_names and result:
            df = pd.DataFrame(result, columns=col_names)
            return df
    except Exception as e:
        print(e)
        return None

def load_create_data(query_name):
    if not os.path.exists('app/data/csv'):
        os.makedirs('data/csv')
    csv_filepath = f'app/data/csv/{query_name}.csv'
    try:
        if not os.path.exists(csv_filepath):
            data = create_dataframe_from_query(f'data/{query_name}.sql')
            data.to_csv(csv_filepath, index=False)
        else:
            print(f"Arquivo {csv_filepath} já existe.")
            data = pd.read_csv(csv_filepath)
        return data
    except Exception as e:
        print(f"Erro ao criar o arquivo csv: {e}")
