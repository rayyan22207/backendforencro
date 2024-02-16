import requests

endpoint =' http://127.0.0.1:8000/api/' # connects to the server and api

get_endpoint = requests.post(endpoint, params={'abc': 123}, json={'query':'Hello world'}) # after connecting, getting the response 
print(get_endpoint)# printting the result
print(get_endpoint.json())# printting the result in json
print(get_endpoint.status_code)# printting the result's status code (e.g 404)