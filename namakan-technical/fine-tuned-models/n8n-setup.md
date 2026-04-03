# n8n Fine-Tuning Pipeline Setup

## Overview
This n8n workflow:
1. Pulls data from client's CRM (Salesforce example)
2. Removes PII (names, emails, phones, addresses)
3. Formats data into Q&A training pairs
4. Uploads to Google Drive
5. Triggers Colab notebook
6. Waits for completion
7. Notifies you when done

## Import Workflow

1. Open n8n: http://heater.local:5678
2. Click "Templates" → "Import from JSON"
3. Paste contents of `n8n-workflow.json`
4. Click "Save"

## Required Credentials

### n8n nodes that need auth:
- **Salesforce** — Your client's Salesforce instance
- **Google Drive** — Your Google account (or client's)
- **Telegram** — Bot for notifications (chat_id: 7982591864)

### Setup:
1. **Salesforce**: Settings → Credentials → Add Salesforce API credential
2. **Google Drive**: Settings → Credentials → Add Google Drive OAuth2
3. **Telegram**: Create bot via @BotFather, get token, add to n8n

## Customize for Each Client

### 1. Change Data Source
Replace "Salesforce Connection" with:
- **HubSpot**: Use HubSpot node
- **PostgreSQL**: Use Database node
- **Files**: Use "Read Binary File" node
- **HTTP/API**: Use HTTP Request node

### 2. Update PII Patterns
Edit "Clean PII" code node to add/remove patterns:

```javascript
const piiPatterns = [
  /\b[A-Za-z]+ [A-Za-z]+\b/g,           // Names
  /\b\d{3}-\d{2}-\d{4}\b/g,             // SSN
  /email pattern here/,                   // Emails
  /phone pattern/,                        // Phones
  /address pattern/                       // Addresses
];
```

### 3. Customize Q&A Format
Edit "Format to Q&A Pairs" to match their data structure:

```javascript
// Example for manufacturing tickets:
return {
  instruction: `Handle: ${r.TicketSubject}`,
  input: '',
  output: `Category: ${r.ProductLine}\nResolution: ${r.Fix}\nEscalate: ${r.NeedsReview}`
};
```

### 4. Set Colab Notebook
1. Create Colab notebook that:
   - Accepts Google Drive file ID
   - Trains model
   - Outputs model to shared Drive folder
   - Sends webhook when done

Example Colab trigger:
```python
# In your Colab notebook:
import requests

data_file = "YOUR_GOOGLE_DRIVE_FILE_ID"
base_model = "qwen2.5-8b"
output_name = "client-model"

# After training completes:
requests.post("YOUR_N8N_WEBHOOK_URL", json={
  "status": "complete",
  "modelUrl": "https://drive.google.com/..."
})
```

## Workflow Steps Explained

```
Manual Trigger
     ↓
Salesforce (pull closed cases)
     ↓
Clean PII (remove names, emails, SSNs, phones, addresses)
     ↓
Format to Q&A (convert to training format)
     ↓
Convert to CSV
     ↓
Upload to Google Drive
     ↓
Trigger Colab (start training)
     ↓
Wait 30 min (or use webhook callback)
     ↓
Download model
     ↓
Notify (Telegram)
```

## Testing

1. Click "Test Workflow" on manual trigger
2. Watch each step in the editor
3. Check Telegram for completion notification
4. Verify output in Google Drive

## Troubleshooting

### Salesforce query returns no results
- Check credentials are valid
- Verify object/field names match their schema
- Try `returnAll: true` to debug

### PII cleaning too aggressive
- Reduce patterns in code node
- Test on small sample first

### Colab not triggering
- Verify notebook URL is public/shareable
- Check webhook URL is accessible from Colab
- Test webhook separately with curl

### Model download fails
- Check if Colab output path is correct
- Verify Google Drive permissions

## Cost Estimate

- **n8n**: Free (self-hosted on heater.local)
- **Colab**: Free (Pro optional for faster GPU)
- **Google Drive**: Free tier (15GB)
- **Salesforce API**: Client's existing license

Total: ~$0 to $10/month
