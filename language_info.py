import streamlit as st
import pandas as pd
from database import get_database_connection, get_language_nmt_pairs, load_language_data, display_map


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

        # Layout with columns
        col1, col2 = st.columns([2, 1])

        with col1:
            # Basic Information Section
            st.header("Basic Information")
            st.markdown(f"""
            **ISO Code:** {details['iso_code'] if pd.notna(details['iso_code']) else 'N/A'}  
            **Geographic Location:** {f"({details['latitude']:.2f}, {details['longitude']:.2f})" if pd.notna(details['latitude']) else 'N/A'}
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

                # Create tabs for different views
                tabs = st.tabs(["Table View", "Chart View"])

                with tabs[0]:
                    # Table view
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

                with tabs[1]:
                    # Chart view
                    st.bar_chart(
                        nmt_pairs.set_index('target_language')['chrf_score'],
                        use_container_width=True
                    )

                # Detailed list view
                st.subheader("Detailed Pairs Information")
                for _, pair in nmt_pairs.iterrows():
                    quality = "★" * int((pair['chrf_score'] or 0) * 5 / 100)
                    st.markdown(f"""
                    - **{pair['source_language']} ↔ {pair['target_language']}**  
                      Quality: {quality} ({pair['chrf_score']:.1f}%)  
                      BLEU Score: {pair['bleu_score']:.1f}
                    """)

        with col2:
            # Model Support Section
            st.header("Model Support")
            models = [m for m in details['available_models'] if m]

            if models:
                for model in models:
                    if model == 'ASR' and details['asr']:
                        st.subheader("🎙️ Speech Recognition (ASR)")
                        if pd.notna(details['asr_url']):
                            st.markdown(f"[Access Model]({details['asr_url']})")

                    elif model == 'NMT' and details['nmt']:
                        st.subheader("🔄 Machine Translation (NMT)")
                        if pd.notna(details['nmt_url']):
                            st.markdown(f"[Access Model]({details['nmt_url']})")

                    elif model == 'TTS' and details['tts']:
                        st.subheader("🔊 Text-to-Speech (TTS)")
                        if pd.notna(details['tts_url']):
                            st.markdown(f"[Access Model]({details['tts_url']})")
            else:
                st.warning("No language models currently available")

            # Add a map showing connections
            if not nmt_pairs.empty:
                st.header("Translation Connections")
                display_map(
                    load_language_data(), 
                    selected_models=['NMT'],
                    selected_language_id=language_id
                )

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