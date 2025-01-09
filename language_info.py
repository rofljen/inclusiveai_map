import streamlit as st
import pandas as pd
from database import get_database_connection, get_language_nmt_pairs, load_language_data
from map_utils import display_map

def get_language_details(language_id):
    """Fetch detailed information about a specific language."""
    engine = get_database_connection()
    query = """
    SELECT 
        ln.*,
        lf.name as family_name,
        lf.id as family_id,
        ls.name as subfamily_name,
        ls.id as subfamily_id,
        ARRAY[
            CASE WHEN ln.asr THEN 'ASR' END,
            CASE WHEN ln.nmt THEN 'NMT' END,
            CASE WHEN ln.tts THEN 'TTS' END
        ] as available_models,
        ST_Y(ST_AsText(ln.coordinates::geometry)) as latitude,
        ST_X(ST_AsText(ln.coordinates::geometry)) as longitude
    FROM language_new ln
    LEFT JOIN language_family lf ON ln.lang_fam_id = lf.id
    LEFT JOIN language_subfamily ls ON ln.lang_sub_id = ls.id
    WHERE ln.id = %(lang_id)s
    """
    try:
        return pd.read_sql_query(query, engine, params={'lang_id': language_id}).iloc[0]
    except Exception as e:
        st.error(f"Error fetching language details: {str(e)}")
        return None

def get_family_languages(family_id):
    """Fetch all languages belonging to a specific language family."""
    engine = get_database_connection()
    query = """
    SELECT lang_name as name, id
    FROM language_new
    WHERE lang_fam_id = %(family_id)s
    ORDER BY lang_name
    """
    return pd.read_sql_query(query, engine, params={'family_id': family_id})

def get_subfamily_languages(subfamily_id):
    """Fetch all languages belonging to a specific language subfamily."""
    engine = get_database_connection()
    query = """
    SELECT lang_name as name, id
    FROM language_new
    WHERE lang_sub_id = %(subfamily_id)s
    ORDER BY lang_name
    """
    return pd.read_sql_query(query, engine, params={'subfamily_id': subfamily_id})

def render_language_info_page(language_id):
    """Render the language information page."""
    try:
        details = get_language_details(language_id)
        if details is None:
            st.error("Language not found")
            return

        # Page title and header
        st.title(f"{details['lang_name']} Language Details")

        # Basic Information Section
        st.header("Basic Information")
        st.markdown(f"""
        **ISO Code:** {details['iso_code'] if pd.notna(details['iso_code']) else 'N/A'}  
        """)

        # Language Classification Section
        st.header("Language Classification")
        if pd.notna(details['family_name']):
            st.markdown(f"**Family:** [{details['family_name']}](?family_id={details['family_id']})")
        if pd.notna(details['subfamily_name']):
            st.markdown(f"**Subfamily:** [{details['subfamily_name']}](?subfamily_id={details['subfamily_id']})")

        # NMT Pairs Section
        nmt_pairs = get_language_nmt_pairs(language_id)
        if not nmt_pairs.empty:
            st.header("Neural Machine Translation Pairs")

            # Summary statistics
            st.markdown(f"""
            ### Overview
            - **Total Translation Pairs:** {len(nmt_pairs)}
            - **Average chrF++ Score:** {nmt_pairs['chrf_score'].mean():.2f}
            - **Average BLEU Score:** {nmt_pairs['bleu_score'].mean():.2f}
            """)

            # Enhanced table view with formatting
            st.markdown("### Translation Pairs")
            st.dataframe(
                nmt_pairs.style.format({
                    'chrf_score': '{:.2f}',
                    'bleu_score': '{:.2f}'
                }).bar(
                    subset=['chrf_score', 'bleu_score'],
                    color='#4CAF50'
                ),
                use_container_width=True
            )

            # Add download functionality
            st.download_button(
                "Download Pairs Data as CSV",
                nmt_pairs.to_csv(index=False).encode('utf-8'),
                f"nmt_pairs_{language_id}.csv",
                "text/csv",
                key='download-pairs'
            )

        # Back button
        st.markdown("---")
        if st.button("← Back to Map"):
            st.session_state.selected_language = None
            st.rerun()

    except Exception as e:
        st.error(f"Error loading language details: {str(e)}")
        if st.button("← Back to Map"):
            st.session_state.selected_language = None
            st.rerun()

def render_family_page(family_id):
    """Render the language family page showing all languages in the family."""
    try:
        languages = get_family_languages(family_id)
        st.title(f"Languages in Family")

        for _, row in languages.iterrows():
            st.markdown(f"- [{row['name']}](?selected_language={row['id']})")

        if st.button("← Back"):
            del st.query_params['family_id']
            st.rerun()

    except Exception as e:
        st.error(f"Error loading family details: {str(e)}")

def render_subfamily_page(subfamily_id):
    """Render the language subfamily page showing all languages in the subfamily."""
    try:
        languages = get_subfamily_languages(subfamily_id)
        st.title(f"Languages in Subfamily")

        for _, row in languages.iterrows():
            st.markdown(f"- [{row['name']}](?selected_language={row['id']})")

        if st.button("← Back"):
            del st.query_params['subfamily_id']
            st.rerun()

    except Exception as e:
        st.error(f"Error loading subfamily details: {str(e)}")