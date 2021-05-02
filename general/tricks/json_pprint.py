import requests
from pprint import pprint

url = 'https://api.github.com/users/ganeshkumarm1'
user = requests.get(url).json()

pprint(user)
