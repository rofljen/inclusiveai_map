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
        .floating-card button {
            width: 24px !important;
            height: 24px !important;
            padding: 0 !important;
            border-radius: 50% !important;
            margin: 8px 0 !important;
            border: none !important;
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

        /* Button hover effects */
        .floating-card button:hover {
            opacity: 0.8;
            transform: scale(1.1);
        }

        /* Clean metric display */
        [data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
        }
        </style>
    """