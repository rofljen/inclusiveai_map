import streamlit as st
from database import load_language_data, get_model_types
from map_utils import display_map
from components import (
    render_sidebar_filters,
    render_statistics,
    render_language_table
)
from styles import apply_custom_styles

def main():
    st.set_page_config(
        page_title="Language Model Availability Dashboard",
        page_icon="🌍",
        layout="wide"
    )
    
    # Apply custom styles
    st.markdown(apply_custom_styles(), unsafe_allow_html=True)
    
    # Page title
    st.title("🌍 Language Model Availability Dashboard")
    
    try:
        # Load data
        df = load_language_data()
        model_types = get_model_types()
        
        # Render sidebar filters
        selected_models, search_query = render_sidebar_filters(model_types)
        
        # Display statistics
        render_statistics(df)
        
        # Create tabs for different views
        tab1, tab2 = st.tabs(["Map View", "Table View"])
        
        with tab1:
            st.subheader("Geographic Distribution")
            display_map(df, selected_models)
        
        with tab2:
            st.subheader("Language Model Availability")
            render_language_table(df, search_query, selected_models)
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.error("Please check your database connection and try again.")

if __name__ == "__main__":
    main()
