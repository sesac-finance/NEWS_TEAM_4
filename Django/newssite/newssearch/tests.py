# from django.test import TestCase
import requests
# Create your tests here.

base_url = 'http://127.0.0.1:8000/'
admin = 'admin/'
test_url = 'http://127.0.0.1:8000/api/team4/'

result = requests.get(base_url + 'details/aaa')
print(result)