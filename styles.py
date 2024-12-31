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
            padding: 2rem;
            max-width: 100%;
        }

        /* Style the model filter buttons */
        [data-testid="baseButton-secondary"] {
            border-radius: 50% !important;
            width: 20px !important;
            height: 20px !important;
            padding: 0 !important;
            min-width: unset !important;
            border: 2px solid transparent !important;
            transition: all 0.2s ease !important;
        }

        /* Model type specific colors */
        [data-testid="baseButton-secondary"][key*="model_ASR"] {
            background-color: #FF4B4B !important;
        }

        [data-testid="baseButton-secondary"][key*="model_NMT"] {
            background-color: #4CAF50 !important;
        }

        [data-testid="baseButton-secondary"][key*="model_TTS"] {
            background-color: #2196F3 !important;
        }

        /* Selected state for buttons */
        [data-testid="baseButton-secondary"][aria-pressed="true"] {
            border-color: #262730 !important;
            transform: scale(1.1);
        }

        /* Hide button text */
        [data-testid="baseButton-secondary"] div {
            display: none !important;
        }

        /* Style metrics */
        [data-testid="stMetricValue"] {
            font-size: 1.5rem !important;
            font-weight: 600 !important;
        }

        [data-testid="stMetricLabel"] {
            font-size: 0.875rem !important;
            color: #6b7280 !important;
        }

        /* Make model type text smaller and refined */
        span[style*="color:"] {
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            color: #4b5563 !important;
        }

        /* Style the Model Types header */
        h3 {
            font-size: 1rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.75rem !important;
            color: #374151 !important;
        }

        /* Responsive layout adjustments */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 1rem;
            }
        }
        </style>
    """