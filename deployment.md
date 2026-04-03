# Model Deployment Guide

**How to Host or Deliver Trained Models to Clients**

---

## Overview

After Colab training completes, you have two options:
1. **Deliver the model** — Client downloads and hosts themselves
2. **Host for them** — Deploy to cloud and charge monthly hosting

This guide covers both approaches.

---

## Option A: Deliver Model to Client

### What They Receive

```
Client receives:
├── acme-support-v1/           # Model folder
│   ├── config.json            # Model config
│   ├── model.safetensors      # Model weights
│   ├── tokenizer.json         # Tokenizer
│   ├── tokenizer_config.json  # Tokenizer config
│   └── (other model files)
├── Modelfile                   # Ollama config
└── instructions.md             # Setup guide
```

### Delivery Methods

| Method | Best For | How |
|--------|----------|-----|
| Google Drive | Most clients | Upload, share link, they download |
| WeTransfer | Large files (>1GB) | Free up to 5GB, no account needed |
| AWS S3 | Enterprise | Presigned URL, secure |
| Direct transfer | Fast, secure | SFTP/FTP to client server |

### Client Setup Guide

```markdown
# Acme Corp - Model Setup Guide

## Prerequisites
- Ollama installed (ollama.com/download)
- 8GB RAM minimum (16GB recommended)
- Internet connection

## Step 1: Download Model
1. Click link: [Google Drive Link]
2. Download `acme-support-v1.tar.gz` (~2.1 GB)
3. Extract to: `~/models/acme-support-v1/`

## Step 2: Install Ollama
```bash
# macOS/Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Download from ollama.com/download
```

## Step 3: Create Modelfile
Create a file named `Modelfile` in `~/models/acme-support-v1/`:

```dockerfile
FROM ./acme-support-v1
TEMPLATE """
<|im_start|>user
{{ .Prompt }}<|im_end|>
<|im_start|>assistant
"""
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER top_k 40
SYSTEM "You are an AI support agent for Acme Corporation. 
You help classify customer tickets and draft professional responses.
Always follow Acme's escalation policies: L1 can be auto-handled, 
L2+ requires human review."
```

## Step 4: Import Model
```bash
cd ~/models/acme-support-v1
ollama create acme-support-v1 -f Modelfile
```

## Step 5: Test
```bash
ollama run acme-support-v1

# Type a test query:
# "Customer says valve is leaking after 2 weeks"
# Press Ctrl+D to exit
```

## Step 6: API Server (Optional)
```bash
# Start API server
ollama serve

# In another terminal, test:
curl http://localhost:11434/api/generate -d '{
  "model": "acme-support-v1",
  "prompt": "Customer reports leaking valve",
  "stream": false
}'
```

## Troubleshooting

### Out of Memory
- Close other applications
- Add swap: `sudo swapon -s`
- Reduce batch size if using programmatically

### Slow responses
- GPU recommended for faster inference
- CPU inference is ~10x slower

### Model not loading
- Verify all files extracted correctly
- Check path has no spaces
- Try: `ollama list` to see available models

## Support
Questions? Email: clint@namakanai.com
```

---

## Option B: Host on Azure

### Why Azure?

- **Enterprise trust** — Clients feel secure with Microsoft
- **GPU VMs** — NC-series (T4, A100)
- **Compliance** — HIPAA, SOC 2 available
- **Managed** — Less maintenance than raw VMs

### Azure VM Options

| VM Size | GPU | vRAM | $/hour | $/month |
|---------|-----|------|--------|--------|
| Standard_NC4as_T4 | T4 | 16GB | $0.22 | ~$160 |
| Standard_NC6s_v3 | V100 | 16GB | $0.90 | ~$650 |
| Standard_NC24ads_A100 | A100 | 80GB | $2.07 | ~$1,500 |

**Recommendation:** Start with T4 ($160/mo), upgrade as needed.

### Step 1: Create Azure VM

```bash
# Using Azure CLI
az login
az account set --subscription "Your Subscription"

# Create resource group
az group create --name namakan-hosts --location eastus

# Create VM (Ubuntu, T4 GPU)
az vm create \
  --resource-group namakan-hosts \
  --name namakan-gpu-1 \
  --image Canonical:0001-com-ubuntu-server-22_04-lts-gen2:latest \
  --size Standard_NC4as_T4 \
  --admin-username namakan \
  --ssh-key-value ~/.ssh/id_rsa.pub \
  --output json
```

### Step 2: Install Dependencies

```bash
# SSH into VM
ssh namakan@<vm-ip-address>

# Update and install
sudo apt-get update && sudo apt-get upgrade -y

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Install CUDA (for GPU support)
wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2204/x86_64/cuda-keyring_1.0-1_all.deb
sudo dpkg -i cuda-keyring_1.0-1_all.deb
sudo apt-get update
sudo apt-get install cuda
```

### Step 3: Deploy Model

