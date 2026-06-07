import os
import requests
from dotenv import load_dotenv

load_dotenv()

BREVO_API_KEY = os.getenv("BREVO_API_KEY")
BREVO_SENDER_EMAIL = os.getenv("BREVO_SENDER_EMAIL")
BREVO_SENDER_NAME = os.getenv("BREVO_SENDER_NAME")

def send_outreach_emails(contacts):
    print(f"\n[Stage 4] Sending outreach emails to {len(contacts)} contacts...")

    if not contacts:
        print("[Stage 4] ⚠ No contacts to email. Exiting.")
        return

    # ── Safety checkpoint ──────────────────────────────────────────
    print("\n" + "="*50)
    print("📋 SAFETY CHECKPOINT — Review before sending")
    print("="*50)
    for c in contacts:
        print(f"  • {c['name']} <{c['email']}> — {c.get('title','Executive')} at {c['domain']}")
    print("="*50)
    confirm = input(f"\nReady to send {len(contacts)} emails? Type 'yes' to confirm: ").strip().lower()
    if confirm != "yes":
        print("[Stage 4] ❌ Cancelled. No emails sent.")
        return
    # ───────────────────────────────────────────────────────────────

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "api-key": BREVO_API_KEY
    }

    sent = 0
    failed = 0

    for contact in contacts:
        name = contact.get("name", "there")
        email = contact.get("email", "")
        domain = contact.get("domain", "your company")
        title = contact.get("title", "Executive")
        first_name = name.split()[0] if name else "there"

        if not email:
            print(f"  ⚠ Skipping {name} — no email")
            failed += 1
            continue

        # Personalised email copy
        subject = f"Quick question for {first_name} — partnerships at {domain}"

        html_content = f"""
        <p>Hi {first_name},</p>

        <p>I came across {domain} and was genuinely impressed by what you're building
        in the payments space.</p>

        <p>I'm reaching out because we help companies like yours automate their
        outreach and lead generation — so your team can focus on closing deals
        instead of finding them.</p>

        <p>Would you be open to a quick 15-minute call this week to explore if
        there's a fit? No pitch, just a conversation.</p>

        <p>Looking forward to hearing from you.</p>

        <p>Best,<br>
        {BREVO_SENDER_NAME}<br>
        </p>
        """

        payload = {
            "sender": {
                "name": BREVO_SENDER_NAME,
                "email": BREVO_SENDER_EMAIL
            },
            "to": [{"email": email, "name": name}],
            "subject": subject,
            "htmlContent": html_content
        }

        try:
            response = requests.post(
                "https://api.brevo.com/v3/smtp/email",
                json=payload,
                headers=headers
            )
            response.raise_for_status()
            print(f"  ✅ Sent to {name} <{email}>")
            sent += 1

        except requests.exceptions.HTTPError as e:
            print(f"  ✗ Failed for {name}: {e}")
            print(f"    Response: {response.text}")
            failed += 1

    print(f"\n[Stage 4] ✅ Done — {sent} sent, {failed} failed")


if __name__ == "__main__":
    # Test with dummy contacts
    test_contacts = [
        {
            "name": "Test User",
            "email": "11249a112@kanchiuniv.ac.in",  # ← put YOUR email here to test
            "title": "CEO",
            "domain": "razorpay.com"
        }
    ]
    send_outreach_emails(test_contacts)
