import json
from utils.pagasa_scraper import get_daily_weather_forecast

def handler(request):
    print("Handler function invoked")  # Add logging for debugging
    # Get forecast data
    try:
        forecast_data = get_daily_weather_forecast()
        if forecast_data is None:
            raise Exception("Failed to retrieve forecast data.")
    except Exception as e:
        print(f"Error in handler: {str(e)}")  # Log errors
        return {
            'statusCode': 500,
            'headers': {
                'Content-type': 'application/json',
                'Access-Control-Allow-Origin': 'https://ulanbadyan.vercel.app/',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps({'error': str(e), 'message': 'Internal Server Error'})
        }

    # Set CORS headers
    headers = {
        'Content-type': 'application/json',
        'Access-Control-Allow-Origin': 'https://ulanbadyan.vercel.app/',
        'Access-Control-Allow-Methods': 'GET, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type',
    }

    # Handle OPTIONS preflight request
    if request.method == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': headers,
            'body': ''
        }

    # Handle GET request
    return {
        'statusCode': 200,
        'headers': headers,
        'body': json.dumps(forecast_data)
    }