```bash
# Create model directory
sudo mkdir -p /opt/models
sudo chown namakan:namakan /opt/models

# Download model from Drive (on your machine)
# Upload to Azure VM
scp -r acme-support-v1 namakan@<vm-ip>:/opt/models/

# Or: Download directly on VM
cd /opt/models
wget "https://drive.google.com/uc?id=FILE_ID&export=download" -O acme-support-v1.tar.gz
tar -xzf acme-support-v1.tar.gz
```

### Step 4: Configure Ollama

```bash
# Create systemd service for auto-start
sudo nano /etc/systemd/system/ollama.service
```

```ini
[Unit]
Description=Ollama Service
After=network.target

[Service]
Type=simple
User=namakan
WorkingDirectory=/opt/models
ExecStart=/usr/local/bin/ollama serve --host 0.0.0.0 --port 11434
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
# Enable and start
sudo systemctl enable ollama
sudo systemctl start ollama

# Check status
sudo systemctl status ollama
```

### Step 5: Set Up API Server (Optional)

```bash
# Install FastAPI
pip install fastapi uvicorn requests

# Create API server
nano /opt/models/api_server.py
```

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pydantic_settings import BaseSettings
import ollama
import os

app = FastAPI(title="Namakan AI API")

class GenerateRequest(BaseModel):
    model: str
    prompt: str
    system: str = ""
    temperature: float = 0.7
    max_tokens: int = 512

class GenerateResponse(BaseModel):
    model: str
    response: str
    tokens: int
    duration_ms: int

@app.post("/generate/{client_id}", response_model=GenerateResponse)
async def generate(client_id: str, request: GenerateRequest):
    try:
        # Map client to model
        model_map = {
            "acme": "acme-support-v1",
            "client-b": "client-b-v1",
        }
        
        model_name = model_map.get(client_id)
        if not model_name:
            raise HTTPException(404, "Client not found")
        
        # Build prompt
        full_prompt = request.prompt
        if request.system:
            full_prompt = f"{request.system}\n\n{request.prompt}"
        
        # Generate
        start = time.time()
        response = ollama.generate(
            model=model_name,
            prompt=full_prompt,
            options={
                "temperature": request.temperature,
                "num_predict": request.max_tokens,
            }
        )
        duration = int((time.time() - start) * 1000)
        
        return GenerateResponse(
            model=client_id,
            response=response['response'],
            tokens=response.get('eval_count', 0),
            duration_ms=duration
        )
        
    except Exception as e:
        raise HTTPException(500, str(e))

@app.get("/health")
async def health():
    return {"status": "ok", "models": list(model_map.keys())}

@app.get("/models/{client_id}")
async def list_models(client_id: str):
    """List available models for client"""
    return {"models": [model_map.get(client_id, "not found")]}

if __name__ == "__main__":
    import uvicorn, time
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

```bash
# Create systemd service for API
sudo nano /etc/systemd/system/namakan-api.service
```

```ini
[Unit]
Description=Namakan API Service
After=network.target ollama.service
Requires=ollama.service

[Service]
Type=simple
User=namakan
WorkingDirectory=/opt/models
ExecStart=/usr/bin/python3 /opt/models/api_server.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

```bash
sudo systemctl enable namakan-api
sudo systemctl start namakan-api
```

### Step 6: Set Up Domain & SSL

```bash
# Install nginx as reverse proxy
sudo apt-get install nginx

