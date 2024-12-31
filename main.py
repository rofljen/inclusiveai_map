import streamlit as st
from database import load_language_data, get_model_types, get_all_nmt_pairs
from map_utils import display_map
from components import render_model_filters, render_statistics
from styles import apply_custom_styles
from language_info import render_language_info_page, render_family_page, render_subfamily_page
from db_utils import handle_backup_upload

def render_nmt_pairs_page():
    """Render the page showing all NMT pairs."""
    st.title("Neural Machine Translation Pairs")

    # Get all NMT pairs
    pairs_df = get_all_nmt_pairs()

    # Add search/filter functionality
    search = st.text_input("Search for language pairs", "")

    # Filter based on search
    if search:
        pairs_df = pairs_df[
            pairs_df['source_language'].str.contains(search, case=False) |
            pairs_df['target_language'].str.contains(search, case=False)
        ]

    # Display pairs in a sortable table
    st.dataframe(
        pairs_df.style.format({
            'chrf_score': '{:.2f}',
            'bleu_score': '{:.2f}'
        }).bar(
            subset=['chrf_score', 'bleu_score'],
            color='#4CAF50'
        ),
        use_container_width=True
    )

    # Add download button
    st.download_button(
        "Download as CSV",
        pairs_df.to_csv(index=False).encode('utf-8'),
        "nmt_pairs.csv",
        "text/csv",
        key='download-nmt-pairs'
    )

def main():
    st.set_page_config(
        page_title="Language Model Availability Dashboard",
        page_icon="🌍",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    # Apply custom styles
    st.markdown(apply_custom_styles(), unsafe_allow_html=True)

    # Initialize session state
    if 'selected_language' not in st.session_state:
        st.session_state.selected_language = None

    try:
        # Handle backup upload
        st.title("Database Backup Upload")
        handle_backup_upload()

        st.markdown("---")

        # Add navigation
        page = st.sidebar.radio(
            "Navigate to",
            ["Map View", "NMT Pairs", "Database Upload"],
            index=0
        )

        if page == "NMT Pairs":
            render_nmt_pairs_page()
            return

        # Load data
        df = load_language_data()
        model_types = get_model_types()

        # Handle query parameters for different pages
        params = st.query_params

        if 'family_id' in params:
            render_family_page(int(params['family_id']))
            return

        if 'subfamily_id' in params:
            render_subfamily_page(int(params['subfamily_id']))
            return

        if 'selected_language' in params:
            lang_id = params['selected_language']
            st.session_state.selected_language = int(lang_id)
            del st.query_params['selected_language']

        # If a language is selected, show its info page
        if st.session_state.selected_language is not None:
            render_language_info_page(st.session_state.selected_language)
            return

        # Create top container for stats and filters
        top_container = st.container()
        with top_container:
            col1, col2 = st.columns([0.7, 0.3])
            with col1:
                render_statistics(df)
            with col2:
                st.markdown("### Model Types")
                selected_models = render_model_filters(model_types)

        # Display map
        display_map(df, st.session_state.get('selected_models', []))

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please check your database connection and try again.")

if __name__ == "__main__":
    main()