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
            WITH ordered_pairs AS (
                SELECT 
                    l1.id as source_id,
                    l2.lang_name as target_name,
                    l2.id as target_id,
                    ARRAY[
                        ST_Y(l2.coordinates::geometry),
                        ST_X(l2.coordinates::geometry)
                    ]::float[] as target_coords,
                    nps.chrf_plus,
                    nps.spbleu_spm_200
                FROM language_new l1
                JOIN nmt_pairs_source nps ON l1.id = nps.source_lang_id OR l1.id = nps.target_lang_id
                JOIN language_new l2 ON 
                    (nps.source_lang_id = l2.id OR nps.target_lang_id = l2.id) AND
                    l2.id != l1.id
                WHERE l2.coordinates IS NOT NULL
                    AND ST_IsValid(l2.coordinates::geometry)
                ORDER BY l2.lang_name
            ),
            lang_connections AS (
                SELECT 
                    source_id as lang_id,
                    array_agg(DISTINCT target_name) as connected_languages,
                    array_agg(DISTINCT target_coords) FILTER (WHERE 
                        target_coords[1] BETWEEN -90 AND 90
                        AND target_coords[2] BETWEEN -180 AND 180
                    ) as connected_coords,
                    array_agg(DISTINCT target_id) as connected_lang_ids,
                    array_agg(DISTINCT chrf_plus) as chrf_scores,
                    array_agg(DISTINCT spbleu_spm_200) as bleu_scores
                FROM ordered_pairs
                GROUP BY source_id
            )
            SELECT 
                l.id,
                l.lang_name as name,
                l.iso_code,
                ST_Y(l.coordinates::geometry) as latitude,
                ST_X(l.coordinates::geometry) as longitude,
                ARRAY[
                    CASE WHEN l.asr THEN 'ASR' END,
                    CASE WHEN l.nmt THEN 'NMT' END,
                    CASE WHEN l.tts THEN 'TTS' END
                ] as available_models,
                (SELECT COUNT(*)
                 FROM nmt_pairs_source nps
                 WHERE nps.source_lang_id = l.id OR nps.target_lang_id = l.id) as nmt_pair_count,
                COALESCE(lc.connected_languages, ARRAY[]::text[]) as connected_languages,
                COALESCE(lc.connected_coords, ARRAY[]::float[][]) as connected_coords,
                COALESCE(lc.connected_lang_ids, ARRAY[]::integer[]) as connected_lang_ids,
                COALESCE(lc.chrf_scores, ARRAY[]::float[]) as chrf_scores,
                COALESCE(lc.bleu_scores, ARRAY[]::float[]) as bleu_scores,
                CASE WHEN lc.lang_id IS NOT NULL THEN TRUE ELSE FALSE END as has_nmt_pair
            FROM language_new l
            LEFT JOIN lang_connections lc ON l.id = lc.lang_id
            WHERE l.coordinates IS NOT NULL
                AND ST_IsValid(l.coordinates::geometry)
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
            nps.chrf_plus as chrf_score,
            nps.spbleu_spm_200 as bleu_score,
            source_lang.lang_name AS source_language,
            target_lang.lang_name AS target_language,
            CASE 
                WHEN source_lang.id = :lang_id THEN 'Source'
                ELSE 'Target'
            END as role
        FROM 
            nmt_pairs_source nps
        LEFT JOIN 
            language_new AS source_lang 
        ON 
            nps.source_lang_id = source_lang.id
        LEFT JOIN 
            language_new AS target_lang 
        ON 
            nps.target_lang_id = target_lang.id
        WHERE 
            nps.source_lang_id IS NOT NULL
            AND nps.target_lang_id IS NOT NULL
            AND (source_lang.id = :lang_id OR target_lang.id = :lang_id)
        ORDER BY 
            role, nps.chrf_plus DESC NULLS LAST;
        """
        return pd.read_sql(text(query), connection, params={'lang_id': language_id})

@st.cache_data
def get_all_nmt_pairs():
    """Get all NMT pairs with their scores."""
    with get_db_session() as connection:
        query = """
        SELECT 
            nps.chrf_plus as chrf_score,
            nps.spbleu_spm_200 as bleu_score,
            source_lang.lang_name AS source_language,
            target_lang.lang_name AS target_language
        FROM 
            nmt_pairs_source nps
        LEFT JOIN 
            language_new AS source_lang 
        ON 
            nps.source_lang_id = source_lang.id
        LEFT JOIN 
            language_new AS target_lang 
        ON 
            nps.target_lang_id = target_lang.id
        WHERE 
            nps.source_lang_id IS NOT NULL
            AND nps.target_lang_id IS NOT NULL
        ORDER BY 
            nps.chrf_plus DESC NULLS LAST;
        """
        return pd.read_sql(query, connection)