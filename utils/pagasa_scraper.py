import requests
from bs4 import BeautifulSoup
import json
import re
import time

cache = None
cache_time = None
CACHE_DURATION = 3600  # 1 hour in seconds

def get_daily_weather_forecast():
    global cache, cache_time
    if cache and cache_time and (time.time() - cache_time < CACHE_DURATION):
        return cache
    
    url = "https://www.pagasa.dost.gov.ph/weather#daily-weather-forecast"
    try:
        response = requests.get(url)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching URL: {e}")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    forecast_data = {}

    # Extract issue date
    issue_div = soup.find('div', class_='issue')
    if issue_div:
        issue_text = issue_div.find('b').get_text(strip=True) if issue_div.find('b') else ""
        forecast_data['issued_at'] = issue_text

    # Extract synopsis
    synopsis_panel = soup.find('div', class_='panel-heading', string='Synopsis')
    if synopsis_panel:
        synopsis_body = synopsis_panel.find_next('div', class_='panel-body')
        if synopsis_body:
            forecast_data['synopsis'] = synopsis_body.find('p').get_text(strip=True) if synopsis_body.find('p') else ""

    # Extract forecast weather conditions
    weather_table = soup.find('h3', string='Forecast Weather Conditions').find_next('table')
    if weather_table:
        weather_conditions = []
        for row in weather_table.find('tbody').find_all('tr'):
            cols = row.find_all('td')
            if len(cols) == 4:
                weather_conditions.append({
                    'place': cols[0].get_text(strip=True),
                    'weather_condition': cols[1].get_text(strip=True),
                    'caused_by': cols[2].get_text(strip=True),
                    'impacts': cols[3].get_text(strip=True)
                })
        forecast_data['forecast_weather_conditions'] = weather_conditions

    # Extract wind and coastal water conditions
    wind_table = soup.find('h3', string='Forecast Wind and Coastal Water Conditions').find_next('table')
    if wind_table:
        wind_conditions = []
        for row in wind_table.find('tbody').find_all('tr'):
            cols = row.find_all('td')
            if len(cols) == 4:
                wind_conditions.append({
                    'place': cols[0].get_text(strip=True),
                    'speed': cols[1].get_text(strip=True),
                    'direction': cols[2].get_text(strip=True),
                    'coastal_water': cols[3].get_text(strip=True)
                })
        forecast_data['forecast_wind_conditions'] = wind_conditions

    # Extract temperature and relative humidity
    temp_table = soup.find('h3', string='Temperature and Relative Humidity').find_next('table')
    if temp_table:
        temp_data = {}
        for row in temp_table.find('tbody').find_all('tr'):
            cols = row.find_all('td')
            if len(cols) == 5:
                metric = cols[0].get_text(strip=True)
                temp_data[metric] = {
                    'max': {'value': cols[1].get_text(strip=True), 'time': cols[2].get_text(strip=True)},
                    'min': {'value': cols[3].get_text(strip=True), 'time': cols[4].get_text(strip=True)}
                }
        forecast_data['temperature_humidity'] = temp_data

    # Extract tides and astronomical information
    tides_astro_table = soup.find('h3', string='Tides and Astronomical Information').find_next('table')
    if tides_astro_table:
        astro_data = {}
        tidal_data = []
        rows = tides_astro_table.find('tbody').find_all('tr')
        for row in rows[1:6]:  # Astronomy rows (Sun Rise to Illumination)
            cols = row.find_all('td')
            if len(cols) >= 3:
                astro_data[cols[0].get_text(strip=True)] = cols[1].get_text(strip=True)
        for row in rows[7:]:  # Tidal prediction rows
            cols = row.find_all('td')
            if len(cols) >= 3 and cols[1].get_text(strip=True) != '--':
                tidal_data.append({
                    'type': cols[0].get_text(strip=True),
                    'value': cols[1].get_text(strip=True),
                    'time': cols[2].get_text(strip=True)
                })
        forecast_data['astronomical_information'] = astro_data
        forecast_data['tidal_predictions'] = tidal_data
    
    # Update cache
    cache = forecast_data
    cache_time = time.time()
    return forecast_data

if __name__ == "__main__":
    forecast = get_daily_weather_forecast()
    if forecast:
        print(json.dumps(forecast, indent=4))
    else:
        print("Failed to retrieve daily weather forecast.")