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

def create_model_indicator_html(available_models, selected_models=None):
    """Create HTML for pie-chart style indicators showing available models."""
    colors = get_model_colors()

    # If no models are selected or available, return a gray circle
    if not available_models or (selected_models and not any(m in selected_models for m in available_models if m)):
        return """
        <div style='
            width: 24px;
            height: 24px;
            background-color: #e5e7eb;
            border-radius: 50%;
            opacity: 0.5;
        '></div>
        """

    # Filter models based on selection
    models = [m for m in available_models if m and (not selected_models or m in selected_models)]

    if not models:
        return None  # Return None to skip creating the marker

    if len(models) == 1:
        return f"""
        <div style='
            width: 24px;
            height: 24px;
            background-color: {colors[models[0]]};
            border-radius: 50%;
            opacity: 0.8;
        '></div>
        """

    # For multiple models, create a pie chart style indicator
    conic_gradient = []
    segment_size = 360 / len(models)
    current_angle = 0

    for model in models:
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
            <button onclick="
                window.parent.postMessage({{
                    type: 'streamlit:componentReady',
                    data: {{
                        apiVersion: 1,
                        componentName: 'streamlit_app',
                        componentInstance: 'language_detail',
                        data: {row['id']}
                    }}
                }}, '*');
                return false;
            " style="color: #1f77b4; text-decoration: none; border: none; background: none; padding: 0; cursor: pointer; font-size: inherit;">
                {row['name']}
            </button>
        </h4>
        <p><strong>ISO Code:</strong> {row['iso_code'] or 'N/A'}</p>
        <p><strong>Available Models:</strong></p>
        <div style='margin-top: 5px'>
            {''.join(model_badges)}
        </div>
    </div>
    """

def add_language_markers(m, df, selected_models=None):
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