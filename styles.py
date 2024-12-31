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
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            z-index: 1000;
            min-width: 200px;
        }

        /* Model type button styles */
        .model-button {
            background-color: var(--model-color);
            border: none;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            color: white;
            font-weight: bold;
            transition: all 0.3s ease;
            margin: 0.25rem;
            cursor: pointer;
        }

        .model-button.active {
            transform: translateY(-2px);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }

        /* Model colors */
        .model-asr { --model-color: #FF4B4B; }
        .model-nmt { --model-color: #4CAF50; }
        .model-tts { --model-color: #2196F3; }

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
        </style>
    """