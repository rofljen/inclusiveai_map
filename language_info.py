import streamlit as st
import pandas as pd
from database import get_database_connection

def get_language_details(language_id):
    """Fetch detailed information about a specific language."""
    engine = get_database_connection()
    query = """
    SELECT 
        ln.*,
        ARRAY[
            CASE WHEN asr THEN 'ASR' END,
            CASE WHEN nmt THEN 'NMT' END,
            CASE WHEN tts THEN 'TTS' END
        ] as available_models
    FROM language_new ln
    WHERE ln.id = %s
    """
    try:
        return pd.read_sql_query(query, engine, params=[language_id]).iloc[0]
    except Exception as e:
        st.error(f"Error fetching language details: {str(e)}")
        return None

def render_language_info_page(language_id):
    """Render the language information page."""
    try:
        details = get_language_details(language_id)
        if details is None:
            st.error("Language not found")
            return

        st.title(f"{details['lang_name']} Language Details")

        # Basic Information
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Basic Information")
            st.markdown(f"**ISO Code:** {details['iso_code'] if pd.notna(details['iso_code']) else 'N/A'}")
            if pd.notna(details['glottocode']):
                st.markdown(f"**Glottocode:** {details['glottocode']}")

        with col2:
            st.subheader("Model Availability")
            models = [m for m in details['available_models'] if m]
            if models:
                for model in models:
                    if model == 'ASR' and details['asr']:
                        st.markdown("✅ **ASR** (Automatic Speech Recognition)")
                        if pd.notna(details['asr_hours']):
                            st.markdown(f"- Training Hours: {details['asr_hours']}")
                        if pd.notna(details['asr_url']):
                            st.markdown(f"- [Model Link]({details['asr_url']})")

                    elif model == 'NMT' and details['nmt']:
                        st.markdown("✅ **NMT** (Neural Machine Translation)")
                        if pd.notna(details['nmt_url']):
                            st.markdown(f"- [Model Link]({details['nmt_url']})")
                        if pd.notna(details['nmt_pairs']):
                            st.markdown(f"- Translation Pairs: {details['nmt_pairs']}")

                    elif model == 'TTS' and details['tts']:
                        st.markdown("✅ **TTS** (Text-to-Speech)")
                        if pd.notna(details['tts_url']):
                            st.markdown(f"- [Model Link]({details['tts_url']})")
            else:
                st.info("No models available for this language")

        # Back button
        if st.button("← Back to Map"):
            st.session_state.selected_language = None
            st.rerun()

    except Exception as e:
        st.error(f"Error loading language details: {str(e)}")
        if st.button("← Back to Map"):
            st.session_state.selected_language = None
            st.rerun()