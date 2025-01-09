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

                # Display total number of pairs and summary statistics
                st.markdown(f"""
                ### Overview
                - **Total Translation Pairs:** {len(nmt_pairs)}
                - **Average chrF++ Score:** {nmt_pairs['chrf_score'].mean():.2f}
                - **Average BLEU Score:** {nmt_pairs['bleu_score'].mean():.2f}
                - **Best Performing Pair:** {nmt_pairs.iloc[0]['source_language']} ↔ {nmt_pairs.iloc[0]['target_language']} 
                  (chrF++: {nmt_pairs.iloc[0]['chrf_score']:.2f}, BLEU: {nmt_pairs.iloc[0]['bleu_score']:.2f})
                """)

                # Create tabs for different views
                tabs = st.tabs(["Detailed View", "Table View", "Chart View"])

                with tabs[0]:
                    # Create a grid layout for pairs
                    for _, pair in nmt_pairs.iterrows():
                        with st.container():
                            st.markdown(f"""
                            <div style="border: 1px solid #ddd; padding: 15px; border-radius: 5px; margin-bottom: 10px;">
                                <h4 style="color: #2c3e50; margin-bottom: 10px;">
                                    {pair['source_language']} ↔ {pair['target_language']}
                                </h4>
                                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 15px;">
                                    <div>
                                        <strong>chrF++ Score</strong>
                                        <div style="font-size: 24px; color: {'#4CAF50' if pair['chrf_score'] >= 30 else '#FFA726' if pair['chrf_score'] >= 20 else '#EF5350'}">
                                            {pair['chrf_score']:.2f}
                                        </div>
                                    </div>
                                    <div>
                                        <strong>BLEU Score</strong>
                                        <div style="font-size: 24px; color: {'#4CAF50' if pair['bleu_score'] >= 15 else '#FFA726' if pair['bleu_score'] >= 10 else '#EF5350'}">
                                            {pair['bleu_score']:.2f}
                                        </div>
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                with tabs[1]:
                    # Enhanced table view with formatting
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

                with tabs[2]:
                    # Create two columns for charts
                    chart_col1, chart_col2 = st.columns(2)

                    with chart_col1:
                        st.subheader("chrF++ Scores")
                        st.bar_chart(
                            nmt_pairs.set_index('target_language')['chrf_score'],
                            use_container_width=True
                        )

                    with chart_col2:
                        st.subheader("BLEU Scores")
                        st.bar_chart(
                            nmt_pairs.set_index('target_language')['bleu_score'],
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

            # Map showing connections
            st.header("Translation Connections Map")
            df = load_language_data()
            display_map(df, selected_models=['NMT'], selected_language_id=language_id)

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