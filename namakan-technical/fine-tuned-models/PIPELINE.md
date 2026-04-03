# Namakan Fine-Tuning Pipeline Guide

**Complete, Secure, and Efficient Process for Custom AI Training**

---

## Overview

This document describes the complete fine-tuning pipeline from data extraction to model delivery. Each client gets:
- **Isolated Colab instance** — No data mixing between clients
- **Automated workflow** — n8n handles data processing
- **Secure pipeline** — PII removal, encrypted storage
- **Reliable delivery** — Webhook notifications, retry logic

---

## Pipeline Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│  CLIENT DATA SOURCES                                                   │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐                  │
│  │Salesforce│  │PostgreSQL│  │HubSpot  │  │Google   │                  │
│  │         │  │         │  │         │  │Drive    │                  │
│  └────┬────┘  └────┬────┘  └────┬────┘  └────┬────┘                  │
└───────┼────────────┼────────────┼────────────┼────────────────────────┘
        │            │            │            │
        └────────────┴─────┬──────┴────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  n8n AUTOMATION (heater.local:5678)                                   │
│                                                                         │
│  1. Pull data from all sources                                         │
│  2. Combine and deduplicate                                            │
│  3. Remove PII (names, emails, phones, addresses)                      │
│  4. Validate PII removal                                                │
│  5. Format to Q&A training pairs                                       │
│  6. Upload to Google Drive (isolated folder)                            │
│  7. Trigger Colab via email                                             │
│  8. Wait for completion (webhook)                                       │
│  9. Notify via Telegram                                                │
│  10. Log to database                                                    │
└─────────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  GOOGLE COLAB (Dedicated Per-Client Instance)                         │
│                                                                         │
│  1. Download training data from Drive                                   │
│  2. Final PII validation                                                │
│  3. Load Qwen2.5-8B with QLoRA (4-bit)                                 │
│  4. Fine-tune on client data                                           │
│  5. Merge LoRA weights                                                 │
│  6. Upload model to Drive                                              │
│  7. Send webhook notification                                           │
│                                                                         │
│  ⚠️ SECURITY: Each client = New Colab instance = Isolated            │
└─────────────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────────────┐
│  MODEL DELIVERY                                                        │
│                                                                         │
│  Option A: Client downloads from Drive                                  │
│  Option B: Deploy to Lambda/RunPod hosting                             │
│  Option C: Namakan hosts on API                                         │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## Security Model

### Data Isolation

| Layer | Security Measure |
|-------|------------------|
| **Colab** | Dedicated instance per client, runtime deleted after training |
| **Training Data** | Stored in isolated Google Drive folder per client |
| **Credentials** | Stored in n8n credential manager, never in code |
| **PII** | Removed before training, validated twice |
| **Model** | Only model weights delivered, no raw data |

### PII Removal

**Removed patterns:**
- Full names (First Last)
- Email addresses
- Phone numbers (all formats)
- Social Security Numbers
- Credit card numbers
- Street addresses
- Order/Invoice numbers

**Validation:**
1. n8n node removes PII using regex
2. Colab notebook does final check
3. Any remaining PII is flagged

### Colab Instance Isolation

**Per-client workflow:**
1. Namakan creates new Colab notebook (copy of template)
2. Notebook configured with client's File IDs
3. Client-specific variables set (CLIENT_NAME, CLIENT_SLUG)
4. Notebook shared via email or Drive link
5. Training runs on fresh runtime
6. Runtime deleted after completion

**Benefits:**
- No data persists between clients
- No risk of model contamination
- Audit trail per client

---

## Setup Requirements

### 1. Google Cloud Setup

```bash
# Create service account for Drive API
gcloud iam service-accounts create namakan-pipeline \
  --display-name="Namakan Pipeline"

# Grant Drive API access
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="serviceAccount:namakan-pipeline@PROJECT_ID.iam.gserviceaccount.com" \
  --role="roles/drive.fileEditor"

# Download key JSON
gcloud iam service-accounts keys create namakan-key.json \
  --iam-account=namakan-pipeline@PROJECT_ID.iam.gserviceaccount.com
```

### 2. n8n Setup

```bash
# Install n8n (if not already)
npm install -g n8n

# Start n8n
n8n start

# Or run with Docker
docker run -d --name n8n \
  -p 5678:5678 \
  -v n8n_data:/home/node/.n8n \
  n8nio/n8n
```

### 3. n8n Credentials

Create these credentials in n8n:

| Credential | Purpose |
|------------|---------|
| **Salesforce API** | Connect to client Salesforce |
| **PostgreSQL** | Client database + training logs |
| **Google Drive** | Training data + model storage |
| **Gmail** | Send Colab notifications |
| **Telegram Bot** | Status notifications |

### 4. Colab Template

1. Upload `colab-notebook.ipynb` to Google Drive
2. Share folder with namakan-colab@gmail.com
3. Note the folder ID

### 5. Environment Variables

```bash
# n8n environment
export N8N_BASIC_AUTH_ACTIVE=true
export N8N_BASIC_AUTH_USER=admin
export N8N_BASIC_AUTH_PASSWORD=YOUR_PASSWORD
export WEBHOOK_URL=https://your-domain.com/webhook

# Google credentials
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/credentials.json
```

