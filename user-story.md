# Namakan Client Workflow — Acme Corp Example

**From First Contact to Trained Model Delivered**

---

## Overview

This document walks through the complete client journey using Acme Corp (metal fabrication company) as the example. It covers:
- Where clients upload data and connect APIs
- What API connections they typically need
- Step-by-step process from contract to delivery

---

## Client Profile: Acme Corp

| Item | Details |
|------|---------|
| **Business** | Metal fabrication, Minneapolis |
| **Size** | 75 employees |
| **CRM** | Salesforce (customer tickets, contacts) |
| **Database** | PostgreSQL (orders, QC records, lot traces) |
| **Documents** | Google Drive (SOPs, contracts, warranties) |
| **Goal** | AI that handles customer support tickets autonomously |

---

## Phase 1: Discovery & Contract

### Step 1.1: Initial Call (Day 1)

**What happens:**
- Clint talks to Acme's VP Operations
- Maps their data sources
- Identifies training use case

**Questions to ask:**
```
1. What CRM do you use?
   → Salesforce

2. Do you have a database with orders/tickets?
   → PostgreSQL with customer records, order history, QC data

3. Where are your documents (SOPs, policies, contracts)?
   → Google Drive, shared folder

4. How many historical records do you have?
   → ~5,000 closed tickets from last 2 years

5. What's the goal?
   → AI that classifies tickets and drafts first responses

6. Who approves before AI handles tickets?
   → L1 tickets auto-handle, L2+ goes to humans
```

**Output:** Scoping document with:
- Data sources identified
- Training scope defined (5,000 tickets)
- Pricing agreed ($5,000 Professional tier)

### Step 1.2: Contract Sent (Day 2-3)

**Document:** Master Service Agreement + Statement of Work

**SOW includes:**
```
Project: Acme Corp Fine-Tuning
Scope: 5,000 training examples from Salesforce + PostgreSQL
Deliverable: Trained Qwen2.5-8B model (.gguf file)
Timeline: 3 weeks
Investment: $5,000 (50% upfront = $2,500)
```

**Where they sign:**
- DocuSign or PDF emailed
- Acme signs and pays 50% upfront

### Step 1.3: Credentials Shared (Day 3-5)

**Where Acme shares credentials:**

| Data Source | How to Connect | What They Do |
|-------------|----------------|--------------|
| Salesforce | Create integration user | Grant read-only access to Cases, Contacts |
| PostgreSQL | Share connection string | Create read-only DB user |
| Google Drive | Share folder | Grant "View" access to namakan@gmail.com |

**Secure delivery options:**
1. **Google Drive** — Share a folder (easiest for files)
2. **1Password** — Share credentials via secure vault
3. **AWS S3** — Upload CSVs to private bucket (enterprise)
4. **Direct DB** — VPN or IP whitelist for PostgreSQL

**Email from Acme's IT:**
```
To: clint@namakanai.com
Subject: Acme Corp - Namakan Credentials

Salesforce:
- Instance: acme.my.salesforce.com
- Username: namakan-integration@acme.com
- Password: [via 1Password]

PostgreSQL:
- Host: db.acmeinternal.com:5432
- Database: acme_production
- Username: namakan_read
- Password: [via 1Password]

Google Drive:
- Folder shared: "Namakan AI - Training Data"
```

---

## Phase 2: Data Connection

### Step 2.1: n8n Workflow Setup (Day 5-7)

**Where:** Clint sets up in n8n at http://localhost:5678

**Acme's data sources in n8n:**

```
┌─────────────────────────────────────────────────────────────┐
│  n8n Workflow: Acme Corp Data Connection                   │
│                                                             │
│  ┌──────────────┐                                          │
│  │ Salesforce   │──┐                                        │
│  │ (Cases)      │  │                                        │
│  └──────────────┘  │                                        │
│                    │                                        │
│  ┌──────────────┐  │   ┌──────────────┐                    │
│  │ PostgreSQL   │──┼──▶│ Combine &    │                    │
│  │ (Orders/QC)  │  │   │ Deduplicate  │                    │
│  └──────────────┘  │   └──────────────┘                    │
│                    │                                        │
│  ┌──────────────┐  │                                        │
│  │ Google Drive │──┘                                        │
│  │ (Documents)  │                                           │
│  └──────────────┘                                           │
└─────────────────────────────────────────────────────────────┘
```

