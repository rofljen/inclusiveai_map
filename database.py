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
        id,
        lang_name as name,
        iso_code,
        ST_Y(ST_SetSRID(coordinates::geometry, 4326)) as latitude,
        ST_X(ST_SetSRID(coordinates::geometry, 4326)) as longitude,
        ARRAY[
            CASE WHEN asr THEN 'ASR' END,
            CASE WHEN nmt THEN 'NMT' END,
            CASE WHEN tts THEN 'TTS' END
        ] as available_models
    FROM language_new
    WHERE coordinates IS NOT NULL
    """
    return pd.read_sql(query, engine)

@st.cache_data
def get_model_types():
    """Get unique model types from database."""
    return ['ASR', 'NMT', 'TTS']