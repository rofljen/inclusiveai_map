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
    # Filter models based on selection
    if selected_models:
        models = [m for m in available_models if m and m in selected_models]
    else:
        models = [m for m in available_models if m]

    colors = get_model_colors()

    if not models:
        return """
        <div style='
            width: 24px;
            height: 24px;
            background-color: #808080;
            border-radius: 50%;
            opacity: 0.7;
        '></div>
        """

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

def add_language_markers(m, df, selected_models=None):
    """Add language markers to the map with popup information."""
    for _, row in df.iterrows():
        # Skip if doesn't match selected model filter
        if selected_models:
            available_models = set(m for m in row['available_models'] if m)
            if not any(model in available_models for model in selected_models):
                continue

        # Filter available models based on selection for display
        display_models = [m for m in row['available_models'] 
                        if m and (not selected_models or m in selected_models)]

        # Create popup content
        model_badges = []
        colors = get_model_colors()

        for model in display_models:
            model_badges.append(
                f'<span style="background-color: {colors[model]}; '
                f'color: white; padding: 2px 8px; border-radius: 10px; '
                f'margin-right: 5px;">{model}</span>'
            )

        popup_content = f"""
        <div style='width: 200px'>
            <h4>{row['name']}</h4>
            <p><strong>ISO Code:</strong> {row['iso_code'] or 'N/A'}</p>
            <p><strong>Available Models:</strong></p>
            <div style='margin-top: 5px'>
                {''.join(model_badges)}
            </div>
        </div>
        """

        # Create custom icon with filtered models
        icon_html = create_model_indicator_html(row['available_models'], selected_models)
        custom_icon = folium.DivIcon(
            html=icon_html,
            icon_size=(24, 24),
            icon_anchor=(12, 12)
        )

        # Add marker to map
        marker = folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(popup_content, max_width=300),
            icon=custom_icon
        )
        marker.add_to(m)

def display_map(df, selected_models=None):
    """Create and display the map with language markers."""
    m = create_base_map()
    add_language_markers(m, df, selected_models)
    folium_static(m)