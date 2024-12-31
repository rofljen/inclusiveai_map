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
        ] as available_models,
        ST_Y(ST_AsText(coordinates::geometry)) as latitude,
        ST_X(ST_AsText(coordinates::geometry)) as longitude
    FROM language_new ln
    WHERE ln.id = %(lang_id)s
    """
    try:
        return pd.read_sql_query(query, engine, params={'lang_id': language_id}).iloc[0]
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

        # Page title and header
        st.title(f"{details['lang_name']} Language Details")

        # Layout with columns
        col1, col2 = st.columns([2, 1])

        with col1:
            # Basic Information Section
            st.header("Basic Information")
            st.markdown(f"""
            **ISO Code:** {details['iso_code'] if pd.notna(details['iso_code']) else 'N/A'}  
            **Glottocode:** {details['glottocode'] if pd.notna(details['glottocode']) else 'N/A'}  
            **Geographic Location:** {f"({details['latitude']:.2f}, {details['longitude']:.2f})" if pd.notna(details['latitude']) else 'N/A'}
            """)

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