import httpx
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

EVENT_BASE_URL = "https://api.fda.gov/drug/event.json"
TIMEOUT = 30

async def fetch_adverse_effects(drug_name: str):
    api_key = os.getenv("openfdakey")
    params = {
        'search': f'patient.drug.medicinalproduct:"{drug_name}"',
        'limit': 1
    }

    headers = {}
    if api_key:
        headers['Authorization'] = f'Bearer {api_key}'

    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        try:
            response = await client.get(EVENT_BASE_URL, params=params, headers=headers)
            response.raise_for_status()
            data = response.json()
        except httpx.HTTPStatusError as exc:
            print(f"HTTP error fetching data for {drug_name}: {exc.response.status_code} - {exc.response.text}")
            return []
        except httpx.RequestError as exc:
            print(f"Error fetching data for {drug_name}: {exc}")
            return []

    if not data.get('results'):
        print(f"No results found for {drug_name}")
        return []

    adverse_effects = [reaction.get('reactionmeddrapt', '') for reaction in data['results'][0].get('patient', {}).get('reaction', [])]

    return adverse_effects

# Example usage
# import asyncio
# adverse_effects = asyncio.run(fetch_adverse_effects('aspirin'))
# print(adverse_effects)
