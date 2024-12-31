import streamlit as st
import pandas as pd

def render_sidebar_filters(model_types):
    """Render sidebar filters for model types and search."""
    st.sidebar.title("Filters")

    # Model type selection using buttons
    st.sidebar.markdown("### Model Types")

    # Initialize session state for selected models if not exists
    if 'selected_models' not in st.session_state:
        st.session_state.selected_models = set()

    # Create a row of buttons for each model type
    cols = st.sidebar.columns(len(model_types))
    selected_models = set()

    for i, model_type in enumerate(model_types):
        with cols[i]:
            # Create custom button with HTML
            is_selected = model_type in st.session_state.selected_models
            button_class = f"model-button model-button-{model_type.lower()}"
            if is_selected:
                button_class += " selected"

            button_html = f"""
            <button class="{button_class}">
                {model_type}
            </button>
            """
            if st.markdown(button_html, unsafe_allow_html=True):
                if model_type in st.session_state.selected_models:
                    st.session_state.selected_models.remove(model_type)
                else:
                    st.session_state.selected_models.add(model_type)

    # Search box
    search_query = st.sidebar.text_input(
        "Search Languages",
        ""
    ).lower()

    return list(st.session_state.selected_models), search_query

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