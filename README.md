# Real-Time Weather Dashboard

A Streamlit application that displays real-time weather information and forecasts using the OpenWeatherMap API.

## Features

- **Current Weather Conditions**: Temperature, humidity, wind speed, and more
- **5-Day Forecast**: Visualized temperature trends
- **Hourly Forecast**: Next 24 hours forecast
- **Detailed Data Tables**: Comprehensive weather data
- **Customizable Settings**: Change units (Celsius/Fahrenheit) and location
- **Auto-Refresh**: Keep your weather data up to date

## Getting Started

### Prerequisites

- Python 3.7+
- OpenWeatherMap API key (free tier available at [OpenWeatherMap](https://openweathermap.org/api))

### Installation

1. Clone this repository or download the source code
2. Install the required packages:

```bash
pip install -r requirements.txt
```

### Running the Application

Run the Streamlit app:

```bash
streamlit run weather_dashboard.py
```

### Configuration

When the app starts:

1. Enter your OpenWeatherMap API key in the sidebar
2. Set your preferred temperature units (Celsius or Fahrenheit)
3. Enter the city name you want weather information for
4. Adjust auto-refresh settings if desired

## Data Sources

This application uses the following OpenWeatherMap API endpoints:
- Current Weather API
- 5-Day/3-Hour Forecast API

## Screenshots

![Dashboard Preview](https://via.placeholder.com/800x400?text=Weather+Dashboard+Preview)

## Customization

You can customize the dashboard by:
- Changing the units between metric and imperial
- Setting different auto-refresh intervals
- Searching for any city supported by OpenWeatherMap

## License

This project is for educational purposes and can be freely used and modified.

## Acknowledgements

- [OpenWeatherMap](https://openweathermap.org/) for providing the weather data API
- [Streamlit](https://streamlit.io/) for the web application framework
- [Plotly](https://plotly.com/) for interactive data visualization