import requests

def search_drugs(pattern):
    endpoint = "https://api.fda.gov/drug/label.json"
    params = {
        "search": f"openfda.brand_name:{pattern}* OR openfda.generic_name:{pattern}*",
        "limit": 10  # Adjust as needed
    }
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["results"]
    else:
        return []

def get_drug_info(drug_id):
    endpoint = f"https://api.fda.gov/drug/label.json?search=set_id:{drug_id}"
    response = requests.get(endpoint)
    if response.status_code == 200:
        data = response.json()
        return data["results"][0] if data["results"] else None
    else:
        return None

# Example batch of words extracted from OCR
words_batch =  [
        "Ixlu",
        "Capouls",
        "Calcitriol",
        "Capsules",
        "Bonerise"
    ]

res = []
for word in words_batch:
    drugs = search_drugs(word)
    if drugs:
        for drug in drugs:
            drug_info = get_drug_info(drug["set_id"])
            if drug_info:
                prod = {}
                prod["Drug name"] = drug_info['openfda'].get('brand_name', ['Unknown'])[0]
                prod["Generic name"] = drug_info['openfda'].get('generic_name', ['Unknown'])[0]
                prod["Manufacturer"] = drug_info['openfda'].get('manufacturer_name', ['Unknown'])[0]
                if 'adverse_reactions' in drug_info:
                    prod["Side effects"] = drug_info['adverse_reactions']
                else:
                    prod["Side effects"] = "Not available"
                res.append(prod)

for item in res:
    print(f"Drug Name: {item['Drug name']}")
    print(f"Generic Name: {item['Generic name']}")
    print(f"Manufacturer: {item['Manufacturer']}")
    print("Side Effects:")
    if isinstance(item['Side effects'], list):
        for effect in item['Side effects']:
            print(f"- {effect}")
    else:
        print(item['Side effects'])
    print("---")
