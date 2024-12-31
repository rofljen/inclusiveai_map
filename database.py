import os
import pandas as pd
from sqlalchemy import create_engine, text
import streamlit as st
from contextlib import contextmanager

@st.cache_resource
def get_database_connection():
    """Create database connection using environment variables."""
    connection_string = os.getenv('DATABASE_URL')
    if not connection_string:
        connection_string = (
            f"postgresql://{os.getenv('PGUSER')}:{os.getenv('PGPASSWORD')}@"
            f"{os.getenv('PGHOST')}:{os.getenv('PGPORT')}/{os.getenv('PGDATABASE')}"
        )
    return create_engine(connection_string, pool_pre_ping=True)

@contextmanager
def get_db_session():
    """Context manager for database sessions."""
    engine = get_database_connection()
    connection = engine.connect()
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

@st.cache_data
def load_language_data():
    """Load language data from PostgreSQL database with NMT pair information."""
    with get_db_session() as connection:
        query = """
        WITH lang_connections AS (
            SELECT 
                l1.id as lang_id,
                string_agg(DISTINCT l2.lang_name, ', ' ORDER BY l2.lang_name) as connected_languages,
                array_agg(DISTINCT ARRAY[CAST(l2.latitude AS float), CAST(l2.longitude AS float)]) as connected_coords
            FROM language_new l1
            JOIN nmt_pairs_source nps ON l1.id = nps.source_lang_id OR l1.id = nps.target_lang_id
            JOIN language_new l2 ON 
                (nps.source_lang_id = l2.id OR nps.target_lang_id = l2.id) AND
                l2.id != l1.id
            GROUP BY l1.id
        )
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
            ] as available_models,
            (SELECT COUNT(*)
             FROM nmt_pairs_source nps
             WHERE nps.source_lang_id = l.id OR nps.target_lang_id = l.id) as nmt_pair_count,
            COALESCE(lc.connected_languages, '') as connected_languages,
            COALESCE(lc.connected_coords, ARRAY[]::float[][]) as connected_lang_coords,
            EXISTS (
                SELECT 1 
                FROM nmt_pairs_source nps 
                WHERE nps.source_lang_id = l.id OR nps.target_lang_id = l.id
            ) as has_nmt_pair
        FROM language_new l
        LEFT JOIN lang_connections lc ON l.id = lc.lang_id
        WHERE l.coordinates IS NOT NULL
            AND ST_X(l.coordinates::geometry) IS NOT NULL 
            AND ST_Y(l.coordinates::geometry) IS NOT NULL
            AND ST_X(l.coordinates::geometry) BETWEEN -180 AND 180
            AND ST_Y(l.coordinates::geometry) BETWEEN -90 AND 90
        ORDER BY l.lang_name
        """
        return pd.read_sql(query, connection)

@st.cache_data
def get_model_types():
    """Get unique model types from database."""
    return ['ASR', 'NMT', 'TTS']

@st.cache_data
def get_language_nmt_pairs(language_id):
    """Get NMT pairs for a specific language."""
    with get_db_session() as connection:
        query = """
        SELECT 
            src.lang_name as source_language,
            tgt.lang_name as target_language,
            nps.chrf_plus as chrf_score,
            nps.spbleu_spm_200 as bleu_score
        FROM nmt_pairs_source nps
        JOIN language_new src ON nps.source_lang_id = src.id
        JOIN language_new tgt ON nps.target_lang_id = tgt.id
        WHERE nps.source_lang_id = :lang_id OR nps.target_lang_id = :lang_id
        ORDER BY nps.chrf_plus DESC NULLS LAST
        """
        return pd.read_sql(text(query), connection, params={'lang_id': language_id})

@st.cache_data
def get_all_nmt_pairs():
    """Get all NMT pairs with their scores."""
    with get_db_session() as connection:
        query = """
        SELECT 
            src.lang_name as source_language,
            tgt.lang_name as target_language,
            nps.chrf_plus as chrf_score,
            nps.spbleu_spm_200 as bleu_score
        FROM nmt_pairs_source nps
        JOIN language_new src ON nps.source_lang_id = src.id
        JOIN language_new tgt ON nps.target_lang_id = tgt.id
        ORDER BY nps.chrf_plus DESC NULLS LAST
        """
        return pd.read_sql(query, connection)