---

## Running the Pipeline

### Manual Trigger (n8n)

1. Open n8n: http://heater.local:5678
2. Open "Namakan Fine-Tuning Pipeline"
3. Click "Test Workflow" on Manual Trigger
4. Enter client configuration:

```json
{
  "clientName": "Acme Corp",
  "clientSlug": "acme",
  "trainingDataFileId": "1XKmj83k...",
  "modelOutputFolderId": "1XKmj83k...",
  "version": "1",
  "webhookUrl": "https://your-domain.com/webhook/namakan-training"
}
```

### Automated Trigger (Webhook)

```bash
# Trigger via webhook
curl -X POST https://your-domain.com/webhook/namakan-training \
  -H "Content-Type: application/json" \
  -d '{
    "clientName": "Acme Corp",
    "clientSlug": "acme",
    "trainingDataFileId": "1XKmj83k...",
    "modelOutputFolderId": "1XKmj83k...",
    "version": "1",
    "webhookUrl": "https://your-domain.com/webhook/callback"
  }'
```

---

## Monitoring & Notifications

### Telegram Notifications

**Training started:**
```
🔄 Training Started

Client: Acme Corp
Version: v1
Records: 3,247
Started: 10:30 AM
```

**Training complete:**
```
✅ Training Complete!

Client: Acme Corp
Model: acme-v1
Records: 3,247
Time: 47 minutes
Loss: 0.82

📁 Model: https://drive.google.com/...
```

**Training failed:**
```
❌ Training Failed

Client: Acme Corp
Error: OOM - Out of memory
Time: 12 minutes

Check Colab logs.
```

---

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| **OOM in Colab** | Batch size too high | Reduce to 2 or 1 |
| **PII detected** | Regex missed something | Add pattern, re-run |
| **Webhook timeout** | Colab takes >90 min | Increase wait time |
| **Drive upload failed** | Permission error | Check service account |
| **No data pulled** | API credentials expired | Refresh credentials |

### Debug Mode

```javascript
// Add to n8n code nodes for debugging
console.log('Records:', records.length);
console.log('Sample:', JSON.stringify(records[0], null, 2));
return records; // Continue with data
```

### Manual Recovery

If Colab fails:

1. Check Colab email for error
2. Fix notebook or data issue
3. Trigger manual run from n8n
4. Or re-upload data and restart

---

## Performance Metrics

### Typical Timings

| Step | Duration |
|------|----------|
| Data extraction (Salesforce) | 2-5 min |
| Data extraction (PostgreSQL) | 1-3 min |
| PII cleaning | <1 min |
| Q&A formatting | <1 min |
| Drive upload | 2-5 min |
| Colab training | 30-60 min |
| Model upload | 5-15 min |
| **Total** | **45-90 min** |

### GPU Requirements

| Model Size | GPU | Memory | Training Time |
|------------|-----|--------|---------------|
| Qwen2.5-3B | T4 | 8GB | 20-30 min |
| Qwen2.5-8B | T4 | 16GB | 45-60 min |
| Qwen2.5-8B | A10G | 24GB | 25-35 min |
| Qwen2.5-14B | A100 | 80GB | 30-40 min |

---

## Cost Analysis

### Per-Client Training Cost

| Resource | Cost |
|----------|------|
| Colab Pro | $0 (with Pro) or $10 |
| Google Drive | $0 (15GB free) |
| n8n (self-hosted) | $0 |
| Namakan time | ~2 hours |
| **Total** | **~$0-10 + time** |

### Hosting Cost (Post-Training)

| Provider | GPU | $/month | Tokens/sec |
|----------|-----|---------|------------|
| Lambda Labs | T4 | $25-50 | 20-30 |
| RunPod | T4 | $20-30 | 20-30 |
| Modal | A10G | $30-50 | 40-60 |

---

## File Structure

```
namakan-technical/fine-tuned-models/
├── workflow.md              # This guide
├── technical.md            # Technical deep-dive
├── deployment.md            # Model deployment guide
├── client-workflow-example.md  # Acme Corp example
├── n8n-workflow.json       # Import into n8n
├── n8n-workflow-production.json  # Production version
├── colab-notebook.ipynb    # Colab training notebook
└── PIPELINE.md            # This file
```

---

## Checklist: New Client Setup

```
□ Discovery call completed
□ Contract signed (50% paid)
□ Create Google Drive folders:
  □ /Namakan/{Client}/training-data/
  □ /Namakan/{Client}/models/
□ Upload colab-notebook.ipynb to training folder
□ Share folders with namakan-colab@gmail.com
□ Set up credentials in n8n:
  □ Salesforce
  □ PostgreSQL
  □ Google Drive
  □ Gmail
  □ Telegram
□ Test credentials (pull sample data)
□ Document folder IDs and credential IDs
□ Schedule training call
□ Run pipeline
□ Deliver model
□ Send setup guide for Ollama/hosting
□ Schedule quarterly retraining
```

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0 | Apr 2026 | Initial release |
