# Weather App

A desktop weather application developed using Python and PySide6, integrated with the Open-Meteo API to retrieve and display weather information for user-specified cities. The application combines API-driven data retrieval with a responsive graphical interface, weather-dependent backgrounds, and animated transitions.

## Overview

The application allows users to search for a city and view its current weather information through a desktop interface. It uses geocoding to resolve city names into geographic coordinates, retrieves weather data from the API, and updates the interface according to the returned conditions.

The project focuses on API integration, modular application design, GUI development, error handling, and visual presentation.

## Features

- **City Search and Geocoding:** Converts user-entered city names into geographic coordinates before retrieving weather data.
- **Weather Data Retrieval:** Fetches weather information through HTTP requests to the Open-Meteo API.
- **Weather Information Display:** Displays temperature, relative humidity, wind speed, and weather conditions.
- **Dynamic Backgrounds:** Selects weather-specific background images for clear, cloudy, rainy, snowy, stormy, and foggy conditions.
- **Animated Transitions:** Uses Qt property animations and opacity effects to create crossfade transitions between backgrounds.
- **Graphical User Interface:** Provides a clean desktop interface with translucent panels, rounded corners, and consistent visual styling.
- **Data Freshness Information:** Displays the elapsed time since the weather data was retrieved.
- **Error Handling:** Handles invalid city searches, unsuccessful API requests, and unexpected responses.
- **Modular Design:** Separates API and data-processing logic from GUI components to improve maintainability and debugging.

## Technologies Used

- **Python** — Application logic and data processing
- **PySide6** — Desktop GUI development
- **Qt Property Animations** — Background transition effects
- **Requests** — HTTP communication with external APIs
- **Open-Meteo API** — Geocoding and weather data
- **pathlib** — Filesystem path management
- **datetime and zoneinfo** — Time-related processing, where applicable

## System Architecture

The application consists of two primary modules.

### 1. Backend — `weather_app.py`

Responsible for communication with the external weather services and processing the returned data.

- Resolves city names into geographic coordinates.
- Sends requests to retrieve weather information for the selected location.
- Processes API responses into structured values for the interface.
- Handles request failures, invalid locations, and unexpected response data.

### 2. Frontend — `weather_gui.py`

Responsible for the graphical interface and user interaction.

- Accepts city names through the search interface.
- Invokes the backend to retrieve weather information.
- Displays the returned weather values and update information.
- Selects background images according to weather conditions.
- Manages animated background transitions and interface updates.
- Presents errors when a search or data retrieval operation fails.

### Data Flow

1. The user enters a city name.
2. The backend requests geographic coordinates from the geocoding service.
3. The coordinates are used to request weather data.
4. The response is processed and returned to the GUI.
5. The GUI updates the weather information and selects the corresponding background.
6. An animated transition presents the updated visual state.

## Project Structure

```text
weather-app/
├── weather_app.py
├── weather_gui.py
├── images/
│   ├── background_weather.png
│   ├── background_weather_rainy.png
│   ├── background_weather_snowy.png
│   ├── background_weather_stormy.png
│   ├── background_weather_cloudy.png
│   └── background_weather_fog.png
├── README.md
├── requirements.txt
└── .gitignore
```

## Installation and Execution

### Prerequisites

- Python 3.10 or later
- An active internet connection

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/weather-app.git
cd weather-app
```

Replace `YOUR_USERNAME` with your GitHub username.

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
```

On Windows:

```bash
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the application

```bash
python weather_gui.py
```

## API Integration

The application uses the Open-Meteo services for location geocoding and weather retrieval.

- [Open-Meteo Weather Forecast API](https://open-meteo.com/en/docs)
- [Open-Meteo Geocoding API](https://open-meteo.com/en/docs/geocoding-api)

Weather data is model-based and may differ slightly from other weather providers or local weather station observations.

## Testing and Validation

The application can be validated through the following checks:

- Searching for multiple valid cities and verifying location-specific results.
- Testing invalid city names and unsuccessful API requests.
- Comparing displayed values with the API response and independent weather sources.
- Verifying temperature, humidity, wind speed, and weather-condition mapping.
- Testing background selection and transitions across different conditions.
- Checking behavior when API responses contain missing or unexpected fields.

## Future Enhancements

- Hourly and multi-day weather forecasts
- Temperature and precipitation visualizations
- Favorite locations and search history
- Configurable temperature and wind-speed units
- Additional weather metrics and forecast summaries
- Improved accessibility and interface customization

## License

No license has been specified yet. A license can be added when the project's distribution and reuse terms are decided.
