# Example: Acme Corp Fine-Tuning Workflow

## Company Profile
- **Name:** Acme Corporation (metal fabrication, Minneapolis)
- **Size:** 50-100 employees
- **Data sources:** Salesforce (CRM), internal PostgreSQL (orders/QC), Google Drive (contracts/SOPs)
- **Goal:** Train AI to handle customer support tickets autonomously

---

## Step 1: Acme Sets Up Data Access

### What Acme does:
1. **Salesforce:** Grant read access to a dedicated "Namakan" integration user
   - Read-only access to Cases, Contacts, Products
   - No write access needed

2. **PostgreSQL:** Create read-only database user
   ```sql
   CREATE USER namakan_read WITH PASSWORD '...';
   GRANT SELECT ON ALL TABLES IN SCHEMA public TO namakan_read;
   ```

3. **Google Drive:** Share "Acme Training Data" folder with our Google account
   - Contains: SOPs, contract templates, return policies, escalation rules

4. **Export historical tickets:** (if not in Salesforce)
   - Export last 2 years of support tickets as CSV
   - Upload to shared Google Drive folder

### Namakan receives:
- [ ] Salesforce credentials (test instance)
- [ ] PostgreSQL connection string
- [ ] Google Drive folder access
- [ ] Sample of 100 historical tickets (for initial training)

---

## Step 2: n8n Workflow Runs

### Data Pull (15 min)

```
Salesforce Query:
─────────────────
SELECT 
  Id, Subject, Description, Status, 
  Resolution, Category, ProductFamily,
  EscalationLevel, CustomerType, CreatedDate
FROM Case
WHERE Status = 'Closed'
  AND CreatedDate > 2024-01-01
LIMIT 5000
```

```
PostgreSQL Query:
─────────────────
SELECT 
  order_id, customer_name, product_line,
  defect_type, root_cause, resolution_code,
  days_to_resolve, return_auth_number
FROM quality_records
WHERE created_at > '2024-01-01'
LIMIT 2000
```

### Combined Data Sample:
```
Case #10234 | "Valve leaking in washdown unit"
Status: Closed | Category: Quality | Product: Industrial Valve
Resolution: Replaced under warranty | Escalation: L2 | Customer: Enterprise

Case #10235 | "Incorrect fitting on order #4492"
Status: Closed | Category: Shipping Error | Product: Fittings  
Resolution: Reshipped correct part | Escalation: L1 | Customer: Standard
```

---

## Step 3: PII Cleaning

### Before Cleaning:
```
Customer: John Smith (612-555-1234)
Contact: john.smith@acme-corp.com
Address: 123 Industrial Blvd, Minneapolis, MN 55401
Agent: Sarah Johnson
Notes: "John called about order #44921..."
```

### After Cleaning:
```
Customer: [REDACTED]
Contact: [REDACTED]
Address: [REDACTED]
Agent: [REDACTED]
Notes: "Customer called about order #[REDACTED]..."
```

### Patterns Removed:
- Names (first + last)
- Email addresses
- Phone numbers
- Street addresses
- Order numbers (optional - keep for context)

---

## Step 4: Format to Q&A Training Pairs

### Original Closed Ticket:
```
Subject: Valve leaking in washdown unit
Description: Customer reports valve leaking after 2 weeks of use
Category: Quality
Resolution: Replaced under warranty
Escalation: L2
```

### Formatted Training Pair:
```
{
  "instruction": "A customer reports a valve is leaking after 2 weeks of use in a washdown environment. Classify and respond.",
  "input": "",
  "output": "Category: Quality - Warranty Claim
Product Line: Industrial Valves
Escalation Level: L2 (warranty replacement)
Response Protocol:
  1. Verify purchase date and warranty status (standard: 90-day warranty for washdown units)
  2. Check lot trace for manufacturing date
  3. If under warranty: Issue return auth, arrange replacement
  4. Document in CRM: lot_number, warranty_status, resolution
  5. If out of warranty: Quote repair/replacement options
Response: 'We apologize for the inconvenience. Based on our records, this valve is covered under our washdown warranty. I'm initiating a replacement now and will send you a return authorization. Our team will reach out within 24 hours with tracking.'"
}
```

---

## Step 5: Upload to Google Drive

