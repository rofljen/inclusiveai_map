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
        div[data-testid="stHorizontalBlock"] button[kind="primary"] {
            background-color: var(--model-color);
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            transition: all 0.3s ease;
        }

        div[data-testid="stHorizontalBlock"] button[kind="secondary"] {
            background-color: transparent;
            border: 2px solid var(--model-color);
            padding: 0.5rem 1rem;
            border-radius: 20px;
            color: var(--model-color);
            font-weight: bold;
            transition: all 0.3s ease;
        }

        /* ASR button */
        div[data-testid="stHorizontalBlock"] button[key="model_button_ASR"] {
            --model-color: #FF4B4B;
        }

        /* NMT button */
        div[data-testid="stHorizontalBlock"] button[key="model_button_NMT"] {
            --model-color: #4CAF50;
        }

        /* TTS button */
        div[data-testid="stHorizontalBlock"] button[key="model_button_TTS"] {
            --model-color: #2196F3;
        }

        /* Hover effects */
        div[data-testid="stHorizontalBlock"] button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        </style>
    """