import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import plotly.express as px
import plotly.graph_objects as go

# Configuration
st.set_page_config(
    page_title="Real-Time Weather Dashboard",
    page_icon="🌤️",
    layout="wide"
)

# Add custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #005cb2;
    }
    .info-container {
        background-color: #f0f8ff;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
    }
    .temp-value {
        font-size: 3rem;
        font-weight: bold;
    }
    .metric-label {
        font-size: 0.9rem;
        color: #666;
    }
    .metric-value {
        font-size: 1.5rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# API Key setup
def get_api_key():
    api_key = st.sidebar.text_input("Enter your OpenWeatherMap API Key", type="password")
    if not api_key:
        st.sidebar.warning("Please enter your API key to use the dashboard")
        st.sidebar.info("Get your free API key at [OpenWeatherMap](https://openweathermap.org/api)")
        st.sidebar.info("This app uses the free tier which allows 60 calls/minute")
    return api_key

# Function to get weather data
def get_weather_data(api_key, location, units="metric"):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": location,
        "appid": api_key,
        "units": units
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()  # Raise exception for 4XX/5XX responses
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            st.error(f"Location '{location}' not found. Please check the spelling.")
        else:
            st.error(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        st.error(f"An error occurred: {err}")
        return None

# Function to get forecast data
def get_forecast_data(api_key, location, units="metric"):
    base_url = "https://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": location,
        "appid": api_key,
        "units": units
    }
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        if response.status_code == 404:
            st.error(f"Location '{location}' not found. Please check the spelling.")
        else:
            st.error(f"HTTP error occurred: {http_err}")
        return None
    except Exception as err:
        st.error(f"An error occurred: {err}")
        return None

# Convert timestamp to readable format
def format_time(timestamp, timezone_offset=0, format="%I:%M %p"):
    return datetime.utcfromtimestamp(timestamp + timezone_offset).strftime(format)

def format_date(timestamp, timezone_offset=0):
    return datetime.utcfromtimestamp(timestamp + timezone_offset).strftime("%A, %b %d")

# Main app
def main():
    # Sidebar
    st.sidebar.title("Settings")
    api_key = get_api_key()
    
    units = st.sidebar.selectbox(
        "Temperature Units",
        options=["metric", "imperial"],
        format_func=lambda x: "Celsius (°C)" if x == "metric" else "Fahrenheit (°F)"
    )
    
    unit_symbol = "°C" if units == "metric" else "°F"
    speed_unit = "m/s" if units == "metric" else "mph"
    
    # Location input
    location = st.sidebar.text_input("Enter City Name", "London")
    
    # Refresh rate
    refresh_interval = st.sidebar.slider(
        "Auto Refresh Interval (minutes)",
        min_value=1,
        max_value=60,
        value=15
    )
    
    # Refresh button
    col1, col2 = st.sidebar.columns([1, 1])
    with col1:
        manual_refresh = st.button("Refresh Now")
    
    with col2:
        auto_refresh = st.checkbox("Auto Refresh", value=True)
    
    if auto_refresh:
        st.sidebar.info(f"Data will refresh every {refresh_interval} minutes")
    
    # Title and description
    st.markdown('<p class="main-header">📊 Real-Time Weather Dashboard</p>', unsafe_allow_html=True)
    
    if not api_key:
        # Show demo image when no API key is provided
        st.info("👈 Please enter your OpenWeatherMap API key in the sidebar to get started.")
        st.image("https://via.placeholder.com/800x400?text=Weather+Dashboard+Preview", use_column_width=True)
        return
    
    # If we have an API key and location, get the weather data
    if api_key and location:
        weather_data = get_weather_data(api_key, location, units)
        
        if weather_data:
            # Display current weather
            timezone_offset = weather_data.get('timezone', 0)
            current_time = format_time(weather_data['dt'], timezone_offset)
            current_date = format_date(weather_data['dt'], timezone_offset)
            
            # City info
            col1, col2 = st.columns([2, 1])
            with col1:
                st.markdown(f"### {weather_data['name']}, {weather_data.get('sys', {}).get('country', '')}")
                st.markdown(f"**{current_date} | {current_time}**")
            
            with col2:
                st.markdown(f"**Sunrise:** {format_time(weather_data['sys']['sunrise'], timezone_offset)}")
                st.markdown(f"**Sunset:** {format_time(weather_data['sys']['sunset'], timezone_offset)}")
            
            # Current conditions
            col1, col2, col3, col4 = st.columns(4)
            
            # Current temperature and weather
            with col1:
                weather_icon = weather_data['weather'][0]['icon']
                icon_url = f"http://openweathermap.org/img/wn/{weather_icon}@2x.png"
                st.image(icon_url, width=100)
                st.markdown(f'<div class="temp-value">{round(weather_data["main"]["temp"])}{unit_symbol}</div>', unsafe_allow_html=True)
                st.markdown(f"*{weather_data['weather'][0]['description'].capitalize()}*")
            
            # Feels like and humidity
            with col2:
                st.markdown('<div class="metric-label">Feels Like</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{round(weather_data["main"]["feels_like"])}{unit_symbol}</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="metric-label">Humidity</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{weather_data["main"]["humidity"]}%</div>', unsafe_allow_html=True)
            
            # Wind and pressure
            with col3:
                st.markdown('<div class="metric-label">Wind Speed</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{weather_data["wind"]["speed"]} {speed_unit}</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="metric-label">Pressure</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{weather_data["main"]["pressure"]} hPa</div>', unsafe_allow_html=True)
            
            # Min/Max temperature
            with col4:
                st.markdown('<div class="metric-label">Min Temp</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{round(weather_data["main"]["temp_min"])}{unit_symbol}</div>', unsafe_allow_html=True)
                
                st.markdown('<div class="metric-label">Max Temp</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="metric-value">{round(weather_data["main"]["temp_max"])}{unit_symbol}</div>', unsafe_allow_html=True)
            
            st.markdown("---")
            
            # Get and process forecast data
            st.markdown('<p class="sub-header">5-Day Forecast</p>', unsafe_allow_html=True)
            forecast_data = get_forecast_data(api_key, location, units)
            
            if forecast_data:
                # Process forecast data
                forecast_list = forecast_data['list']
                forecast_df = pd.DataFrame(forecast_list)
                
                # Extract date and time
                forecast_df['date_time'] = pd.to_datetime(forecast_df['dt'], unit='s')
                forecast_df['date'] = forecast_df['date_time'].dt.date
                forecast_df['time'] = forecast_df['date_time'].dt.strftime('%H:%M')
                
                # Extract temperature and weather description
                forecast_df['temp'] = forecast_df['main'].apply(lambda x: x['temp'])
                forecast_df['feels_like'] = forecast_df['main'].apply(lambda x: x['feels_like'])
                forecast_df['humidity'] = forecast_df['main'].apply(lambda x: x['humidity'])
                forecast_df['description'] = forecast_df['weather'].apply(lambda x: x[0]['description'])
                forecast_df['icon'] = forecast_df['weather'].apply(lambda x: x[0]['icon'])
                
                # Daily average temperature
                daily_temp = forecast_df.groupby('date')['temp'].mean().reset_index()
                daily_temp['date_str'] = daily_temp['date'].astype(str)
                
                # Plot temperature forecast
                fig = px.line(
                    daily_temp, 
                    x='date_str', 
                    y='temp',
                    markers=True,
                    labels={'date_str': 'Date', 'temp': f'Temperature ({unit_symbol})'},
                    title='5-Day Temperature Forecast'
                )
                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title=f"Temperature ({unit_symbol})",
                    plot_bgcolor='rgba(240,248,255,0.8)',
                    title_font_size=20
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # Display hourly forecast for the next 24 hours
                st.markdown('<p class="sub-header">Hourly Forecast (Next 24h)</p>', unsafe_allow_html=True)
                
                # Take first 8 entries (24 hours, as entries are 3 hours apart)
                hourly = forecast_df.iloc[:8].copy()
                hourly['hour'] = hourly['date_time'].dt.strftime('%I %p')
                
                # Display hourly forecast cards
                cols = st.columns(len(hourly))
                for i, (_, row) in enumerate(hourly.iterrows()):
                    with cols[i]:
                        icon_url = f"http://openweathermap.org/img/wn/{row['icon']}@2x.png"
                        st.image(icon_url, width=50)
                        st.markdown(f"**{row['hour']}**")
                        st.markdown(f"{round(row['temp'])}{unit_symbol}")
                        st.markdown(f"{row['humidity']}% humidity")
                
                # Display detailed forecast table
                st.markdown('<p class="sub-header">Detailed Forecast</p>', unsafe_allow_html=True)
                
                # Filter columns for display
                display_df = forecast_df[['date_time', 'temp', 'feels_like', 'humidity', 'description']].copy()
                display_df.columns = ['DateTime', 'Temperature', 'Feels Like', 'Humidity (%)', 'Conditions']
                display_df['DateTime'] = display_df['DateTime'].dt.strftime('%Y-%m-%d %H:%M')
                display_df['Temperature'] = display_df['Temperature'].round().astype(int).astype(str) + unit_symbol
                display_df['Feels Like'] = display_df['Feels Like'].round().astype(int).astype(str) + unit_symbol
                
                st.dataframe(display_df, use_container_width=True)
                
                # Add weather map
                st.markdown('<p class="sub-header">Weather Map</p>', unsafe_allow_html=True)
                st.info("🌍 For a detailed weather map, visit [OpenWeatherMap](https://openweathermap.org/weathermap)")
                
                # Add a placeholder for a map (in a real app, you might use folium or other mapping libraries)
                map_placeholder = st.empty()
                map_placeholder.info("Weather map feature would be available here with premium API access")
            
            # Add last updated info
            st.sidebar.markdown("---")
            st.sidebar.markdown(f"Last updated: {datetime.now().strftime('%H:%M:%S')}")

if __name__ == "__main__":
    main()