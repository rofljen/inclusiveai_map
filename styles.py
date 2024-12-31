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

        .floating-card h3 {
            margin-bottom: 1rem;
            color: #262730;
        }

        /* Model filters container */
        .model-filters {
            display: flex;
            flex-direction: column;
            gap: 0.5rem;
        }

        /* Remove default Streamlit padding and margins */
        .floating-card [data-testid="stVerticalBlock"] {
            gap: 0 !important;
            padding: 0 !important;
        }

        /* Style the buttons */
        .floating-card button {
            width: 24px !important;
            height: 24px !important;
            padding: 0 !important;
            border-radius: 50% !important;
            margin: 0 !important;
            border: 2px solid transparent !important;
            transition: all 0.3s ease !important;
        }

        /* Hide button text */
        .floating-card button div {
            display: none !important;
        }

        /* Model type specific colors */
        .floating-card button[key*="toggle_ASR"] {
            background-color: #FF4B4B !important;
        }

        .floating-card button[key*="toggle_NMT"] {
            background-color: #4CAF50 !important;
        }

        .floating-card button[key*="toggle_TTS"] {
            background-color: #2196F3 !important;
        }

        /* Selected state */
        .floating-card button[data-selected="true"] {
            border-color: #262730 !important;
        }

        /* Button hover effects */
        .floating-card button:hover {
            opacity: 0.8;
            transform: scale(1.1);
        }

        /* Clean metric display */
        [data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
        }

        /* Adjust column layout */
        .floating-card [data-testid="stHorizontalBlock"] {
            gap: 1rem !important;
            align-items: center !important;
        }

        /* Style text next to buttons */
        .floating-card span {
            color: #262730;
            font-size: 14px;
            margin-left: 8px;
        }
        </style>
    """