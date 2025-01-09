import folium
import streamlit as st
from streamlit_folium import folium_static
from folium import plugins
import pandas as pd
import numpy as np

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

    # Convert available_models to list and filter out None values
    models_present = [m for m in (available_models or []) if m is not None]

    if not selected_models:
        if len(models_present) == 0:
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
        models_to_show = models_present
    else:
        models_to_show = [m for m in models_present if m in selected_models]
        if len(models_to_show) == 0:
            return None

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

def create_pair_popup_content(source_lang, target_lang, pair_data):
    """Create HTML content for NMT pair popup."""
    return f"""
    <div style='min-width: 200px; padding: 10px;'>
        <h4 style='margin-bottom: 10px; color: #2c3e50;'>Translation Pair Details</h4>
        <div style='margin-bottom: 15px;'>
            <strong>Source:</strong> {source_lang}<br>
            <strong>Target:</strong> {target_lang}
        </div>
        <div style='background: #f8f9fa; padding: 10px; border-radius: 4px;'>
            <div style='margin-bottom: 8px;'>
                <strong>Quality Metrics:</strong>
            </div>
            <div style='display: flex; justify-content: space-between;'>
                <span>chrF++ Score:</span>
                <span>{pair_data.get('chrf_score', 'N/A'):.2f}</span>
            </div>
            <div style='display: flex; justify-content: space-between;'>
                <span>BLEU Score:</span>
                <span>{pair_data.get('bleu_score', 'N/A'):.2f}</span>
            </div>
        </div>
    </div>
    """

def add_language_connections(m, df, selected_language_id=None):
    """Add lines connecting languages that have NMT pairs."""
    if selected_language_id is None:
        return

    # Get the selected language's data
    selected_lang = df[df['id'] == selected_language_id].iloc[0]

    if not isinstance(selected_lang.get('connected_coords'), (list, np.ndarray)):
        return

    # Create a feature group for connections
    connections_group = folium.FeatureGroup(name="NMT Connections")

    # Get source coordinates
    source_coords = [selected_lang['latitude'], selected_lang['longitude']]

    # Add lines for each connection
    for idx, target_coords in enumerate(selected_lang['connected_coords']):
        if isinstance(target_coords, (list, np.ndarray)) and len(target_coords) == 2:
            # Get the connected language name and scores
            connected_lang_name = selected_lang['connected_languages'][idx] if isinstance(selected_lang.get('connected_languages'), (list, np.ndarray)) and idx < len(selected_lang['connected_languages']) else 'Unknown'

            # Get scores for this pair
            pair_data = {
                'chrf_score': selected_lang['chrf_scores'][idx] if isinstance(selected_lang.get('chrf_scores'), (list, np.ndarray)) and idx < len(selected_lang['chrf_scores']) else 0.0,
                'bleu_score': selected_lang['bleu_scores'][idx] if isinstance(selected_lang.get('bleu_scores'), (list, np.ndarray)) and idx < len(selected_lang['bleu_scores']) else 0.0
            }

            # Create popup content
            popup_content = create_pair_popup_content(
                selected_lang['name'],
                connected_lang_name,
                pair_data
            )

            # Create a line with animation and enhanced popup
            line = plugins.AntPath(
                locations=[source_coords, target_coords],
                weight=2,
                color='#4CAF50',
                opacity=0.6
            )
            # Add popup to the line
            popup = folium.Popup(popup_content, max_width=300)
            line.add_child(popup)
            line.add_to(connections_group)

            # Add markers for connected languages with enhanced popup
            marker = folium.CircleMarker(
                location=target_coords,
                radius=8,
                color="#4CAF50",
                fill=True,
                popup=folium.Popup(popup_content, max_width=300)
            )
            marker.add_to(connections_group)

    connections_group.add_to(m)

def create_popup_content(row):
    """Create HTML content for map marker popup."""
    colors = get_model_colors()
    model_badges = []

    # Convert available_models to list and filter out None values
    available_models = [m for m in (row.get('available_models') or []) if m is not None]

    for model in available_models:
        model_badges.append(
            f'<span style="background-color: {colors[model]}; '
            f'color: white; padding: 2px 8px; border-radius: 10px; '
            f'margin-right: 5px;">{model}</span>'
        )

    nmt_info = ''
    if 'NMT' in available_models:
        nmt_info = f"""
        <p><strong>NMT Pairs:</strong> {row.get('nmt_pair_count', 0)} language pairs</p>
        """

    connected_langs = ''
    if isinstance(row.get('connected_languages'), str) and row['connected_languages'].strip():
        connected_langs = """
        <p><strong>Connected Languages:</strong></p>
        <div style='margin-top: 5px; max-height: 100px; overflow-y: auto;'>
            {}
        </div>
        """.format(
            '<br>'.join(f"• {lang}" for lang in row['connected_languages'].split(', '))
        )

    view_details_button = f"""
        <div style='margin-top: 10px'>
            <a href="?selected_language={row['id']}" 
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
    """

    return f"""
    <div style='width: 250px'>
        <h4 style="margin-bottom: 8px;">
            {row['name']}
        </h4>
        <p><strong>ISO Code:</strong> {row.get('iso_code') or 'N/A'}</p>
        <p><strong>Available Models:</strong></p>
        <div style='margin-top: 5px'>
            {''.join(model_badges) if model_badges else '<span style="color: #666;">None available</span>'}
        </div>
        {nmt_info}
        {connected_langs}
        {view_details_button}
    </div>
    """

def display_map(df, selected_models=None, selected_language_id=None):
    """Create and display the map with language markers and connections."""
    m = create_base_map()

    # Add the language connections first so they appear under the markers
    add_language_connections(m, df, selected_language_id)

    # Add the language markers
    add_language_markers(m, df, selected_models)

    # Add layer controls
    folium.LayerControl().add_to(m)

    folium_static(m)

def add_language_markers(m, df, selected_models):
    """Add language markers to the map with popup information."""
    for _, row in df.iterrows():
        icon_html = create_model_indicator_html(row.get('available_models'), selected_models)

        if selected_models and icon_html is None:
            continue

        custom_icon = folium.DivIcon(
            html=icon_html,
            icon_size=(24, 24),
            icon_anchor=(12, 12)
        )

        marker = folium.Marker(
            location=[row['latitude'], row['longitude']],
            popup=folium.Popup(create_popup_content(row), max_width=300),
            icon=custom_icon
        )
        marker.add_to(m)