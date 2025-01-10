import streamlit as st
import pandas as pd
import altair as alt
from database import get_database_connection
import trafilatura
import urllib.parse

@st.cache_data
def get_language_nmt_pairs(language_id):
    """Get NMT pairs for a specific language."""
    engine = get_database_connection()
    query = """
    SELECT 
        nps.chrf_plus as chrf_score,
        nps.spbleu_spm_200 as bleu_score,
        source_lang.lang_name AS source_language,
        target_lang.lang_name AS target_language,
        CASE 
            WHEN source_lang.id = %(lang_id)s THEN 'Source'
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
        AND (source_lang.id = %(lang_id)s OR target_lang.id = %(lang_id)s)
    ORDER BY 
        role, nps.chrf_plus DESC NULLS LAST;
    """
    return pd.read_sql_query(query, engine, params={'lang_id': language_id})

def get_location_from_coordinates(lat, lon):
    """Get location information from coordinates using OpenStreetMap Nominatim."""
    try:
        url = f"https://nominatim.openstreetmap.org/reverse?format=xml&lat={lat}&lon={lon}"
        downloaded = trafilatura.fetch_url(url)
        if downloaded:
            location_text = trafilatura.extract(downloaded)
            if location_text:
                parts = [part.strip() for part in location_text.split(',')]
                city = parts[0] if parts else None
                country = parts[-1].strip() if len(parts) > 1 else None
                return city, country
    except Exception:
        return None, None
    return None, None

def create_score_chart(nmt_pairs):
    """Create an interactive chart for NMT pair scores."""
    # Prepare data for visualization
    chart_data = pd.melt(
        nmt_pairs,
        id_vars=['source_language', 'target_language'],
        value_vars=['chrf_score', 'bleu_score'],
        var_name='metric',
        value_name='score'
    )

    # Create interactive chart
    chart = alt.Chart(chart_data).mark_bar().encode(
        x=alt.X('target_language:N', sort='-y', title='Target Language'),
        y=alt.Y('score:Q', title='Score'),
        color=alt.Color('metric:N', 
            scale=alt.Scale(scheme='category10'),
            legend=alt.Legend(title='Metric')
        ),
        tooltip=[
            alt.Tooltip('target_language:N', title='Language'),
            alt.Tooltip('score:Q', format='.2f'),
            alt.Tooltip('metric:N', title='Metric')
        ]
    ).properties(
        width='container',
        height=300,
        title='Translation Quality Scores by Target Language'
    ).interactive()

    return chart

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
    """Render the enhanced language information page with interactive elements."""
    try:
        details = get_language_details(language_id)
        if details is None:
            st.error("Language not found")
            return

        # Header Section
        with st.container():
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.title(f"{details['lang_name']}")
            with col2:
                if st.button("← Back to Map", type="secondary"):
                    st.session_state.selected_language = None
                    st.rerun()

        # Tabs for different sections
        tabs = st.tabs(["Overview", "Language Technology", "Translation Pairs"])

        # Overview Tab
        with tabs[0]:
            col1, col2 = st.columns([1, 1])

            with col1:
                with st.container():
                    st.markdown("##### 🌐 Location and Geography")
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
                with st.container():
                    st.markdown("##### 🏷️ Classification and Identifiers")
                    if pd.notna(details['family_name']):
                        st.markdown(f"**Family:** [{details['family_name']}](?family_id={details['family_id']})")
                    if pd.notna(details['subfamily_name']):
                        st.markdown(f"**Subfamily:** [{details['subfamily_name']}](?subfamily_id={details['subfamily_id']})")
                    if pd.notna(details['iso_code']):
                        st.markdown(f"**ISO Code:** {details['iso_code']}")
                    if pd.notna(details['glottocode']):
                        st.markdown(f"**Glotto Code:** {details['glottocode']}")

        # Language Technology Tab
        with tabs[1]:
            tech_col1, tech_col2, tech_col3 = st.columns(3)

            with tech_col1:
                with st.container():
                    st.markdown("##### Speech Recognition (ASR)")
                    if details['asr']:
                        st.markdown('<div class="status-indicator status-available">✓ Available</div>', unsafe_allow_html=True)
                        if pd.notna(details['asr_url']):
                            st.markdown(f"[Try ASR Model]({details['asr_url']})")
                    else:
                        st.markdown('<div class="status-indicator status-unavailable">✗ Not Available</div>', unsafe_allow_html=True)

            with tech_col2:
                with st.container():
                    st.markdown("##### Machine Translation (NMT)")
                    if details['nmt']:
                        st.markdown('<div class="status-indicator status-available">✓ Available</div>', unsafe_allow_html=True)
                        if pd.notna(details['nmt_url']):
                            st.markdown(f"[Try NMT Model]({details['nmt_url']})")
                    else:
                        st.markdown('<div class="status-indicator status-unavailable">✗ Not Available</div>', unsafe_allow_html=True)

            with tech_col3:
                with st.container():
                    st.markdown("##### Text-to-Speech (TTS)")
                    if details['tts']:
                        st.markdown('<div class="status-indicator status-available">✓ Available</div>', unsafe_allow_html=True)
                        if pd.notna(details['tts_url']):
                            st.markdown(f"[Try TTS Model]({details['tts_url']})")
                    else:
                        st.markdown('<div class="status-indicator status-unavailable">✗ Not Available</div>', unsafe_allow_html=True)

        # Translation Pairs Tab
        with tabs[2]:
            nmt_pairs = get_language_nmt_pairs(language_id)
            if not nmt_pairs.empty:
                # Summary metrics
                metric_col1, metric_col2, metric_col3 = st.columns(3)
                with metric_col1:
                    st.metric("Total Pairs", len(nmt_pairs))
                with metric_col2:
                    st.metric("Avg chrF++ Score", f"{nmt_pairs['chrf_score'].mean():.2f}")
                with metric_col3:
                    st.metric("Avg BLEU Score", f"{nmt_pairs['bleu_score'].mean():.2f}")

                # Interactive chart
                st.markdown("### Score Distribution")
                with st.container():
                    chart = create_score_chart(nmt_pairs)
                    st.altair_chart(chart, use_container_width=True)

                # Detailed pairs table
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

                # Download button
                st.download_button(
                    "📥 Download Translation Pairs Data",
                    nmt_pairs.to_csv(index=False).encode('utf-8'),
                    f"translation_pairs_{details['lang_name'].lower().replace(' ', '_')}.csv",
                    "text/csv",
                    key='download-pairs'
                )
            else:
                st.info("No translation pairs available for this language.")

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please check your database connection and try again.")

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