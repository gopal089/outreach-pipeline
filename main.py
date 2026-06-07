import sys
from stage1_ocean import find_lookalike_companies
from stage2_prospeo import find_decision_makers
from stage3_eazyreach import find_emails
from stage4_brevo import send_outreach_emails

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

    # Stage 2 — Find decision makers
    contacts = find_decision_makers(domains)
    if not contacts:
        print("\n❌ Stage 2 failed — no contacts found. Exiting.")
        return

    # Stage 3 — Find verified emails
    enriched_contacts = find_emails(contacts)
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
