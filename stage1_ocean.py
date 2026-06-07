import os
import requests
from dotenv import load_dotenv

load_dotenv()

OCEAN_API_KEY = os.getenv("OCEAN_API_KEY")

def find_lookalike_companies(seed_domain):
    print(f"\n[Stage 1] Finding lookalike companies for: {seed_domain}")

    url = "https://api.ocean.io/v3/search/companies"

    headers = {
        "x-api-token": OCEAN_API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "size": 10,
        "companiesFilters": {
            "lookalikeDomains": [seed_domain]
        }
    }

    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()

        domains = []
        for item in data.get("companies", []):
            company = item.get("company", {})
            domain = company.get("domain")
            name = company.get("name", "Unknown")
            if domain:
                domains.append(domain)
                print(f"  → {name} ({domain})")

        print(f"\n[Stage 1] ✅ Found {len(domains)} lookalike companies")
        return domains

    except requests.exceptions.HTTPError as e:
        print(f"[Stage 1] HTTP Error: {e}")
        print(f"Response: {response.text}")
        return []
    except Exception as e:
        print(f"[Stage 1] Error: {e}")
        return []

if __name__ == "__main__":
    results = find_lookalike_companies("stripe.com")
    print("\nFinal domain list:", results)