### Step 2.2: Test Data Pull (Day 7)

**What happens:**
- n8n pulls sample (100 records from each source)
- Clint reviews data quality
- Confirms format matches expectations

**Sample pulled data:**

**From Salesforce (Cases):**
```
{
  "Id": "0038d00000XYZ123",
  "Subject": "Valve leaking in washdown unit",
  "Description": "Customer reports valve leaking after 2 weeks",
  "Status": "Closed",
  "Category": "Quality",
  "Resolution": "Replaced under warranty",
  "EscalationLevel": "L2",
  "CreatedDate": "2026-01-15"
}
```

**From PostgreSQL (Orders):**
```
{
  "order_id": "ORD-2026-44921",
  "customer_tier": "Enterprise",
  "product_line": "Industrial Valves",
  "defect_type": "Leak",
  "root_cause": "Manufacturing defect",
  "resolution_code": "WARRANTY_REPLACEMENT"
}
```

**From Google Drive (SOPs):**
```
Warranty_Policy_v3.pdf
├── Section 4.2: Enterprise Warranty Terms
├── Section 7.1: Washdown Product Warranty (90 days)
└── Section 12.3: Lot Trace Requirements
```

### Step 2.3: Full Data Export (Day 7-8)

**Once sample looks good:**
- n8n pulls full dataset (5,000 tickets)
- Google Drive folder synced
- Data stored temporarily in Google Drive

**Where data sits:**
```
Google Drive: /Namakan/Acme Corp/2026-04-02/
├── raw-data/
│   ├── salesforce-cases-2026-04-02.csv (3,247 records)
│   ├── postgresql-orders-2026-04-02.csv (1,853 records)
│   └── sop-documents/ (12 files)
└── cleaned-data/ (created by n8n cleaning step)
    └── training-pairs-2026-04-02.csv
```

---

## Phase 3: Data Cleaning

### Step 3.1: PII Removal (Day 8)

**Where:** n8n "Clean PII" code node

**What gets removed:**

| PII Type | Example | Replacement |
|----------|---------|-------------|
| Customer names | "John Smith" | "[REDACTED]" |
| Emails | "john@customer.com" | "[REDACTED]" |
| Phone numbers | "612-555-1234" | "[REDACTED]" |
| Addresses | "123 Industrial Blvd" | "[REDACTED]" |
| Order numbers | "ORD-2026-44921" | "[ORDER_ID]" |
| SSNs | "123-45-6789" | "[REDACTED]" |

**Before:**
```
Customer: John Smith (612-555-1234)
Issue: Valve leaking, order ORD-2026-44921
Notes: John called from customer site at 123 Industrial Blvd...
```

**After:**
```
Customer: [REDACTED] ([REDACTED])
Issue: [REDACTED] leaking, order [ORDER_ID]
Notes: [REDACTED] called from [REDACTED]...
```

### Step 3.2: Q&A Pair Formatting (Day 8-9)

**Where:** n8n "Format Training Data" code node

**Format created:**

```csv
instruction,input,output
"A customer reports a product is leaking after 2 weeks of use. Classify and draft a response.","","Category: Quality - Warranty Claim\nEscalation: L2\nResponse: We apologize for the inconvenience. Based on our warranty policy, this appears to be covered. Initiating replacement now. Expect RA# within 24 hours."
"A customer questions a charge on their invoice. Review and respond.","","Category: Billing - Dispute\nEscalation: L1\nResponse: Thank you for reaching out. I'm reviewing your account and will respond within 2 business hours with clarification."
```

**Training pair count:** 3,247 tickets → 3,247 Q&A pairs

### Step 3.3: Review & Approve (Day 9-10)

**Where:** Clint reviews, Acme approves (optional)

