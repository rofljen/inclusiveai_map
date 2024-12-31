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
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'map'

    try:
        # Load data
        df = load_language_data()
        model_types = get_model_types()

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
                if selected_models != st.session_state.get('selected_models', []):
                    st.session_state['selected_models'] = selected_models
                    st.rerun()

        # Display map
        display_map(df, st.session_state.get('selected_models', []))

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please check your database connection and try again.")

if __name__ == "__main__":
    main()