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
    colors = get_model_colors()

    # Filter out None values from available_models
    models_present = [m for m in available_models if m]

    # If no models are selected, show all languages
    if not selected_models:
        if not models_present:
            # Gray marker for languages without any models
            return """
            <div style='
                width: 24px;
                height: 24px;
                background-color: #808080;
                border-radius: 50%;
                opacity: 0.4;
                border: 2px solid white;
            '></div>
            """
        # For languages with models, show their model indicators
        models_to_show = models_present
    else:
        # If models are selected, only show languages with those models
        models_to_show = [m for m in models_present if m in selected_models]
        if not models_to_show:
            return None  # Don't show languages that don't match the filter

    # Single model indicator
    if len(models_to_show) == 1:
        return f"""
        <div style='
            width: 24px;
            height: 24px;
            background-color: {colors[models_to_show[0]]};
            border-radius: 50%;
            opacity: 0.8;
            border: 2px solid white;
        '></div>
        """

    # Multiple models pie chart indicator
    conic_gradient = []
    segment_size = 360 / len(models_to_show)
    current_angle = 0

    for model in models_to_show:
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
            {''.join(model_badges) if model_badges else '<span style="color: #666;">None available</span>'}
        </div>
        <div style='margin-top: 10px'>
            <a href="?selected_language={row['id']}" 
               target="_blank"
               style="
                   display: inline-block;
                   color: white;
                   background-color: #1f77b4;
                   border: none;
                   padding: 4px 12px;
                   border-radius: 4px;
                   cursor: pointer;
                   font-size: 14px;
                   text-decoration: none;
               ">
                View Details
            </a>
        </div>
    </div>
    """

def add_language_markers(m, df, selected_models):
    """Add language markers to the map with popup information."""
    for _, row in df.iterrows():
        # Create custom icon with filtered models
        icon_html = create_model_indicator_html(row['available_models'], selected_models)

        # Skip adding marker only if models are selected and this language doesn't match
        if selected_models and icon_html is None:
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