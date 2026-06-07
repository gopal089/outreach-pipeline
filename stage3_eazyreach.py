def find_emails(contacts):
    print(f"\n[Stage 3] Email enrichment — using Prospeo data directly")
    
    enriched = [c for c in contacts if c.get("email")]
    skipped = len(contacts) - len(enriched)

    if skipped:
        print(f"  ⚠ Skipped {skipped} contacts with no email")

    print(f"[Stage 3] ✅ {len(enriched)} contacts ready with verified emails")
    return enriched
