def apply_custom_styles():
    """Apply custom CSS styles to the application."""
    return """
        <style>
        .stMetric {
            background-color: #f0f2f6;
            padding: 10px;
            border-radius: 5px;
        }
        .stMetric:hover {
            background-color: #e0e2e6;
        }
        .streamlit-expanderHeader {
            background-color: #f0f2f6;
            border-radius: 5px;
        }

        /* Model type button styles */
        .model-button {
            display: inline-block;
            padding: 5px 10px;
            margin: 5px;
            border-radius: 15px;
            cursor: pointer;
            font-size: 14px;
            border: none;
            color: white;
        }

        .model-button-asr {
            background-color: #FF6B6B;
        }

        .model-button-nmt {
            background-color: #4ECDC4;
        }

        .model-button-tts {
            background-color: #45B7D1;
        }

        .model-button.selected {
            box-shadow: 0 0 0 2px white, 0 0 0 4px currentColor;
        }
        </style>
    """