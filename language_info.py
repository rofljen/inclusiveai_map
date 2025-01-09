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
            if location_text:
                parts = [part.strip() for part in location_text.split(',')]
                city = parts[0] if parts else None
                # Usually the country is the last meaningful part
                country = parts[-1].strip() if len(parts) > 1 else None
                return city, country
    except Exception:
        return None, None
    return None, None

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
        ST_X(ST_AsText(ln.coordinates::geometry)) as longitude,
        ln.lang_code,
        ln.description,
        ln.endangered_level,
        ln.last_updated
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

        # Create a card-like container for the header
        with st.container():
            st.title(f"{details['lang_name']}")
            if pd.notna(details.get('description')):
                st.markdown(details['description'])
            st.markdown("---")

        # Basic Information Section
        st.header("📋 Basic Information")
        col1, col2, col3 = st.columns([1, 1, 1])

        with col1:
            st.markdown("##### 🌐 Location")
            if pd.notna(details['latitude']) and pd.notna(details['longitude']):
                city, country = get_location_from_coordinates(details['latitude'], details['longitude'])
                location_text = []
                if city:
                    location_text.append(city)
                if country:
                    location_text.append(country)
                if location_text:
                    st.markdown(f"**Region:** {', '.join(location_text)}")
                st.markdown(f"**Coordinates:** ({details['latitude']:.2f}, {details['longitude']:.2f})")

        with col2:
            st.markdown("##### 🏷️ Classification")
            if pd.notna(details['family_name']):
                st.markdown(f"**Family:** [{details['family_name']}](?family_id={details['family_id']})")
            if pd.notna(details['subfamily_name']):
                st.markdown(f"**Subfamily:** [{details['subfamily_name']}](?subfamily_id={details['subfamily_id']})")

        with col3:
            st.markdown("##### 🔍 Identifiers")
            if pd.notna(details['iso_code']):
                st.markdown(f"**ISO Code:** {details['iso_code']}")
            if pd.notna(details['glottocode']):
                st.markdown(f"**Glotto Code:** {details['glottocode']}")
            if pd.notna(details['lang_code']):
                st.markdown(f"**Language Code:** {details['lang_code']}")

        st.markdown("---")

        # Model Availability Section with improved layout
        st.header("🤖 Language Technology")

        # Create three columns for each model type
        tech_col1, tech_col2, tech_col3 = st.columns(3)

        with tech_col1:
            st.markdown("##### Speech Recognition (ASR)")
            if details['asr']:
                st.success("✅ Available")
                if pd.notna(details['asr_url']):
                    st.markdown(f"[Access ASR Model]({details['asr_url']})")
                    st.markdown("Try the model to convert speech to text")
            else:
                st.error("❌ Not Available")

        with tech_col2:
            st.markdown("##### Machine Translation (NMT)")
            if details['nmt']:
                st.success("✅ Available")
                if pd.notna(details['nmt_url']):
                    st.markdown(f"[Access NMT Model]({details['nmt_url']})")
                    st.markdown("Try the model to translate text")
            else:
                st.error("❌ Not Available")

        with tech_col3:
            st.markdown("##### Text-to-Speech (TTS)")
            if details['tts']:
                st.success("✅ Available")
                if pd.notna(details['tts_url']):
                    st.markdown(f"[Access TTS Model]({details['tts_url']})")
                    st.markdown("Try the model to generate speech")
            else:
                st.error("❌ Not Available")

        st.markdown("---")

        # NMT Pairs Section with enhanced visualization
        nmt_pairs = get_language_nmt_pairs(language_id)
        if not nmt_pairs.empty:
            st.header("🔄 Translation Pairs")

            # Summary metrics
            metric_col1, metric_col2, metric_col3 = st.columns(3)
            with metric_col1:
                st.metric("Total Pairs", len(nmt_pairs))
            with metric_col2:
                st.metric("Avg chrF++ Score", f"{nmt_pairs['chrf_score'].mean():.2f}")
            with metric_col3:
                st.metric("Avg BLEU Score", f"{nmt_pairs['bleu_score'].mean():.2f}")

            # Display detailed pairs with enhanced formatting
            st.markdown("### Translation Pair Details")
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
                "📥 Download Translation Pairs Data",
                nmt_pairs.to_csv(index=False).encode('utf-8'),
                f"translation_pairs_{details['lang_name'].lower().replace(' ', '_')}.csv",
                "text/csv",
                key='download-pairs'
            )

        # Meta Information
        if pd.notna(details.get('last_updated')):
            st.markdown("---")
            st.markdown(f"*Last Updated: {details['last_updated']}*")

        # Navigation
        st.markdown("---")
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