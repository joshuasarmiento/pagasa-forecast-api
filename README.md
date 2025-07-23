# PAGASA Forecast API

This project provides a simple Python API to fetch daily weather forecasts from the PAGASA (Philippine Atmospheric, Geophysical and Astronomical Services Administration) website. It scrapes data from the official PAGASA weather forecast page and serves it as a JSON API.

## Features

*   **Daily Weather Forecast:** Retrieves comprehensive daily weather information including synopsis, weather conditions, wind and coastal water conditions, temperature, humidity, tides, and astronomical information.
*   **CORS Enabled:** Allow all origins for now; restrict later
*   **Data Caching:** Implements a basic caching mechanism to reduce the number of requests to the PAGASA website and improve response times.

## Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository_url>
    cd pagasa-forecast-api
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```bash
    pip install requests beautifulsoup4
    ```

## Usage

To start the API server, run the `pagasa-forecast.py` script:

```bash
python api/pagasa-forecast.py
```

The API will be accessible at `http://localhost:8000`.

## API Endpoints

### `GET /`

Returns the daily weather forecast data in JSON format.

**Example Response:**

```json
{
    "issued_at": "Issued at 5:00 AM, 23 July 2025",
    "synopsis": "...",
    "forecast_weather_conditions": [
        {
            "place": "Luzon",
            "weather_condition": "...",
            "caused_by": "...",
            "impacts": "..."
        }
    ],
    "forecast_wind_conditions": [
        {
            "place": "Luzon",
            "speed": "...",
            "direction": "...",
            "coastal_water": "..."
        }
    ],
    "temperature_humidity": {
        "Metro Manila": {
            "max": {"value": "32°C", "time": "2:00 PM"},
            "min": {"value": "25°C", "time": "5:00 AM"}
        }
    },
    "astronomical_information": {
        "Sun Rise": "5:30 AM",
        "Sun Set": "6:30 PM",
        "Moon Rise": "...",
        "Moon Set": "...",
        "Illumination": "..."
    },
    "tidal_predictions": [
        {
            "type": "High Tide",
            "value": "1.5m",
            "time": "10:00 AM"
        }
    ]
}
```

## Technologies Used

*   Python 3
*   `http.server` (built-in Python module)
*   `requests`
*   `BeautifulSoup4`
