import streamlit as st
import pandas as pd
from database import get_database_connection

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
        ST_Y(ST_AsText(ln.geom)) as latitude,
        ST_X(ST_AsText(ln.geom)) as longitude
    FROM languages ln
    LEFT JOIN language_families lf ON ln.family_id = lf.id
    LEFT JOIN language_subfamilies ls ON ln.subfamily_id = ls.id
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
    SELECT name, id
    FROM languages
    WHERE family_id = %(family_id)s
    ORDER BY name
    """
    return pd.read_sql_query(query, engine, params={'family_id': family_id})

def get_subfamily_languages(subfamily_id):
    """Fetch all languages belonging to a specific language subfamily."""
    engine = get_database_connection()
    query = """
    SELECT name, id
    FROM languages
    WHERE subfamily_id = %(subfamily_id)s
    ORDER BY name
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
        st.title(f"{details['name']} Language Details")

        # Layout with columns
        col1, col2 = st.columns([2, 1])

        with col1:
            # Basic Information Section
            st.header("Basic Information")
            st.markdown(f"""
            **ISO Code:** {details['iso_code'] if pd.notna(details['iso_code']) else 'N/A'}  
            **Glottocode:** {details['glottocode'] if pd.notna(details['glottocode']) else 'N/A'}  
            **Number of Speakers:** {f"{details['speakers']:,}" if pd.notna(details['speakers']) else 'N/A'}  
            **Main City:** {details['main_city'] if pd.notna(details['main_city']) else 'N/A'}  
            **Continent:** {details['continent'] if pd.notna(details['continent']) else 'N/A'}  
            **Geographic Location:** {f"({details['latitude']:.2f}, {details['longitude']:.2f})" if pd.notna(details['latitude']) else 'N/A'}
            """)

            # Language Family Information
            st.header("Language Classification")
            if pd.notna(details['family_name']):
                st.markdown(f"**Family:** [{details['family_name']}](?family_id={details['family_id']})")
            if pd.notna(details['subfamily_name']):
                st.markdown(f"**Subfamily:** [{details['subfamily_name']}](?subfamily_id={details['subfamily_id']})")

            # Language Resources Section
            st.header("Language Resources")
            if pd.notna(details['resources_url']):
                st.markdown(f"[View Available Resources]({details['resources_url']})")
            else:
                st.info("No additional resources available")

        with col2:
            # Model Support Section
            st.header("Model Support")
            models = [m for m in details['available_models'] if m]

            if models:
                for model in models:
                    if model == 'ASR' and details['asr']:
                        st.subheader("🎙️ Speech Recognition (ASR)")
                        metrics = []
                        if pd.notna(details['asr_hours']):
                            metrics.append(f"Training Hours: {details['asr_hours']}")
                        if pd.notna(details['asr_speakers']):
                            metrics.append(f"Unique Speakers: {details['asr_speakers']}")
                        if metrics:
                            st.markdown("\n".join(f"- {m}" for m in metrics))
                        if pd.notna(details['asr_url']):
                            st.markdown(f"[Access Model]({details['asr_url']})")

                    elif model == 'NMT' and details['nmt']:
                        st.subheader("🔄 Machine Translation (NMT)")
                        if pd.notna(details['nmt_pairs']):
                            st.markdown(f"**Translation Pairs:** {details['nmt_pairs']}")
                        if pd.notna(details['nmt_url']):
                            st.markdown(f"[Access Model]({details['nmt_url']})")

                    elif model == 'TTS' and details['tts']:
                        st.subheader("🔊 Text-to-Speech (TTS)")
                        if pd.notna(details['tts_hours']):
                            st.markdown(f"**Training Hours:** {details['tts_hours']}")
                        if pd.notna(details['tts_url']):
                            st.markdown(f"[Access Model]({details['tts_url']})")
            else:
                st.warning("No language models currently available")

        # Additional Information Section
        st.header("Additional Information")
        if pd.notna(details['description']):
            st.markdown(details['description'])
        else:
            st.info("No additional information available")

        # Back button with some spacing
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