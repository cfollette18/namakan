# n8n Workflow Guide

**Automated Fine-Tuning Pipeline**

---

## Overview

The n8n workflow handles:
1. Data extraction from client sources
2. PII removal and cleaning
3. Q&A formatting
4. Triggering Colab training
5. Monitoring and notifications

---

## Workflow Structure

```
┌─────────────────────────────────────────────────────────────┐
│  TRIGGER                                                     │
│  Manual or Webhook                                           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  DATA EXTRACTION                                             │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐                   │
│  │Salesforce│  │PostgreSQL│  │HubSpot  │  ← Enable as needed│
│  └────┬────┘  └────┬────┘  └────┬────┘                    │
│       └────────────┴────────────┘                           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  DATA CLEANING                                              │
│  1. Combine sources                                        │
│  2. Remove PII (names, emails, phones, addresses)         │
│  3. Validate PII removal                                    │
│  4. Format to Q&A pairs                                    │
│  5. Deduplicate                                             │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  COLAB TRIGGER                                              │
│  1. Upload CSV to Google Drive                              │
│  2. Configure Colab payload                                 │
│  3. Send training request                                   │
│  4. Wait for completion (webhook)                           │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│  NOTIFICATION                                                │
│  ┌───────────┐  ┌───────────┐                              │
│  │Telegram   │  │Database   │                              │
│  │(Success)  │  │(Log run)  │                              │
│  └───────────┘  └───────────┘                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Setup

### 1. Import Workflow

In n8n (http://localhost:5678):
1. Click **Templates**
2. **Import from JSON**
3. Select `n8n-workflow-production.json`

### 2. Configure Credentials

Create these credentials in n8n:

| Credential | Node | Purpose |
|------------|------|---------|
| **Salesforce API** | Salesforce | Pull cases/tickets |
| **PostgreSQL** | PostgreSQL | Pull records + log training |
| **Google Drive** | Google Drive | Upload CSV, save model |
| **Gmail** | Email | Send Colab notifications |
| **Telegram Bot** | Telegram | Status notifications |

### 3. Update Static Values

In the workflow, replace these placeholder IDs:

```javascript
// In "Upload to Google Drive" node:
folderId: "NAMAKAN_TRAINING_FOLDER_ID"  // Your Drive folder

// In "Trigger Colab (Email)" node:
to: "namakan-colab@gmail.com"

// In "Prepare Colab Payload" node:
outputFolderId: "NAMAKAN_MODELS_FOLDER_ID"
```

---

## PII Cleaning Patterns

The workflow removes these PII types:

| Pattern | Replacement |
|---------|------------|
| Full names (First Last) | `[PERSON]` |
| Email addresses | `[EMAIL]` |
| Phone numbers | `[PHONE]` |
| SSN | `[SSN]` |
| Credit cards | `[CARD]` |
| Street addresses | `[ADDRESS]` |
| Order numbers (ORD-XXXXX) | `[ORDER_ID]` |
| Internal references | `[REF]` |

---

## Data Sources

### Salesforce

```sql
SELECT Id, CaseNumber, Subject, Description, Status,
       Category__c, Resolution, EscalationLevel__c,
       CustomerType__c, ProductFamily__c, CreatedDate
FROM Case
WHERE Status = 'Closed'
  AND CreatedDate > 2024-01-01
```

### PostgreSQL

```sql
SELECT order_id, customer_tier, product_line,
       defect_type, root_cause, resolution_code,
       lot_number, created_at
FROM quality_records
WHERE created_at > '2024-01-01'
  AND archived = false
LIMIT 10000
```

### HubSpot (optional)

Pulls tickets with properties:
- Subject
- Content
- Pipeline
- Status
- Created date

---

## Q&A Formatting

Records are automatically categorized:

| Category | Detection Keywords |
|----------|-------------------|
| Quality - Warranty | quality, defect, warranty, leak, broken |
| Billing Inquiry | billing, invoice, payment, charge |
| Shipping - Order | shipping, delivery, order, tracking |
| Returns - Refunds | return, refund, exchange |
| General Inquiry | (default) |

Each Q&A pair includes:
- Instruction (customer issue)
- Input (empty for text generation)
- Output (categorized response with protocol)

---

## Triggering

### Manual

1. Open workflow in n8n
2. Click "Test Workflow"
3. Enter client configuration:

```json
{
  "clientName": "Acme Corp",
  "clientSlug": "acme",
  "trainingDataFileId": "1XKmj...",
  "modelOutputFolderId": "1Ykml...",
  "version": "1",
  "webhookUrl": "https://your-domain.com/webhook/callback"
}
```

### Webhook

```bash
curl -X POST https://your-domain.com/webhook/namakan-training \
  -H "Content-Type: application/json" \
  -d '{
    "clientName": "Acme Corp",
    "clientSlug": "acme",
    "trainingDataFileId": "1XKmj...",
    "modelOutputFolderId": "1Ykml...",
    "version": "1",
    "webhookUrl": "https://your-domain.com/webhook/callback"
  }'
```

---

## Notifications

### Telegram (Success)

```
✅ Training Complete!

Client: Acme Corp
Model: acme-v1
Records: 3,247
Time: 47 minutes

📁 Model: [Drive link]
```

### Telegram (Failure)

```
❌ Training Failed

Client: Acme Corp
Error: [error message]

Check Colab logs.
```

---

## Monitoring

### View Training Log

```sql
SELECT * FROM training_runs
ORDER BY created_at DESC
LIMIT 10;
```

### Metrics

| Metric | Description |
|--------|-------------|
| `client_name` | Client identifier |
| `model_name` | Trained model name |
| `status` | complete/failed |
| `training_examples` | Number of records |
| `duration_minutes` | Training time |
| `drive_link` | Model location |

---

## Troubleshooting

### No Data Pulled

1. Check credentials are valid
2. Verify API permissions
3. Test query in Salesforce/DB directly

### PII Not Removed

Add new pattern in "Clean PII" node:

```javascript
{ regex: /\\bNEW_PATTERN\\b/g, replacement: '[REDACTED]' }
```

### Colab Not Triggered

1. Check Gmail credentials
2. Verify email sent
3. Check Colab inbox

### Webhook Timeout

Increase wait time in "Wait for Completion" node:
- Current: 90 minutes
- Maximum: 1440 minutes (24 hours)

---

## Files

- `n8n-workflow-production.json` — Import this into n8n

---

## Next Steps

1. Import workflow into n8n
2. Create all credentials
3. Update folder IDs
4. Test with sample data
5. Configure Telegram channel
6. Set up webhook URL for production