# Configure nginx
sudo nano /etc/nginx/sites-available/namakan-api
```

```nginx
server {
    listen 80;
    server_name api.namakanai.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/namakan-api /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

# Install SSL
sudo apt-get install certbot python3-certbot-nginx
sudo certbot --nginx -d api.namakanai.com
```

### Step 7: Firewall & Security

```bash
# Allow only needed ports
sudo ufw allow 22    # SSH
sudo ufw allow 80    # HTTP
sudo ufw allow 443   # HTTPS
sudo ufw enable

# Set up fail2ban
sudo apt-get install fail2ban
sudo systemctl enable fail2ban
```

### Azure Cost Optimization

```bash
# Set up auto-shutdown (save money after hours)
az vm auto-shutdown \
  --resource-group namakan-hosts \
  --name namakan-gpu-1 \
  --time 1900  # 7PM local time
```

### Monitoring

```bash
# Install Azure Monitor
az vm extension set \
  --resource-group namakan-hosts \
  --vm-name namakan-gpu-1 \
  --name MicrosoftMonitoringAgent \
  --publisher Microsoft.EnterpriseCloud.Monitoring

# Or use simple scripts
crontab -e
# Add:
# */5 * * * * curl -s http://localhost:8000/health >> /var/log/namakan-health.log
```

---

## Option C: Deliver + Set Up for Them

Sometimes clients want you to set it up but don't want ongoing hosting. Here's how to do remote setup.

### Remote Setup Process

```bash
# 1. Client grants you temporary SSH access
# Option A: Password (less secure)
# Option B: SSH key (preferred)

# 2. Client creates namakan user
sudo adduser namakan
sudo usermod -aG sudo namakan

# 3. Client gives you their IP and credentials
ssh namakan@<client-ip>
```

### Client VM Setup Script

```bash
#!/bin/bash
# setup-namakan.sh - Run on client's VM

set -e

echo "Setting up Namakan AI model..."

# Update
apt-get update && apt-get upgrade -y

# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Create directory
mkdir -p /opt/namakan/models
chown namakan:namakan /opt/namakan/models

# Copy model files (client does this manually or you SFTP)
echo "Please copy model files to /opt/namakan/models/"
echo "Then run: ollama create acme-support-v1 -f /opt/namakan/models/Modelfile"

# Create Modelfile
cat > /opt/namakan/models/Modelfile << 'EOF'
FROM ./acme-support-v1
TEMPLATE """
<|im_start|>user
{{ .Prompt }}<|im_end|>
<|im_start|>assistant
"""
PARAMETER temperature 0.7
SYSTEM "You are an AI support agent for Acme Corporation."
EOF

# Create systemd service
cat > /etc/systemd/system/namakan.service << 'EOF'
[Unit]
Description=Namakan AI Service
After=network.target

[Service]
Type=simple
User=namakan
WorkingDirectory=/opt/namakan
ExecStart=/usr/local/bin/ollama serve --host 0.0.0.0
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl enable namakan
systemctl start namakan

echo "Setup complete!"
echo "Test with: curl http://localhost:11434/api/generate -d '{\"model\":\"acme-support-v1\",\"prompt\":\"test\"}'"
```

### Client Handoff Checklist

```
□ VM created (client's Azure/AWS/local)
□ Ollama installed
□ Model files transferred
□ Modelfile configured
□ Service enabled and running
□ Firewall configured
□ Test passed
□ Documentation delivered
□ Credentials rotated (remove your access)
□ Monitoring set up (optional)
```

---

## Integration Examples

### Salesforce Integration

```javascript
// n8n workflow: Salesforce → Model → Salesforce

// 1. New Case created in Salesforce
// 2. Send to model
const response = await fetch('https://api.namakanai.com/generate/acme', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    model: 'acme-support-v1',
    prompt: `Classify and draft response for: ${caseDescription}`,
    system: 'Classify as L1 or L2, draft response'
  })
});

const result = await response.json();

// 3. Update Salesforce with draft
// If L1: Auto-post response
// If L2: Post for human review
```

### API Usage Examples

```python
# Python
import requests

response = requests.post('https://api.namakanai.com/generate/acme', json={
    'model': 'acme-support-v1',
    'prompt': 'Customer says valve is leaking after 2 weeks',
    'temperature': 0.7,
    'max_tokens': 512
})
print(response.json()['response'])
```

```javascript
// JavaScript / Node.js
const response = await fetch('https://api.namakanai.com/generate/acme', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
        model: 'acme-support-v1',
        prompt: 'Customer says valve is leaking after 2 weeks'
    })
});
const data = await response.json();
console.log(data.response);
```

```bash
# cURL
curl -X POST https://api.namakanai.com/generate/acme \
  -H 'Content-Type: application/json' \
  -d '{"prompt": "Customer says valve is leaking", "model": "acme-support-v1"}'
```

---

## Pricing for Hosting

### Azure Hosting ($160/mo starting)

| Component | Cost |
|-----------|------|
| Azure NC4as_T4 (T4 GPU) | $120/mo |
| Managed disks | $20/mo |
| Data transfer | $10/mo |
| SSL certificate | Free |
| Monitoring | Free |
| **Total** | **~$150/mo** |

### Markup Strategy

| Azure Cost | Your Price | Margin |
|------------|------------|--------|
| $150/mo | $200/mo | 33% |
| $150/mo | $250/mo | 67% |

**Recommendation:** Charge $200-250/mo for hosting, undercut enterprise pricing while making margin.

---

## Security Checklist

```
□ SSH key authentication only (no passwords)
□ Firewall allows only 80, 443, 22 (limited IP)
□ SSL certificate on API endpoint
□ API authentication (add API key per client)
□ No model files in public buckets
□ Regular security updates: sudo apt-get update && sudo apt-get upgrade
□ Monitoring for unusual activity
□ Backup strategy (snapshot VM daily)
□ Incident response plan
```

---

## Quick Reference

| Task | Command |
|------|---------|
| Check Ollama status | `systemctl status ollama` |
| View logs | `journalctl -u ollama -f` |
| Test API | `curl http://localhost:11434/api/generate -d '{"model":"acme","prompt":"hi"}'` |
| Restart service | `sudo systemctl restart ollama` |
| Check GPU | `nvidia-smi` |
| Monitor memory | `free -h` |

---

## Support Matrix

| Client Need | Delivery Option | Hosting Option |
|-------------|------------------|----------------|
| Small, technical | ✅ (Drive) | ❌ |
| Mid-size, non-technical | ❌ | ✅ (Azure) |
| Enterprise, compliance | ❌ | ✅ (Azure GovCloud) |
| Want control | ✅ (Ollama) | ❌ |
| Want simplicity | ❌ | ✅ (API) |
