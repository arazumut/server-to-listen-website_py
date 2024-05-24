import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class Restaurant:
    def __init__(self, dataset_file):
        with open(dataset_file, 'r') as file:
            self.menu = json.load(file)

    def list_meals(self, is_vegetarian=False, is_vegan=False):
        filtered_menu = []
        for meal in self.menu:
            if (not is_vegetarian or self._is_meal_vegetarian(meal)) and \
               (not is_vegan or self._is_meal_vegan(meal)):
                filtered_menu.append({
                    'id': meal['id'],
                    'name': meal['name'],
                    'ingredients': meal['ingredients']
                })
        return filtered_menu

    def get_meal(self, meal_id):
        for meal in self.menu:
            if meal['id'] == meal_id:
                return meal
        return None

    def quality(self, meal_id, **kwargs):
        meal = self.get_meal(meal_id)
        if meal:
            total_quality = sum(self._ingredient_quality(ingredient, kwargs.get(ingredient, 'high')) for ingredient in meal['ingredients'])
            return {'quality': total_quality}
        else:
            return {'error': 'Meal not found'}

    def price(self, meal_id, **kwargs):
        meal = self.get_meal(meal_id)
        if meal:
            total_price = sum(self._ingredient_price(ingredient, kwargs.get(ingredient, 'high')) for ingredient in meal['ingredients'])
            return {'price': total_price}
        else:
            return {'error': 'Meal not found'}

    def _is_meal_vegetarian(self, meal):
        for ingredient in meal['ingredients']:
            if not self._is_ingredient_vegetarian(ingredient):
                return False
        return True


    def _is_meal_vegan(self, meal):
        for ingredient in meal['ingredients']:
            if not self._is_ingredient_vegan(ingredient):
                return False
        return True

    def _is_ingredient_vegetarian(self, ingredient):
        
        return True

    def _is_ingredient_vegan(self, ingredient):
        
        return True

    def _ingredient_quality(self, ingredient, quality):
        
        return 30  # Placeholder value

    def _ingredient_price(self, ingredient, quality):
        
        return 1.99  

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        params = parse_qs(parsed_path.query)

        if parsed_path.path == '/listMeals':
            is_vegetarian = params.get('is_vegetarian', ['false'])[0].lower() == 'true'
            is_vegan = params.get('is_vegan', ['false'])[0].lower() == 'true'
            response = restaurant.list_meals(is_vegetarian=is_vegetarian, is_vegan=is_vegan)
        elif parsed_path.path == '/getMeal':
            meal_id = int(params.get('id', [0])[0])
            response = restaurant.get_meal(meal_id)
        else:
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode('utf-8')
        parsed_data = parse_qs(post_data)

        if self.path == '/quality':
            meal_id = int(parsed_data.get('meal_id', [0])[0])
            kwargs = {k: v[0] for k, v in parsed_data.items() if k != 'meal_id'}
            response = restaurant.quality(meal_id, **kwargs)
        elif self.path == '/price':
            meal_id = int(parsed_data.get('meal_id', [0])[0])
            kwargs = {k: v[0] for k, v in parsed_data.items() if k != 'meal_id'}
            response = restaurant.price(meal_id, **kwargs)
        else:
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode())

host = 'localhost'
port = 5500
restaurant = Restaurant('dataset.json')

try:
    
    server = HTTPServer((host, port), RequestHandler)
    print(f'Server running on http://{host}:{port}')
    server.serve_forever()
except KeyboardInterrupt:
    print('\nShutting down the server...')
    server.socket.close()
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

class Restaurant:
    def __init__(self, dataset_file):
        with open(dataset_file, 'r') as file:
            self.menu = json.load(file)

    

class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        params = parse_qs(parsed_path.query)

        if parsed_path.path == '/listMeals':
            is_vegetarian = params.get('is_vegetarian', ['false'])[0].lower() == 'true'
            is_vegan = params.get('is_vegan', ['false'])[0].lower() == 'true'
            response = restaurant.list_meals(is_vegetarian=is_vegetarian, is_vegan=is_vegan)
        elif parsed_path.path == '/getMeal':
            meal_id = int(params.get('id', [0])[0])
            response = restaurant.get_meal(meal_id)
        elif parsed_path.path == '/getMealById':  # Düzeltme burada
            meal_id = int(params.get('id', [0])[0])
            meal = restaurant.get_meal(meal_id)
            if meal:
                response = meal
            else:
                response = {'error': 'Meal not found'}
        else:
            self.send_response(404)
            self.end_headers()
            return

        self.send_response(200)
        self.send_header('Content-type', 'text/html')  
        self.end_headers()

        # index.html dosyasını oku ve içeriğini gönder
        with open('internTaskwebSites.html', 'r') as file:
            html_content = file.read()

        self.wfile.write(html_content.encode())


    # Diğer sınıf metotları burada

host = 'localhost'
port = 5500
restaurant = Restaurant('dataset.json')

try:
    server = HTTPServer((host, port), RequestHandler)
    print(f'Server running on http://{host}:{port}')
    server.serve_forever()
except KeyboardInterrupt:
    print('\nShutting down the server...')
    server.socket.close()
