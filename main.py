import streamlit as st
from database import load_language_data, get_model_types
from map_utils import display_map
from components import render_model_filters, render_statistics
from styles import apply_custom_styles
from language_info import render_language_info_page

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
        # Load data
        df = load_language_data()
        model_types = get_model_types()

        # Handle language selection from query params
        params = st.query_params
        if 'selected_language' in params:
            lang_id = params['selected_language']
            st.session_state.selected_language = int(lang_id)
            # Clear the query param after processing
            del st.query_params['selected_language']

        # If a language is selected, show its info page
        if st.session_state.selected_language is not None:
            render_language_info_page(st.session_state.selected_language)
            return

        # Create top container for stats and filters
        top_container = st.container()
        with top_container:
            # Display statistics
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