import streamlit as st
import pandas as pd

def render_model_filters(model_types):
    """Render model type filters in a floating card with legend-style display."""
    # Initialize session state for selected models if not exists
    if 'selected_models' not in st.session_state:
        st.session_state.selected_models = set()

    model_colors = {
        'ASR': '#FF4B4B',
        'NMT': '#4CAF50',
        'TTS': '#2196F3'
    }

    # Create legend items as clickable filters
    for model_type in model_types:
        is_selected = model_type in st.session_state.selected_models
        model_class = f'model-{model_type.lower()}'

        col1, col2 = st.columns([0.2, 0.8])

        with col1:
            # Hidden button to handle the click event
            if st.button(f"Toggle {model_type}", key=f"toggle_{model_type}", label_visibility="hidden"):
                if is_selected:
                    st.session_state.selected_models.remove(model_type)
                else:
                    st.session_state.selected_models.add(model_type)
                st.rerun()

        with col2:
            st.markdown(f'<span class="legend-label">{model_type}</span>', unsafe_allow_html=True)

    return list(st.session_state.selected_models)

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

def render_search_page(df, search_query, selected_models):
    """Render the search and filter page."""
    st.subheader("Search & Filter Languages")

    # Search box
    search_query = st.text_input("Search by Language Name or ISO Code", "").lower()

    # Advanced filters
    with st.expander("Advanced Filters"):
        col1, col2 = st.columns(2)
        with col1:
            min_models = st.slider("Minimum Number of Models", 0, 3, 0)
        with col2:
            show_only_with_coords = st.checkbox("Show Only Languages with Coordinates", True)

    # Filter the dataframe
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

    if min_models > 0:
        filtered_df = filtered_df[
            filtered_df['available_models'].apply(
                lambda x: len([m for m in x if m]) >= min_models
            )
        ]

    if show_only_with_coords:
        filtered_df = filtered_df[
            filtered_df['latitude'].notna() & filtered_df['longitude'].notna()
        ]

    # Display results
    st.subheader(f"Results ({len(filtered_df)} languages)")

    for idx, row in filtered_df.iterrows():
        with st.container():
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button(row['name'], key=f"lang_{idx}"):
                    st.session_state.selected_language = row['id']
                    st.rerun()
            with col2:
                models = [m for m in row['available_models'] if m]
                if models:
                    model_badges = []
                    for model in models:
                        color = {'ASR': '#FF4B4B', 'NMT': '#4CAF50', 'TTS': '#2196F3'}[model]
                        model_badges.append(
                            f'<span style="background-color: {color}; color: white; '
                            f'padding: 2px 8px; border-radius: 10px; margin-right: 5px;">{model}</span>'
                        )
                    st.markdown(''.join(model_badges), unsafe_allow_html=True)
                else:
                    st.text("No models available")
            st.markdown("---")

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
        for idx, row in filtered_df.iterrows():
            col1, col2 = st.columns([3, 1])
            with col1:
                if st.button(row['name'], key=f"lang_{idx}"):
                    st.session_state.selected_language = row['id']
                    st.rerun()
            with col2:
                models = [m for m in row['available_models'] if m]
                if models:
                    model_badges = []
                    for model in models:
                        color = {'ASR': '#FF4B4B', 'NMT': '#4CAF50', 'TTS': '#2196F3'}[model]
                        model_badges.append(
                            f'<span style="background-color: {color}; color: white; '
                            f'padding: 2px 8px; border-radius: 10px; margin-right: 5px;">{model}</span>'
                        )
                    st.markdown(''.join(model_badges), unsafe_allow_html=True)
                else:
                    st.text("No models available")
    else:
        st.info("No languages match the selected filters.")