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
        </style>
    """
