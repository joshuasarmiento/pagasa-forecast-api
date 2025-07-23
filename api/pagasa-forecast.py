import json
from http.server import BaseHTTPRequestHandler
from utils.pagasa_scraper import get_daily_weather_forecast

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        print("do_GET function invoked")
        try:
            forecast_data = get_daily_weather_forecast()
            if forecast_data is None:
                raise Exception("Failed to retrieve forecast data.")

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', 'https://ulanbadyan.vercel.app/')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps(forecast_data).encode('utf-8'))
        except Exception as e:
            print(f"Error in do_GET: {str(e)}")
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', 'https://ulanbadyan.vercel.app/')
            self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
            self.send_header('Access-Control-Allow-Headers', 'Content-Type')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e), 'message': 'Internal Server Error'}).encode('utf-8'))

    def do_OPTIONS(self):
        print("do_OPTIONS function invoked")
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', 'https://ulanbadyan.vercel.app/')
        self.send_header('Access-Control-Allow-Methods', 'GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

if __name__ == '__main__':
    from http.server import HTTPServer
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, handler)
    print('serving at', server_address)
    httpd.serve_forever()
