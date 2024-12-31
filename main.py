import streamlit as st
from database import load_language_data, get_model_types
from map_utils import display_map
from components import render_model_filters, render_statistics
from styles import apply_custom_styles
from language_info import render_language_info_page, render_family_page, render_subfamily_page
from db_utils import handle_backup_upload

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

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please check your database connection and try again.")

if __name__ == "__main__":
    main()