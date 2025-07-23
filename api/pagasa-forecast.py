from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import sys
import os

# Add the parent directory to the sys.path to allow importing pagasa_scraper
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'utils'))

from pagasa_scraper import get_daily_weather_forecast

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', 'https://ulanbadyan.vercel.app/')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        forecast_data = get_daily_weather_forecast()
        self.wfile.write(json.dumps(forecast_data).encode('utf-8'))

    def do_OPTIONS(self):
        # Handle CORS preflight requests
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', 'https://ulanbadyan.vercel.app/')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, handler)
    print(f'Starting httpd server on port 8000')
    httpd.serve_forever()