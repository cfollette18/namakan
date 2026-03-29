# Namakan Sales

Cold outreach, prospect tracking, and sales execution for Namakan AI Engineering.

## Files

| File | Purpose |
|------|---------|
| `COLD-EMAIL-SEQUENCE.md` | 5-email outreach sequence with templates |
| `LINKEDIN-OUTREACH.md` | LinkedIn connection and message templates |
| `OBJECTION-HANDLING.md` | Common objections + responses |
| `QUALIFICATION-CHECKLIST.md` | BANT qualification criteria |
| `CALL-SCRIPT.md` | Phone call script for discovery calls |
| `PROPOSAL-TEMPLATE.md` | Proposal template for custom projects |
| `PROSPECTS.md` | Prospect pipeline overview |
| `TARGET-LIST.md` | Ideal customer profile and target verticals |
| `send_sequence.py` | CLI tool for managing prospect sequences |

## Prospect Data

Prospect JSON files stored in `prospects/`:
- `graco.json`, `polaris.json`, `nvent.json` — Manufacturing
- `mayo-clinic.json` — Healthcare
- `faegre-drinker.json` — Legal/Professional Services
- Plus 4 others

## Using send_sequence.py

```bash
cd namakan-sales

# List all prospects
python3 send_sequence.py list

# Generate next email for a prospect
python3 send_sequence.py generate graco

# Advance sequence (mark email sent)
python3 send_sequence.py advance graco

# Mark as replied
python3 send_sequence.py replied graco

# Mark as converted
python3 send_sequence.py converted graco
```

## Email Sequence Cadence

| Email | Day | Goal |
|-------|-----|------|
| 1 — Intro | Day 0 | Start conversation |
| 2 — Value Demo | Day 7 | Demonstrate capability |
| 3 — Domain Specific | Day 14 | Name specific opportunities |
| 4 — Resource Offer | Day 21 | Provide value |
| 5 — Respectful Close | Day 28 | Close file gracefully |
