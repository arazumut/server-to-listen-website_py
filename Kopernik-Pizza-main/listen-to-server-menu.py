import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class Restaurant:
    def __init__(self, dataset_file):
        try:
            with open(dataset_file, 'r') as file:
                self.menu = json.load(file)
        except FileNotFoundError:
            print(f"Error: The file {dataset_file} does not exist.")
            self.menu = []
        except json.JSONDecodeError:
            print(f"Error: The file {dataset_file} is not a valid JSON file.")
            self.menu = []

    def list_meals(self, is_vegetarian=False, is_vegan=False):
        filtered_menu = []
        for meal in self.menu:
            if 'id' not in meal:
                print("Error: Missing 'id' in meal:", meal)
                continue  
            if (not is_vegetarian or self._is_meal_vegetarian(meal)) and \
               (not is_vegan or self._is_meal_vegan(meal)):
                filtered_menu.append({
                    'id': meal['id'],
                    'name': meal['name'],
                    'price': meal['price']  # Fiyatı buradan alınacak
                })
        return filtered_menu

    def get_meal(self, meal_id):
        for meal in self.menu:
            if meal['id'] == meal_id:
                return meal
        return None

    def _is_meal_vegetarian(self, meal):
        return all(self._is_ingredient_vegetarian(ingredient) for ingredient in meal['ingredients'])

    def _is_meal_vegan(self, meal):
        return all(self._is_ingredient_vegan(ingredient) for ingredient in meal['ingredients'])

    def _is_ingredient_vegetarian(self, ingredient):
        # Burada bir mantık ekleyebilirsiniz
        return True

    def _is_ingredient_vegan(self, ingredient):
        # Burada bir mantık ekleyebilirsiniz
        return True

class RequestHandler(BaseHTTPRequestHandler):
    def _set_headers(self, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        parsed_path = urlparse(self.path)
        params = parse_qs(parsed_path.query)
        response = None

        if parsed_path.path == '/listMeals':
            is_vegetarian = params.get('is_vegetarian', ['false'])[0].lower() == 'true'
            is_vegan = params.get('is_vegan', ['false'])[0].lower() == 'true'
            response = restaurant.list_meals(is_vegetarian=is_vegetarian, is_vegan=is_vegan)

        if response is None:
            self._set_headers(404)
            self.wfile.write(b"Resource not found")
        else:
            self._set_headers(200)
            self.wfile.write(json.dumps(response).encode())

host = 'localhost'
port = 5500
restaurant = Restaurant('food.json')  

server = HTTPServer((host, port), RequestHandler)
print(f'Server running on http://{host}:{port}')
try:
    server.serve_forever()
except KeyboardInterrupt:
    print('\nShutting down the server...')
    server.socket.close()
