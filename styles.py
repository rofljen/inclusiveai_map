def apply_custom_styles():
    """Apply custom CSS styles to the application."""
    return """
        <style>
        /* Base styles */
        .main .block-container {
            padding: 2rem;
            max-width: 100%;
        }

        /* Interactive Cards */
        .stMarkdown div[data-testid="stMarkdownContainer"] {
            background: white;
            border-radius: 8px;
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            transition: transform 0.2s, box-shadow 0.2s;
        }

        .stMarkdown div[data-testid="stMarkdownContainer"]:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: transparent;
        }

        .stTabs [data-baseweb="tab"] {
            padding: 8px 16px;
            border-radius: 4px;
            border: none;
            font-weight: 500;
            background-color: #f8f9fa;
            transition: background-color 0.2s;
        }

        .stTabs [data-baseweb="tab"]:hover {
            background-color: #e9ecef;
        }

        .stTabs [data-baseweb="tab"][aria-selected="true"] {
            background-color: #1f77b4;
            color: white;
        }

        /* Metric cards */
        [data-testid="metric-container"] {
            background-color: white;
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }

        [data-testid="metric-container"]:hover {
            transform: translateY(-2px);
        }

        /* Headers */
        h1, h2, h3, h4, h5, h6 {
            color: #2c3e50;
            margin-bottom: 1rem;
        }

        /* Status indicators */
        .status-indicator {
            display: inline-flex;
            align-items: center;
            padding: 4px 12px;
            border-radius: 16px;
            font-size: 0.875rem;
            font-weight: 500;
            margin-bottom: 8px;
        }

        .status-available {
            background-color: #d4edda;
            color: #155724;
        }

        .status-unavailable {
            background-color: #f8d7da;
            color: #721c24;
        }

        /* Interactive buttons */
        .stButton button {
            border-radius: 4px;
            padding: 0.5rem 1rem;
            font-weight: 500;
            transition: all 0.2s;
        }

        .stButton button:hover {
            transform: translateY(-1px);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }

        /* Data table styling */
        .dataframe {
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
        }

        .dataframe th {
            background-color: #f8f9fa;
            padding: 12px 16px;
            font-weight: 600;
        }

        .dataframe td {
            padding: 12px 16px;
            border-top: 1px solid #e9ecef;
        }

        /* Chart container */
        .chart-container {
            background: white;
            border-radius: 8px;
            padding: 1rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            margin: 1rem 0;
        }

        /* Model filters container */
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
            user-select: none;
        }

        /* Hide default checkbox */
        .model-filter-row input[type="checkbox"] {
            position: absolute;
            opacity: 0;
            cursor: pointer;
            height: 0;
            width: 0;
        }

        /* Style model circles */
        .model-circle {
            width: 12px;
            height: 12px;
            border-radius: 50%;
            opacity: 0.3;
            transition: opacity 0.2s ease;
        }

        /* Style circle when checkbox is checked */
        .model-filter-row input:checked ~ .model-circle {
            opacity: 1;
        }

        /* Model name text */
        .model-name {
            font-size: 0.875rem;
            font-weight: 500;
            color: #4b5563;
        }

        /* Style the Model Types header */
        h3 {
            font-size: 1rem !important;
            font-weight: 600 !important;
            margin-bottom: 0.5rem !important;
            color: #374151 !important;
        }

        /* Hide sidebar by default */
        [data-testid="stSidebar"] {
            display: none;
        }


        /* Responsive adjustments */
        @media (max-width: 768px) {
            .main .block-container {
                padding: 1rem;
            }
        }
        </style>
    """