**Sample sent to Acme VP:**
```
Subject: Acme Training Data - Sample for Review

Hi [VP Name],

Attached is a sample of 50 training pairs we'll use to train your AI.
Please review and confirm the format looks right.

[Link to Google Sheet: 50 sample pairs]

Key things to check:
1. Does the response tone match your brand?
2. Are the escalation rules correct (L1 vs L2)?
3. Any sensitive info we missed?

Let me know if you want adjustments.

- Clint
```

**Acme approves** → proceed to training

---

## Phase 4: Training

### Step 4.1: Upload to Colab (Day 10)

**Where:** Automated via n8n → Google Drive → Colab

**n8n workflow continues:**
```
Upload to Drive → Trigger Colab → Wait → Download Model
```

**What happens:**
1. n8n uploads cleaned CSV to Google Drive
2. Colab notebook reads from Drive
3. Training runs (~45 min on Colab Pro)
4. Output model uploaded to Drive
5. n8n downloads model
6. Telegram notification sent to Clint

### Step 4.2: Colab Training (Day 10)

**Colab notebook:**
```python
# Namakan Fine-Tuning - Acme Corp
# =================================

# Config
BASE_MODEL = "qwen2.5-8b-instruct"
DATA_FILE = "https://drive.google.com/uc?id=1XKmj83k...acme-training"
OUTPUT_NAME = "acme-support-v1"
LORA_RANK = 16
LORA_ALPHA = 32
EPOCHS = 3

# Training
# ... (45 minutes later) ...

# Output
# Model saved to: /content/acme-support-v1.gguf
```

### Step 4.3: Notification (Day 10)

**Telegram message to Clint:**
```
✅ Training Complete!

Client: Acme Corp
Model: acme-support-v1
Training Records: 3,247
Training Time: 47 minutes
Final Loss: 0.82

📁 Model: acme-support-v1.gguf (2.1 GB)
🔗 Drive: https://drive.google.com/acme-support-v1.gguf
```

---

## Phase 5: Delivery

### Step 5.1: Model Delivery (Day 10-11)

**Option A: Download & Send**
```
1. n8n downloads .gguf from Drive
2. Clint uploads to file sharing (WeTransfer, Drive)
3. Email to Acme: "Your trained model is ready"
4. Acme downloads
```

**Option B: Direct Transfer**
```
1. Upload to Acme's S3 bucket
2. Or: Share via their secure FTP
```

**Email to Acme:**
```
Subject: Acme Corp - Your Trained AI Model

Hi [VP Name],

Your AI model is ready.

📁 File: acme-support-v1.gguf (2.1 GB)
📊 Training Report: [link]

To run it:

1. Download Ollama: ollama.com/download
2. Place .gguf file in ~/models/
3. Run:
   ollama create acme-support-v1 -f Modelfile
   ollama run acme-support-v1

Next steps:
- Test on 10 sample tickets
- Let me know if you'd like me to set up hosting ($200/mo)
- Ready to discuss agentic workflows?

- Clint
```

### Step 5.2: Testing & Validation (Day 11-14)

**Acme tests model:**

| Test | Input | Expected Output |
|------|-------|-----------------|
| 1 | "Valve leaking after 1 week" | Warranty response, L2 |
| 2 | "Invoice seems wrong" | Billing response, L1 |
| 3 | "Need expedited shipping" | Shipping info, L1 |

**Feedback loop:**
- Acme tests 10 tickets
- 8/10 good → approve
- 2/10 need adjustment → retrain on those 2 cases

### Step 5.3: Final Payment (Day 14)

**Acme pays remaining 50%:** $2,500

---

## Phase 6: Expansion (Optional)

### Step 6.1: Hosting (Month 2+)

**Acme doesn't want to run locally**

```
Price: $200/month
Includes:
- API endpoint: api.namakanai.com/acme
- 99.5% uptime
- Usage dashboard
```

**Integration:**
```python
# Acme's system calls our API
response = requests.post("https://api.namakanai.com/acme", json={
  "ticket": "Valve leaking after 1 week",
  "customer_tier": "Enterprise"
})
```

