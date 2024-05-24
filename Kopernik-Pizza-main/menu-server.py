from http.server import BaseHTTPRequestHandler, HTTPServer
import json

# Menü verilerini temsil eden bir liste
menu_items = [
    {"name": "Hamburger", "price": 10},
    {"name": "Pizza", "price": 12},
    {"name": "Salad", "price": 8}
]

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Gelen isteğin rotasına göre işlem yapma
        if self.path == '/menu':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            # Menü verilerini JSON formatında gönderme
            self.wfile.write(json.dumps(menu_items).encode())
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not Found')

def run(server_class=HTTPServer, handler_class=RequestHandler, port=5500):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print('Starting httpd on port', port)
    httpd.serve_forever()

if __name__ == "__main__":
    run()
