# Sales Prospect Pipeline

Track and manage cold outreach for Namakan's 4 service offerings.

## Quick Start

```bash
cd namakan-sales

# List all prospects
python3 send_sequence.py list

# Create a new prospect
python3 send_sequence.py create \
  --company "Acme Corp" \
  --contact "John Smith" \
  --email "john@acmecorp.com" \
  --industry "Manufacturing" \
  --opportunity "RAG pipeline on service manuals" \
  --data "15 years of field service records"

# Generate next email in sequence
python3 send_sequence.py generate polaris

# Advance sequence (mark email as sent)
python3 send_sequence.py advance polaris

# Mark as replied (stops sequence)
python3 send_sequence.py replied polaris

# Mark as converted (signed contract!)
python3 send_sequence.py converted polaris

# Close without converting
python3 send_sequence.py close polaris --reason "not interested"
```

## The 5-Email Sequence

| # | Name | Day | Goal |
|---|------|-----|------|
| 1 | Intro | 0 | Start conversation with specificity |
| 2 | Value Demo | 7 | Demonstrate capability without selling |
| 3 | Domain Specific | 14 | Name specific opportunities (requires research) |
| 4 | Resource | 21 | Provide value, keep door open |
| 5 | Respectful Close | 28 | Close file gracefully, leave door open |

## Adding a New Prospect

1. Research the company — find decision-maker name, email, LinkedIn
2. Identify their proprietary data assets
3. Identify 2-3 specific AI opportunities
4. Create the prospect:
   ```bash
   python3 send_sequence.py create --company "Company Name" --contact "Name" --email "email"
   ```
5. Edit the JSON file in `prospects/` to add details
6. Generate email 1 and send manually (Gmail, Brevo, etc.)

## Current Prospects

See `send_sequence.py list` for active prospects.

## Sending Emails

This tool generates emails but does NOT send them. Use:
- **Brevo** (free to 500 contacts) — upload contacts, paste email body
- **Gmail + Mailtrack** — direct send with tracking
- **Apollo.io** — email finding + sending in one

## Before Every Email

- [ ] Confirm decision-maker name + correct email
- [ ] Read 2+ recent articles/posts from the company
- [ ] Find one specific thing they are working on
- [ ] Identify their proprietary data assets
- [ ] Personalize the subject line to THEM
- [ ] No typos. Every sentence feels written for THEM.

## Success Metrics

Track in a spreadsheet:
- Emails sent
- Open rate (use tracking)
- Reply rate (target: 10-20%)
- Meetings booked
- Proposals sent
- Contracts signed
- Revenue closed

Typical B2B enterprise conversion funnel:
100 cold emails → 10 replies → 3 calls → 1 proposal → 0.3 contracts
