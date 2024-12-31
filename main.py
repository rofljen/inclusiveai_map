import streamlit as st
from database import load_language_data, get_model_types
from map_utils import display_map
from components import (
    render_sidebar_filters,
    render_statistics,
    render_language_table,
    render_search_page
)
from styles import apply_custom_styles
from language_info import render_language_info_page

def main():
    st.set_page_config(
        page_title="Language Model Availability Dashboard",
        page_icon="🌍",
        layout="wide"
    )

    # Apply custom styles
    st.markdown(apply_custom_styles(), unsafe_allow_html=True)

    # Initialize session state for selected language
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

        # Navigation
        st.sidebar.title("Navigation")
        page = st.sidebar.radio("", ["Map View", "Search & Filter"], 
                              format_func=lambda x: x)

        # Page title
        st.title("🌍 Language Model Availability Dashboard")

        # Render model type filters in sidebar
        selected_models, search_query = render_sidebar_filters(model_types)

        if page == "Map View":
            # Display statistics
            render_statistics(df)

            # Display map
            st.subheader("Geographic Distribution")
            display_map(df, selected_models)

        else:  # Search & Filter page
            render_search_page(df, search_query, selected_models)

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please check your database connection and try again.")

if __name__ == "__main__":
    main()