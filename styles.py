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
        .legend-circle {
            width: 24px;
            height: 24px;
            border-radius: 50%;
            margin: 8px 0;
            cursor: pointer;
            transition: all 0.3s ease;
            opacity: 0.8;
        }

        .legend-label {
            font-size: 14px;
            color: #262730;
            margin-left: 8px;
            line-height: 36px;
        }

        /* Model colors */
        .model-asr { background-color: #FF4B4B; }
        .model-nmt { background-color: #4CAF50; }
        .model-tts { background-color: #2196F3; }

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

        /* Remove default Streamlit padding and margins */
        [data-testid="stVerticalBlock"] {
            gap: 0 !important;
            padding: 0 !important;
        }

        /* Hide default button styles */
        .floating-card [data-testid="stHorizontalBlock"] {
            gap: 0.5rem !important;
        }

        /* Style the buttons in the legend */
        .floating-card [data-testid="baseButton-secondary"] {
            width: 24px !important;
            height: 24px !important;
            padding: 0 !important;
            border-radius: 50% !important;
            margin: 8px 0 !important;
            background-color: var(--model-color) !important;
            border: none !important;
        }

        /* Clean metric display */
        [data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
        }

        /* Hide button text */
        .floating-card [data-testid="baseButton-secondary"] div {
            display: none !important;
        }
        </style>
    """