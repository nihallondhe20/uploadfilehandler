import requests

# Replace 'your_table_name' with the name of the table you want to delete
table_name = 'your_table_name'

# Define the API endpoint URL
api_url = f'http://localhost:8000/api/delete_table/{table_name}/'

# Send a DELETE request to the API
response = requests.delete(api_url)

# Check the response
if response.status_code == 200:
    print(f"Table '{table_name}' deleted successfully.")
else:
    print(f"Error: {response.status_code} - {response.json().get('error', 'Unknown error')}")