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
        ls.name as subfamily_name,
        c.name as continent_name
    FROM language_new ln
    LEFT JOIN language_family lf ON ln.lang_fam_id = lf.id
    LEFT JOIN language_subfamily ls ON ln.lang_sub_id = ls.id
    LEFT JOIN continent c ON ln.continent_id = c.id
    WHERE ln.id = %s
    """
    return pd.read_sql_query(query, engine, params=[language_id]).iloc[0]

def render_language_info_page(language_id):
    """Render the language information page."""
    try:
        details = get_language_details(language_id)
        
        st.title(f"{details['lang_name']} Language Details")
        
        # Basic Information
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Basic Information")
            st.markdown(f"**ISO Code:** {details['iso_code'] or 'N/A'}")
            st.markdown(f"**Glottocode:** {details['glottocode'] or 'N/A'}")
            st.markdown(f"**Family:** {details['family_name'] or 'N/A'}")
            st.markdown(f"**Subfamily:** {details['subfamily_name'] or 'N/A'}")
            st.markdown(f"**Continent:** {details['continent_name'] or 'N/A'}")
        
        with col2:
            st.subheader("Model Availability")
            if details['asr']:
                st.markdown("✅ **ASR** (Automatic Speech Recognition)")
                if details['asr_hours']:
                    st.markdown(f"- Training Hours: {details['asr_hours']}")
                if details['asr_url']:
                    st.markdown(f"- [Model Link]({details['asr_url']})")
            
            if details['nmt']:
                st.markdown("✅ **NMT** (Neural Machine Translation)")
                if details['nmt_url']:
                    st.markdown(f"- [Model Link]({details['nmt_url']})")
                if details['nmt_pairs']:
                    st.markdown(f"- Translation Pairs: {details['nmt_pairs']}")
            
            if details['tts']:
                st.markdown("✅ **TTS** (Text-to-Speech)")
                if details['tts_url']:
                    st.markdown(f"- [Model Link]({details['tts_url']})")

        # Back button
        if st.button("← Back to Map"):
            st.session_state.selected_language = None
            st.experimental_rerun()

    except Exception as e:
        st.error(f"Error loading language details: {str(e)}")
        if st.button("← Back to Map"):
            st.session_state.selected_language = None
            st.experimental_rerun()
