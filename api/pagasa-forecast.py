import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))  # Add parent directory to path

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from utils.pagasa_scraper import get_daily_weather_forecast

def handler(request):
    # Get forecast data
    try:
        forecast_data = get_daily_weather_forecast()
        if forecast_data is None:
            raise Exception("Failed to retrieve forecast data.")
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Content-type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type',
            },
            'body': json.dumps({'error': str(e), 'message': 'Internal Server Error'})
        }

    # Set CORS headers
    headers = {
        'Content-type': 'application/json',
        'Access-Control-Allow-Origin': '*',
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

# Local development server
class LocalHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:5173')  # Restrict to Vue frontend
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        try:
            forecast_data = get_daily_weather_forecast()
            if forecast_data is None:
                raise Exception("Failed to retrieve forecast data.")
            self.wfile.write(json.dumps(forecast_data).encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e), 'message': 'Internal Server Error'}).encode('utf-8'))

    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', 'http://localhost:5173')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    # Check if running in Vercel environment
    if os.environ.get('VERCEL'):
        # In Vercel, the `handler` function is the entry point
        # No need to run a server here, Vercel handles it
        pass
    else:
        # Local development
        server_address = ('', 8000)
        httpd = HTTPServer(server_address, LocalHandler)
        print(f'Starting httpd server on port 8000')
        httpd.serve_forever()