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

        subject = f"Quick question for {first_name} — partnerships at {domain}"

        html_content = f"""
        <p>Hi {first_name},</p>

        <p>I noticed <strong>{domain}</strong> is doing incredible work in the payments space —
        the scale and speed at which you're growing is hard to miss.</p>

        <p>I'm reaching out because we work with fintech companies at similar
        stages to help them automate their sales outreach — finding the right
        prospects, personalising at scale, and booking more meetings without
        adding headcount.</p>

        <p>Most of our clients see a 3x increase in qualified pipeline within
        the first 60 days.</p>

        <p>Would a 15-minute call this week make sense? I'd love to show you
        exactly how it works — no commitment, just a conversation.</p>

        <p>Best,<br>
        {BREVO_SENDER_NAME}<br>
        <a href="mailto:{BREVO_SENDER_EMAIL}">{BREVO_SENDER_EMAIL}</a>
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
    test_contacts = [
        {
            "name": "Test User",
            "email": "11249a112@kanchiuniv.ac.in",
            "title": "CEO",
            "domain": "razorpay.com"
        }
    ]
    send_outreach_emails(test_contacts)
