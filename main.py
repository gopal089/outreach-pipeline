import sys
import json
import os
from stage1_ocean import find_lookalike_companies
from stage2_prospeo import find_decision_makers
from stage3_eazyreach import find_emails
from stage4_brevo import send_outreach_emails

CACHE_FILE = "contacts_cache.json"

def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, "r") as f:
            return json.load(f)
    return []

def run_pipeline(seed_domain):
    print("\n" + "="*60)
    print(f"  🚀 OUTREACH PIPELINE STARTING")
    print(f"  Seed domain: {seed_domain}")
    print("="*60)

    # Stage 1 — Find lookalike companies
    domains = find_lookalike_companies(seed_domain)
    if not domains:
        print("\n❌ Stage 1 failed — no domains found. Exiting.")
        return

    # Stage 2 — Find decision makers + emails
    # Check cache first to avoid hitting rate limits
    cached = load_cache()
    if cached:
        print(f"\n[Stage 2] 📋 Loaded {len(cached)} contacts from cache")
        print(f"[Stage 2] ✅ Found {len(cached)} contacts with verified emails")
        contacts = cached
    else:
        contacts = find_decision_makers(domains)
        if not contacts:
            print("\n❌ Stage 2 failed — no contacts found. Exiting.")
            return

    # Stage 3 — Filter contacts with emails
    enriched_contacts = [c for c in contacts if c.get("email")]
    print(f"\n[Stage 3] Email enrichment — using Prospeo data directly")
    print(f"[Stage 3] ✅ {len(enriched_contacts)} contacts ready with verified emails")

    if not enriched_contacts:
        print("\n❌ Stage 3 failed — no emails found. Exiting.")
        return

    # Stage 4 — Send outreach emails
    send_outreach_emails(enriched_contacts)

    print("\n" + "="*60)
    print("  ✅ PIPELINE COMPLETE!")
    print("="*60)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python main.py <seed_domain>")
        print("Example: python main.py stripe.com")
        sys.exit(1)

    seed_domain = sys.argv[1]
    run_pipeline(seed_domain)
