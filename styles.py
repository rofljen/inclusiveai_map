def apply_custom_styles():
    """Apply custom CSS styles to the application."""
    return """
        <style>
        /* Hide sidebar by default */
        [data-testid="stSidebar"] {
            display: none;
        }

        /* Make the main content full width */
        .main .block-container {
            padding: 0;
            max-width: 100%;
        }

        /* Floating card styles */
        .floating-card {
            position: fixed;
            bottom: 2rem;
            right: 2rem;
            background: white;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 1000;
            min-width: 200px;
        }

        /* Legend styles */
        .legend-item {
            display: flex;
            align-items: center;
            margin: 0.5rem 0;
            padding: 0.25rem;
            border-radius: 5px;
            transition: all 0.3s ease;
        }

        .legend-item:hover {
            background: rgba(0,0,0,0.05);
        }

        .legend-indicator {
            display: flex;
            align-items: center;
            justify-content: center;
            width: 24px;
            height: 24px;
        }

        .model-dot {
            width: 16px;
            height: 16px;
            border-radius: 50%;
            background-color: var(--model-color);
            opacity: 0.8;
        }

        /* Model colors */
        .model-asr { --model-color: #FF4B4B; }
        .model-nmt { --model-color: #4CAF50; }
        .model-tts { --model-color: #2196F3; }

        /* Make the map container full height */
        [data-testid="stArrowVegaLiteChart"] {
            width: 100vw;
            height: 100vh;
        }

        /* Style the folium map */
        .folium-map {
            width: 100%;
            height: 100vh;
            position: absolute;
            top: 0;
            left: 0;
        }

        /* Style Streamlit buttons in the legend */
        .floating-card [data-testid="baseButton-secondary"] {
            background: transparent;
            border: none;
            color: #262730;
            text-align: left;
            width: 100%;
            padding: 0.25rem 0.5rem;
        }

        .floating-card [data-testid="baseButton-primary"] {
            background: rgba(0,0,0,0.05);
            border: none;
            color: #262730;
            text-align: left;
            width: 100%;
            padding: 0.25rem 0.5rem;
        }

        /* Hide default button styles */
        .floating-card button {
            box-shadow: none !important;
        }

        .floating-card button:hover {
            border: none;
            color: #262730;
            background: rgba(0,0,0,0.05);
        }
        </style>
    """