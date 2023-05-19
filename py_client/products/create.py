import requests

endpoint = 'http://localhost:8000/api/products/'

data = {
    'title': 'Jeans',
    'description': 'Fancy jeans for cool guys',
    'price': 50
}

response = requests.post(endpoint, data)

print(response.json())