### Step 6.2: Agentic Workflow (Month 3)

**Acme wants AI to handle tickets end-to-end**

```
Price: $5,000-10,000
Scope:
- Auto-classify ticket
- Draft response
- Update Salesforce
- Escalate L2+ to human
```

**n8n workflow:**
```
New Salesforce Ticket
    ↓
Fine-tuned Model (classify + respond)
    ↓
[If L1] → Draft response → Post to Salesforce
[If L2+] → Flag for human review
```

### Step 6.3: Quarterly Retraining (Every 3 months)

**Keep model fresh with new data**

```
Price: $500-1,000/quarter
Process:
- Pull last quarter's tickets from Salesforce
- Clean + format
- Retrain on new data
- Deploy updated model
```

---

## Data Access Summary

### Where Does Data Live?

| Stage | Data Location | Who Has Access |
|-------|---------------|----------------|
| Credentials shared | Acme's systems | Only Acme |
| Data pulled | n8n (localhost) | Clint only |
| Raw data | Google Drive (Namakan folder) | Clint only |
| Cleaned data | Google Drive (Namakan folder) | Clint only |
| Training | Google Colab | Clint only |
| Trained model | Google Drive | Clint + Acme |
| Final model | Acme's infrastructure | Acme only |

### Security Summary

```
Acme's Data Journey:
1. Lives in Acme's Salesforce/PostgreSQL/Drive
2. Read-only access granted to Clint (temporary)
3. Pulled via n8n to localhost
4. Stored in Clint's Google Drive (private)
5. Sent to Colab for training (processed, not stored long-term)
6. Only model weights (not raw data) returned
7. Raw data deleted after training complete
```

---

## API Connections Clients Typically Need

### CRM Systems

| CRM | Common Use Case | Connection Type |
|-----|-----------------|-----------------|
| Salesforce | Cases, contacts, opportunities | API + Integration User |
| HubSpot | Tickets, contacts, deals | OAuth or API Key |
| Zoho | Cases, contacts | API |
| Freshdesk | Tickets, customers | REST API |
| Zendesk | Tickets, users | REST API |

### Databases

| Database | Common Use Case | Connection Type |
|----------|-----------------|-----------------|
| PostgreSQL | Orders, inventory, QC records | Direct connection + read-only user |
| MySQL | Orders, customers | Direct connection |
| SQL Server | Legacy data | ODBC or direct |
| MongoDB | Logs, unstructured data | Connection string |

### Document Storage

| Service | Common Use Case | Connection Type |
|---------|-----------------|-----------------|
| Google Drive | SOPs, policies, contracts | OAuth (share folder) |
| SharePoint | Company documents | OAuth |
| Dropbox | Files, backups | OAuth |
| S3 | Large files, exports | IAM credentials |
| Box | Enterprise documents | OAuth |

### Other Integrations

| Service | Common Use Case | Connection Type |
|---------|-----------------|-----------------|
| Slack | Notifications, alerts | Bot token |
| Gmail | Email history, templates | OAuth |
| QuickBooks | Invoices, payments | OAuth |
| Stripe | Payment history | API key |

---

## Quick Start Checklist

### For New Client Onboarding

```
□ Discovery call completed
□ Contract signed (50% paid)
□ Credentials received
□ n8n workflow created
□ Sample data pulled and reviewed
□ Full data export completed
□ PII cleaning verified
□ Training data approved (client sign-off)
□ Colab training triggered
□ Model downloaded
□ Model tested by client
□ Final payment received
□ Hosting offered (optional)
□ Agentic workflow proposed (optional)
```

---

## Timeline Summary

| Day | Activity |
|-----|----------|
| 1 | Discovery call |
| 2-3 | Contract sent and signed |
| 5-7 | Credentials shared, n8n setup |
| 7-8 | Full data export |
| 8-9 | Data cleaning and formatting |
| 9-10 | Client review and approval |
| 10 | Colab training (~45 min) |
| 11-14 | Model testing and validation |
| 14 | Final payment |

**Total: ~2 weeks from contract to delivery**
