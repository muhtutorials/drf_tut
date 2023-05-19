import requests

endpoint = 'http://localhost:8000/api/products/1/'

data = {
    'price': 35
}

response = requests.patch(endpoint, data)

print(response.json())