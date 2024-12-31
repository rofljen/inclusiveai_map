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
        l.id,
        l.lang_name as name,
        l.iso_code,
        NULLIF(ST_Y(l.coordinates::geometry), 'NaN') as latitude,
        NULLIF(ST_X(l.coordinates::geometry), 'NaN') as longitude,
        ARRAY[
            CASE WHEN l.asr THEN 'ASR' END,
            CASE WHEN l.nmt THEN 'NMT' END,
            CASE WHEN l.tts THEN 'TTS' END
        ] as available_models
    FROM language_new l
    WHERE l.coordinates IS NOT NULL
        AND ST_X(l.coordinates::geometry) IS NOT NULL 
        AND ST_Y(l.coordinates::geometry) IS NOT NULL
        AND ST_X(l.coordinates::geometry) BETWEEN -180 AND 180
        AND ST_Y(l.coordinates::geometry) BETWEEN -90 AND 90
    ORDER BY l.lang_name
    """
    return pd.read_sql(query, engine)

@st.cache_data
def get_model_types():
    """Get unique model types from database."""
    return ['ASR', 'NMT', 'TTS']