import streamlit as st
import pandas as pd
from database import get_database_connection, get_language_nmt_pairs
import trafilatura
import urllib.parse

def get_location_from_coordinates(lat, lon):
    """Get location information from coordinates using OpenStreetMap Nominatim."""
    try:
        # Use OpenStreetMap Nominatim to get location info
        url = f"https://nominatim.openstreetmap.org/reverse?format=xml&lat={lat}&lon={lon}"
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            location_text = trafilatura.extract(downloaded)
            return location_text.split(',')[0] if location_text else None
    except Exception:
        return None

def get_language_details(language_id):
    """Fetch detailed information about a specific language."""
    engine = get_database_connection()
    query = """
    SELECT 
        ln.id,
        ln.lang_name,
        ln.iso_code,
        ln.glottocode,
        lf.name as family_name,
        lf.id as family_id,
        ls.name as subfamily_name,
        ls.id as subfamily_id,
        ln.asr,
        ln.nmt,
        ln.tts,
        ln.asr_url,
        ln.nmt_url,
        ln.tts_url,
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

        # Page title
        st.title(f"{details['lang_name']}")

        # Basic Information Section
        col1, col2 = st.columns(2)
        with col1:
            if pd.notna(details['latitude']) and pd.notna(details['longitude']):
                location = get_location_from_coordinates(details['latitude'], details['longitude'])
                if location:
                    st.markdown(f"**Location:** {location}")
                else:
                    st.markdown(f"**Coordinates:** ({details['latitude']:.2f}, {details['longitude']:.2f})")
            st.markdown(f"**Glotto Code:** {details['glottocode'] if pd.notna(details['glottocode']) else 'N/A'}")

        # Language Classification
        with col2:
            if pd.notna(details['family_name']):
                st.markdown(f"**Family:** [{details['family_name']}](?family_id={details['family_id']})")
            if pd.notna(details['subfamily_name']):
                st.markdown(f"**Subfamily:** [{details['subfamily_name']}](?subfamily_id={details['subfamily_id']})")

        # Model Availability Section
        st.header("Available Models")
        model_col1, model_col2, model_col3 = st.columns(3)

        with model_col1:
            if details['asr']:
                st.success("🎙️ ASR Available")
                if pd.notna(details['asr_url']):
                    st.markdown(f"[Access ASR Model]({details['asr_url']})")
            else:
                st.error("🎙️ ASR Not Available")

        with model_col2:
            if details['nmt']:
                st.success("🔄 NMT Available")
                if pd.notna(details['nmt_url']):
                    st.markdown(f"[Access NMT Model]({details['nmt_url']})")
            else:
                st.error("🔄 NMT Not Available")

        with model_col3:
            if details['tts']:
                st.success("🔊 TTS Available")
                if pd.notna(details['tts_url']):
                    st.markdown(f"[Access TTS Model]({details['tts_url']})")
            else:
                st.error("🔊 TTS Not Available")

        # NMT Pairs Section
        nmt_pairs = get_language_nmt_pairs(language_id)
        if not nmt_pairs.empty:
            st.header("Translation Pairs")
            # Display the pairs table with formatting
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
                "Download as CSV",
                nmt_pairs.to_csv(index=False).encode('utf-8'),
                f"nmt_pairs_{language_id}.csv",
                "text/csv",
                key='download-pairs'
            )

        # Back button
        if st.button("← Back to Map"):
            st.session_state.selected_language = None
            st.rerun()

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please check your database connection and try again.")
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