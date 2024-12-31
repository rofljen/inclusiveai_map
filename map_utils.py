import folium
import streamlit as st
from streamlit_folium import folium_static

def create_base_map():
    """Create the base map centered on the world view."""
    return folium.Map(
        location=[20, 0],
        zoom_start=2,
        tiles='CartoDB positron'
    )

def get_model_colors():
    """Get consistent color scheme for models."""
    return {
        'ASR': '#FF4B4B',
        'NMT': '#4CAF50',
        'TTS': '#2196F3'
    }

def create_model_indicator_html(available_models, selected_models):
    """Create HTML for pie-chart style indicators showing available models."""
    if not available_models:
        return None

    # If there are selected models, only show markers for languages that have those models
    if selected_models:
        matching_models = [m for m in available_models if m and m in selected_models]
        if not matching_models:
            return None
    else:
        # If no models are selected, don't show any markers
        return None

    colors = get_model_colors()

    if len(matching_models) == 1:
        return f"""
        <div style='
            width: 24px;
            height: 24px;
            background-color: {colors[matching_models[0]]};
            border-radius: 50%;
            opacity: 0.8;
        '></div>
        """

    # For multiple models, create a pie chart style indicator
    conic_gradient = []
    segment_size = 360 / len(matching_models)
    current_angle = 0

    for model in matching_models:
        next_angle = current_angle + segment_size
        conic_gradient.append(f"{colors[model]} {current_angle}deg {next_angle}deg")
        current_angle = next_angle

    return f"""
    <div style='
        width: 24px;
        height: 24px;
        background: conic-gradient({", ".join(conic_gradient)});
        border-radius: 50%;
        opacity: 0.8;
        border: 2px solid white;
    '></div>
    """

def create_popup_content(row):
    """Create HTML content for map marker popup."""
    colors = get_model_colors()
    model_badges = []

    for model in [m for m in row['available_models'] if m]:
        model_badges.append(
            f'<span style="background-color: {colors[model]}; '
            f'color: white; padding: 2px 8px; border-radius: 10px; '
            f'margin-right: 5px;">{model}</span>'
        )

    return f"""
    <div style='width: 200px'>
        <h4 style="margin-bottom: 8px;">
            {row['name']}
        </h4>
        <p><strong>ISO Code:</strong> {row['iso_code'] or 'N/A'}</p>
        <p><strong>Available Models:</strong></p>
        <div style='margin-top: 5px'>
            {''.join(model_badges)}
        </div>
        <div style='margin-top: 10px'>
            <button onclick="
                window.parent.postMessage({{'selected_language': {row['id']}}}, '*');
            " style="color: #1f77b4; border: none; background: none; padding: 0; cursor: pointer;">
                View Details
            </button>
        </div>
    </div>
    """

def add_language_markers(m, df, selected_models):
    """Add language markers to the map with popup information."""
    for _, row in df.iterrows():
        # Create custom icon with filtered models
        icon_html = create_model_indicator_html(row['available_models'], selected_models)

        # Skip adding marker if no models are selected for this language
        if icon_html is None:
            continue

        custom_icon = folium.DivIcon(
            html=icon_html,
            icon_size=(24, 24),
            icon_anchor=(12, 12)
        )

        # Add marker to map
        marker = folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(create_popup_content(row), max_width=300),
            icon=custom_icon
        )
        marker.add_to(m)

def display_map(df, selected_models=None):
    """Create and display the map with language markers."""
    m = create_base_map()
    add_language_markers(m, df, selected_models)
    folium_static(m)