```
Folder: /Acme Corp / Training Data / 2026-04-02
File: acme-support-training-2026-04-02.csv
Size: 847 records
Format: Q&A pairs (instruction, input, output)
```

---

## Step 6: Trigger Colab Training

### Colab Notebook:
```python
# Namakan Fine-Tuning Pipeline
# Input: Google Drive file ID
# Output: Trained LoRA adapter

BASE_MODEL = "qwen2.5-8b"
DATA_FILE = "1XKmj83kQp8N7GtvAcmeCorp20260402"
OUTPUT_NAME = "acme-corp-support-v1"
LORA_RANK = 16
LORA_ALPHA = 32
EPOCHS = 3

# Training runs for ~45 minutes on Colab Pro
# Outputs: acme-corp-support-v1.gguf (ready to deploy)
```

---

## Step 7: Notification

### Telegram Message to Clint:
```
✅ Training Complete!

Client: Acme Corporation
Model: acme-corp-support-v1
Training Records: 847
Training Time: 47 minutes
Loss: 0.82 (final)

📁 Model File:
drive.google.com/acme-corp-support-v1.gguf

🔗 Ready to deploy!
```

---

## Step 8: Deploy Model to Acme

### Option A: Local (Acme's Server)
```bash
# Acme downloads the .gguf file
# Runs on their internal Ollama server

ollama create acme-support-v1 -f acme-corp-support-v1.gguf
ollama run acme-support-v1
```

### Option B: API (Namakan hosts)
```bash
# Namakan deploys to Acme's API endpoint
# Acme integrates into their support system

POST https://api.acme.com/ai/support
{
  "message": "Customer called about leaking valve",
  "customer_tier": "enterprise"
}
```

---

## What Acme Corp Needs to Do

### Week 1: Setup (1-2 hours)
- [ ] Create read-only Salesforce integration user
- [ ] Create read-only PostgreSQL user
- [ ] Share Google Drive folder with Namakan
- [ ] Export any additional historical data (optional)
- [ ] Sign MSA/NDA

### Week 2: Review & Approve (30 min)
- [ ] Review sample of 50 cleaned training pairs
- [ ] Approve or adjust formatting
- [ ] Define edge cases (what's L1 vs L2, etc.)

### Week 3: Training (no action needed)
- [ ] Namakan runs training
- [ ] Receive Telegram notification when done

### Week 4: Deploy & Test (1 hour)
- [ ] Download model or receive API credentials
- [ ] Test 10 sample tickets
- [ ] Approve or request retraining

### Ongoing: Monitor & Improve (30 min/month)
- [ ] Review AI responses monthly
- [ ] Flag incorrect responses for retraining
- [ ] Quarterly retrain with new data

---

## Cost Breakdown (Acme Corp)

> Pricing reflects Namakan's current SMB tier. See [service-offerings.md](../../namakan-business/service-offerings.md) for full pricing details.

| Item | Cost |
|------|------|
| Initial fine-tuning (SMB tier: 500–2K examples) | $5,000–$15,000 |
| Colab (free or $10/mo Pro) | $0–10 |
| Model deployment (local Ollama, self-hosted) | $0 |
| Monthly API hosting (optional, Namakan cloud) | $200/mo |
| Quarterly retraining | $500–$1,000/quarter |

**Year 1 Total:** ~$5,500–$16,500 + optional hosting

*This example uses 847 records (within SMB tier). Mid-Market ($15K–$25K) and Enterprise ($25K–$40K) pricing available for larger datasets.*

---

## Next Steps for Acme

1. **This call:** Answer questions, sign MSA
2. **Next day:** Send credentials, grant folder access
3. **Week 1–2:** Review sample training data, finalize dataset
4. **Week 3–4:** Fine-tuning training (Colab)
5. **Week 5–6:** Evaluation and testing
6. **Week 6–8:** Live deployment and handoff *(SMB timeline: 4–8 weeks total)*

---

## Ready to Start?

Tell us about your data:
1. What CRM do you use? (Salesforce, HubSpot, other?)
2. Do you have a database with orders/tickets? (PostgreSQL, MySQL, Excel?)
3. Where are your SOPs/contracts stored? (Google Drive, SharePoint, files?)
4. How many historical tickets/records do you have?

We'll build the workflow for you.
