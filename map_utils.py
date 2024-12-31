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

def get_marker_color(available_models):
    """Determine marker color based on available models."""
    models = set(model for model in available_models if model)
    if len(models) == 3:  # All models available
        return '#8E44AD'  # Purple
    elif 'ASR' in models and 'NMT' in models:
        return '#FF4B4B'  # Red
    elif 'ASR' in models and 'TTS' in models:
        return '#4CAF50'  # Green
    elif 'NMT' in models and 'TTS' in models:
        return '#2196F3'  # Blue
    elif 'ASR' in models:
        return '#FF4B4B'  # Red
    elif 'NMT' in models:
        return '#4CAF50'  # Green
    elif 'TTS' in models:
        return '#2196F3'  # Blue
    return '#808080'  # Gray for no models

def add_language_markers(m, df, selected_models=None):
    """Add language markers to the map with popup information."""
    for _, row in df.iterrows():
        if selected_models:
            available_models = set(row['available_models']) - {None}
            if not any(model in available_models for model in selected_models):
                continue

        popup_content = f"""
        <div style='width: 200px'>
            <h4>{row['name']}</h4>
            <p><strong>ISO Code:</strong> {row['iso_code']}</p>
            <p><strong>Available Models:</strong></p>
            <ul>
                {''.join(f"<li>{model}</li>" for model in row['available_models'] if model)}
            </ul>
        </div>
        """

        marker_color = get_marker_color(row['available_models'])
        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=8,
            popup=folium.Popup(popup_content, max_width=300),
            color=marker_color,
            fill=True,
            fill_color=marker_color,
            fill_opacity=0.7
        ).add_to(m)

def display_map(df, selected_models=None):
    """Create and display the map with language markers."""
    m = create_base_map()
    add_language_markers(m, df, selected_models)
    folium_static(m)