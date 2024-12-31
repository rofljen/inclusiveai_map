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

        /* Model filters box container */
        .model-filters-box {
            background-color: white;
            border: 1px solid #e5e7eb;
            border-radius: 8px;
            padding: 1rem;
            margin-top: 0.5rem;
        }

        /* Style model circles */
        .model-circle {
            width: 12px !important;
            height: 12px !important;
            border-radius: 50% !important;
            margin: 4px auto !important;
            transition: opacity 0.2s ease !important;
        }

        /* Hide the actual button */
        [data-testid="baseButton-secondary"] {
            position: absolute !important;
            opacity: 0 !important;
            cursor: pointer !important;
            width: 12px !important;
            height: 12px !important;
            margin: 4px auto !important;
            padding: 0 !important;
            min-width: unset !important;
            background: transparent !important;
            border: none !important;
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
        span {
            font-size: 0.875rem !important;
            font-weight: 500 !important;
            color: #4b5563 !important;
        }

        /* Style the Model Types header */
        h3 {
            font-size: 1rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.5rem !important;
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