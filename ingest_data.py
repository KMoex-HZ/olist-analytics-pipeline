import os
import pandas as pd
from sqlalchemy import create_engine

# Database Configuration (Ensure this matches your docker-compose.yml)
DB_USER = 'caelan_admin'
DB_PASSWORD = 'password_rahasia'
DB_HOST = 'localhost'
DB_PORT = '5432'
DB_NAME = 'olist_db'

# Establish PostgreSQL connection
engine = create_engine(f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

def ingest_csv():
    """
    Scans the data directory for CSV files and ingests them into PostgreSQL tables.
    Table names are derived from filenames for better schema organization.
    """
    data_dir = './data'
    # Filter for all files with a .csv extension
    files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    for file in files:
        # Standardize table names by removing file extensions and common prefixes/suffixes
        table_name = file.replace('.csv', '').replace('olist', '').replace('dataset', '').strip('_')
        file_path = os.path.join(data_dir, file)
        
        print(f"🚀 Ingesting data from {file} into table: {table_name}...")
        
        # Load CSV into a Pandas DataFrame
        df = pd.read_csv(file_path)
        
        # Load DataFrame to PostgreSQL
        # if_exists='replace' ensures a clean state by overwriting existing tables
        df.to_sql(table_name, engine, if_exists='replace', index=False)
        
        print(f"✅ Table '{table_name}' successfully created! ({len(df)} rows)")

if __name__ == "__main__":
    try:
        ingest_csv()
        print("\n🔥 DATA INGESTION COMPLETE: Data warehouse is ready for processing.")
    except Exception as e:
        print(f"❌ Critical Error during ingestion: {e}")