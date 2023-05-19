import requests

endpoint = 'http://localhost:8000/api/products/2/'

response = requests.delete(endpoint)

print(response)
