# Fine-Tuned Models — Technical Package

**Everything needed to run the complete Namakan fine-tuning pipeline**

---

## Quick Start

### 1. Set Up n8n
Import `n8n-workflow-production.json` into n8n at http://localhost:5678

### 2. Configure Credentials
- Salesforce API
- PostgreSQL
- Google Drive OAuth2
- Gmail
- Telegram Bot

### 3. Set Up Colab
Upload `colab-notebook.ipynb` to Google Drive, share with namakan-colab@gmail.com

### 4. Run Pipeline
Trigger manually in n8n or via webhook

---

## Files Included

| File | Purpose |
|------|---------|
| `PIPELINE.md` | Complete pipeline guide with architecture, security, troubleshooting |
| `technical.md` | Deep-dive: QLoRA, PEFT, Colab setup, deployment |
| `deployment.md` | Model delivery and hosting options |
| `client-workflow-example.md` | Acme Corp walkthrough |
| `n8n-workflow-production.json` | Production n8n workflow (import this) |
| `colab-notebook.ipynb` | Colab training notebook (upload this) |
| `README.md` | This file |

---

## Security Features

- **Per-client Colab instances** — No data mixing
- **PII removal before training** — 2-stage validation
- **Encrypted credentials** — n8n credential manager
- **No data retention** — Raw data deleted after training
- **Isolated Drive folders** — Per-client storage

---

## Cost Per Client

| Item | Cost |
|------|------|
| Colab Pro | $0-10 |
| Google Drive | $0 |
| n8n (self-hosted) | $0 |
| Lambda/RunPod hosting | $30-50/mo |
| **Total** | **~$30-60/mo hosting** |

---

## Timeline

| Phase | Duration |
|-------|----------|
| Data extraction | 5-10 min |
| PII cleaning | <1 min |
| Training data prep | 2-5 min |
| Colab training | 30-60 min |
| Model upload | 5-15 min |
| **Total** | **45-90 min** |

---

## Support

Questions? Check:
1. `PIPELINE.md` — Troubleshooting section
2. `technical.md` — Deep-dive documentation
3. Telegram notifications — Real-time status

---

*Last updated: April 2026*
