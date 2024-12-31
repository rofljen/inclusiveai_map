import streamlit as st
import pandas as pd

def render_sidebar_filters(model_types):
    """Render sidebar filters for model types and search."""
    st.sidebar.title("Filters")
    
    # Model type selection
    selected_models = st.sidebar.multiselect(
        "Select Model Types",
        options=model_types,
        default=[]
    )
    
    # Search box
    search_query = st.sidebar.text_input(
        "Search Languages",
        ""
    ).lower()
    
    return selected_models, search_query

def render_statistics(df):
    """Render statistics about languages and models."""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Total Languages",
            len(df)
        )
    
    with col2:
        total_models = sum(
            len([x for x in models if x]) 
            for models in df['available_models']
        )
        st.metric(
            "Total Model Implementations",
            total_models
        )
    
    with col3:
        languages_with_models = len(
            df[df['available_models'].apply(lambda x: any(m for m in x if m))]
        )
        st.metric(
            "Languages with Models",
            languages_with_models
        )

def render_language_table(df, search_query, selected_models):
    """Render a table showing language and model information."""
    filtered_df = df.copy()
    
    if search_query:
        filtered_df = filtered_df[
            filtered_df['name'].str.lower().str.contains(search_query) |
            filtered_df['iso_code'].str.lower().str.contains(search_query)
        ]
    
    if selected_models:
        filtered_df = filtered_df[
            filtered_df['available_models'].apply(
                lambda x: any(model in x for model in selected_models)
            )
        ]
    
    if not filtered_df.empty:
        st.dataframe(
            filtered_df[['name', 'iso_code', 'available_models']],
            hide_index=True,
            column_config={
                'name': 'Language',
                'iso_code': 'ISO Code',
                'available_models': 'Available Models'
            }
        )
    else:
        st.info("No languages match the selected filters.")
