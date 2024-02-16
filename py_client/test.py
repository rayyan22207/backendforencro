import requests

# Set the API endpoint
url = 'http://192.168.18.4:8000/api/auth/register/'  # Replace with your API URL

# Define the login credentials
credentials = {
    'username': 'rayyan22207@gmail.com',
    'password': 'idkidkidk',
}

response = requests.post(url, data=credentials)

# Check the response status code
if response.status_code == 200:
    # Authentication successful
    data = response.json()
    token = data.get('token')
    if token:
        print(f'Authentication successful. Token: {token}')
    else:
        print('Token not found in the response data.')
elif response.status_code == 400:
    # Invalid request
    data = response.json()
    error_message = data.get('error', 'Unknown error')
    print(f'Invalid request: {error_message}')
elif response.status_code == 401:
    # Authentication failed
    data = response.json()
    error_message = data.get('non_field_errors', 'Authentication failed')
    print(f'Authentication failed: {error_message}')
else:
    # Other response status code
    print(f'Unexpected status code: {response.status_code}')