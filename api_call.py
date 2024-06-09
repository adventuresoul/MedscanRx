import requests

# Define the base URL for the OpenFDA drug endpoint
base_url = "https://api.fda.gov/drug/label.json"

# Define the parameters for the query
params = {
    "search": "ibuprofen",  # The drug name you want to search for
    "limit": 1              # Limit the number of results to 1 for simplicity
}

# Make the GET request to the OpenFDA API
response = requests.get(base_url, params=params)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    data = response.json()
    # Print the result
    # print(data)
else:
    print(f"Error: {response.status_code}")

print(len(data['results']))
if "results" in data and len(data["results"]) > 0:
    for result in data['results']:
        print(f"Drug Name: {result.get('openfda', {}).get('brand_name', 'N/A')}")
        print(f"spl_product_data_elements: {result.get("spl_product_data_elements", "N/A")}")
        print("-" * 50)
        print(f"Purpose: {result.get('purpose', 'N/A')}")
        print("-" * 50)
        #print(f"Warnings: {result.get('warnings', 'N/A')}")
else:
    print("No results found.")
