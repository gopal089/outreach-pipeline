import os
import requests
import time
from dotenv import load_dotenv

load_dotenv()

PROSPEO_API_KEY = os.getenv("PROSPEO_API_KEY")

HEADERS = {
    "Content-Type": "application/json",
    "X-KEY": PROSPEO_API_KEY
}

def search_people(domain):
    """Step 1: Search for decision makers by domain, get person_ids"""
    payload = {
        "page": 1,
        "filters": {
            "company": {
                "websites": {
                    "include": [domain]
                }
            },
            "person_seniority": {
                "include": ["C-Suite", "Vice President", "Founder/Owner"]
            }
        }
    }
    response = requests.post(
        "https://api.prospeo.io/search-person",
        json=payload,
        headers=HEADERS
    )
    response.raise_for_status()
    return response.json()

def enrich_person(person_id, linkedin_url):
    """Step 2: Get verified email using person_id or linkedin_url"""
    payload = {
        "only_verified_email": True,
        "data": {
            "person_id": person_id
        }
    }
    if not person_id and linkedin_url:
        payload["data"] = {"linkedin_url": linkedin_url}

    response = requests.post(
        "https://api.prospeo.io/enrich-person",
        json=payload,
        headers=HEADERS
    )
    response.raise_for_status()
    return response.json()

def find_decision_makers(domains):
    print(f"\n[Stage 2] Finding decision makers + emails for {len(domains)} companies...")

    all_contacts = []

    for domain in domains:
        print(f"\n  Searching: {domain}")

        try:
            # Step 1: Search for people
            search_data = search_people(domain)

            if search_data.get("error"):
                print(f"    ⚠ Search error: {search_data.get('error_code')}")
                time.sleep(4)
                continue

            results = search_data.get("results", [])[:3]

            if not results:
                print(f"    ℹ No contacts found")
                time.sleep(4)
                continue

            for item in results:
                person = item.get("person", {})
                name = f"{person.get('first_name','')} {person.get('last_name','')}".strip()
                person_id = person.get("person_id", "")
                linkedin_url = person.get("linkedin_url", "")

                # Get job title from job history
                job_history = person.get("job_history", [])
                title = "Executive"
                for job in job_history:
                    if job.get("current"):
                        title = job.get("title", "Executive")
                        break

                print(f"    → Enriching {name}...")
                time.sleep(3)  # wait 3 seconds between enrich calls

                try:
                    enrich_data = enrich_person(person_id, linkedin_url)

                    if enrich_data.get("error"):
                        print(f"      ⚠ No email found")
                        continue

                    email_obj = enrich_data.get("person", {}).get("email", {})
                    email = email_obj.get("email", "")

                    if email:
                        contact = {
                            "name": name,
                            "title": title,
                            "domain": domain,
                            "linkedin_url": linkedin_url,
                            "email": email
                        }
                        all_contacts.append(contact)
                        print(f"      ✅ {name} — {title} — {email}")
                    else:
                        print(f"      ⚠ Email not revealed")

                except requests.exceptions.HTTPError as e:
                    print(f"      ✗ Enrich error: {e}")
                    time.sleep(5)  # wait longer after error

            time.sleep(4)  # wait between companies

        except requests.exceptions.HTTPError as e:
            print(f"    ✗ HTTP Error: {e}")
            time.sleep(5)
        except Exception as e:
            print(f"    ✗ Error: {e}")

    print(f"\n[Stage 2] ✅ Found {len(all_contacts)} contacts with verified emails")
    return all_contacts


if __name__ == "__main__":
    test_domains = ["razorpay.com", "cashfree.com", "adyen.com"]
    contacts = find_decision_makers(test_domains)
    for c in contacts:
        print(c)
