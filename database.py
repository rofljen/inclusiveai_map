import os
import pandas as pd
from sqlalchemy import create_engine
import streamlit as st

@st.cache_resource
def get_database_connection():
    """Create database connection using environment variables."""
    connection_string = os.getenv('DATABASE_URL')
    if not connection_string:
        connection_string = (
            f"postgresql://{os.getenv('PGUSER')}:{os.getenv('PGPASSWORD')}@"
            f"{os.getenv('PGHOST')}:{os.getenv('PGPORT')}/{os.getenv('PGDATABASE')}"
        )
    return create_engine(connection_string)

@st.cache_data
def load_language_data():
    """Load language data from PostgreSQL database."""
    engine = get_database_connection()
    query = """
    SELECT 
        languages.id,
        languages.name,
        languages.iso_code,
        languages.latitude,
        languages.longitude,
        array_agg(DISTINCT model_types.name) as available_models
    FROM languages
    LEFT JOIN language_models ON languages.id = language_models.language_id
    LEFT JOIN model_types ON language_models.model_type_id = model_types.id
    GROUP BY languages.id, languages.name, languages.iso_code, 
             languages.latitude, languages.longitude
    """
    return pd.read_sql(query, engine)

@st.cache_data
def get_model_types():
    """Get unique model types from database."""
    engine = get_database_connection()
    query = "SELECT DISTINCT name FROM model_types ORDER BY name"
    return pd.read_sql(query, engine)['name'].tolist()
