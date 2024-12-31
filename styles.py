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

        /* Model filter row */
        .model-filter-row {
            display: flex;
            align-items: center;
            gap: 0.75rem;
            padding: 0.5rem;
            cursor: pointer;
            position: relative;
        }

        /* Style model circles */
        .model-circle {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            transition: opacity 0.2s ease;
        }

        /* Model name text */
        .model-name {
            font-size: 0.875rem;
            font-weight: 500;
            color: #4b5563;
        }

        /* Completely hide Streamlit button artifacts */
        button[data-testid^="baseButton-"] {
            position: absolute !important;
            inset: 0 !important;
            opacity: 0 !important;
            cursor: pointer !important;
            margin: 0 !important;
            padding: 0 !important;
            width: 100% !important;
            height: 100% !important;
            min-width: 0 !important;
            border: none !important;
            background: none !important;
            box-shadow: none !important;
        }

        /* Hide all button children elements */
        button[data-testid^="baseButton-"] * {
            display: none !important;
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