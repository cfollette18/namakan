# Secure Data Pipeline

*Namakan AI Engineering — Internal Operations Reference*

---

## Overview

Every client project involves their proprietary data. This pipeline governs how we receive, handle, store, process, and protect client data throughout the engagement.

**Core principle:** Client data is their asset. We are custodians, not owners. It is never used for any purpose other than the contracted work.

---

## Data Classification

| Level | Description | Examples | Handling |
|-------|-------------|---------|---------|
| **Public** | Already publicly available | Marketing docs, published content | Standard precautions |
| **Internal** | Internal-only, non-sensitive | SOPs, internal communications | Secure but not regulated |
| **Confidential** | Sensitive business data | Customer lists, financial data | Encryption required |
| **Restricted** | Highly sensitive, regulated | PII, PHI, financial records, trade secrets | Maximum security, audit trail |

---

## Pipeline Phases

```
Client Data → Intake → Classification → Storage → Processing → Training → Delivery → Destruction
```

---

## Phase 1: Data Intake

### 1.1 Secure Upload Portal
- Clients upload via encrypted SFTP or ShareFile
- No email attachments for data files
- Upload generates automatic receipt + file hash (SHA-256)

### 1.2 Initial Virus/Malware Scan
```bash
# Automatic scan on upload
clamscan --infected --remove=no --no-summary $UPLOAD_DIR
# If infected: quarantine and alert client immediately
```

### 1.3 Data Inventory
```python
def inventory_data(directory):
    """Create manifest of all uploaded files."""
    manifest = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            path = os.path.join(root, file)
            manifest.append({
                "filename": file,
                "path": path,
                "size": os.path.getsize(path),
                "sha256": hash_file(path),
                "mime_type": magic.from_file(path),
                "uploaded_at": datetime.now().isoformat()
            })
    return manifest
```

### 1.4 Client Data Agreement
Before any data is accepted:
- [ ] Signed NDA (mutual, covers the engagement)
- [ ] Data handling acknowledgement signed
- [ ] Scope of data use documented
- [ ] Retention period agreed (default: project duration + 90 days)

---

## Phase 2: Data Classification

### 2.1 Automated Classification
```python
SENSITIVE_PATTERNS = {
    "pii": [
        r"\b\d{3}-\d{2}-\d{4}\b",      # SSN
        r"\b\d{9}\b",                     # Driver's license
        r"\b[A-Z]{2}\d{6,8}\b",          # Passport
    ],
    "phi": [
        r"\bMRN[:\s]+\d+",                # Medical record number
        r"diagnosis.*", r"patient.*",
    ],
    "financial": [
        r"\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b",  # Credit card
        r"account.*#?\s*\d+", r"routing.*\d{9}",
    ]
}

def classify_file(filepath):
    """Return highest sensitivity level found in file."""
    with open(filepath, 'r', errors='ignore') as f:
        content = f.read().lower()
    
    for level, patterns in SENSITIVE_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, content, re.IGNORECASE):
                return level
    return "internal"
```

### 2.2 Manual Review
- Automated classification reviewed by human before processing
- Client asked to confirm or adjust classification
- Any Restricted data flagged for additional controls

---

## Phase 3: Secure Storage

### 3.1 Encryption at Rest
```bash
# All client data encrypted with AES-256
# Encryption key derived from client-specific key + master key
openssl enc -aes-256-cbc -salt -pbkdf2 \
  -in $PLAINTEXT_FILE \
  -out $ENCRYPTED_FILE \
  -pass file:$CLIENT_KEY_FILE
```

### 3.2 Storage Architecture
```
Client Data/
├── client-[id]/
│   ├── raw/              # Original uploaded files (encrypted)
│   ├── processed/         # Cleaned, chunked data (encrypted)
│   ├── training/         # Final training dataset (encrypted)
│   └── manifests/        # File inventories + hashes
```

### 3.3 Access Controls
- Client data stored on isolated volume (not shared with other clients)
- Access requires: encrypted key + MFA
- Access log maintained (who, when, what)
- Minimum necessary access principle

### 3.4 Backup Policy
- Encrypted backups to isolated storage
- Retention: duration of project + 90 days post-delivery
- Then: secure erasure within 30 days of retention end

---

## Phase 4: Data Processing

### 4.1 PII/Sensitive Data Handling
```python
def redact_pii(text):
    """Redact PII for training data that shouldn't contain it."""
    redacted = re.sub(r"\b\d{3}-\d{2}-\d{4}\b", "[SSN]", text)
    redacted = re.sub(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z]{2,}\b", "[EMAIL]", redacted)
    redacted = re.sub(r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b", "[PHONE]", redacted)
    # Names, addresses handled via NER
    return redacted

def anonymize_for_training(text, entities):
    """Replace identified entities with category tokens."""
    for entity in entities:
        text = text.replace(entity["text"], f"[{entity['label'].upper()}]")
    return text
```

### 4.2 Data Cleaning Pipeline
```python
def clean_training_data(raw_dir, clean_dir):
    """Standard cleaning for training data."""
    for filename in os.listdir(raw_dir):
        filepath = os.path.join(raw_dir, filename)
        
        # 1. Basic cleaning
        text = open(filepath).read()
        text = normalize_whitespace(text)
        text = remove_control_characters(text)
        
        # 2. PII redaction
        text = redact_pii(text)
        
        # 3. Filter quality
        if len(text) < 50 or len(text) > 50000:
            continue  # Skip too short or too long
        
        # 4. Deduplication
        if is_duplicate(text):
            continue
        
        # 5. Save cleaned
        save(clean_dir, filename, text)
```

### 4.3 Chunking for Training
```python
def chunk_for_training(text, chunk_size=512, overlap=64):
    """Chunk text into training-ready segments."""
    tokens = tokenize(text)
    chunks = []
    for i in range(0, len(tokens), chunk_size - overlap):
        chunk_tokens = tokens[i:i + chunk_size]
        chunks.append(detokenize(chunk_tokens))
    return chunks
```

---

## Phase 5: Training Data Handling

### 5.1 Isolated Training Environment
- Each client trained in dedicated Docker container
- Container destroyed after training completes
- No cross-client data leakage possible

### 5.2 Model Weights
- Trained model weights belong to CLIENT
- We do not retain copies post-delivery (unless retainer)
- Client receives full model weights + inference code

### 5.3 Training Run Security
```bash
# Training runs in isolated network namespace
# No external network access from training containers
# All data volumes encrypted
docker run --network=none \
           --memory=32g \
           --device=/dev/nvidia0 \
           -v /encrypted/data:/data:ro \
           -v /encrypted/output:/output \
           namakan-training:latest
```

---

## Phase 6: Delivery

### 6.1 Secure Transfer
- Model weights delivered via encrypted SFTP or physical media (for large models)
- Transfer generates receipt + hash verification
- Client confirms receipt within 48 hours

### 6.2 Data Return/Destruction
After delivery:
1. Client confirms receipt of model
2. We destroy all copies of their data within 14 days
3. Client receives Certificate of Destruction
4. We retain zero copies unless retainer active

```python
def secure_delete(directory):
    """Overwrite and delete all files in directory."""
    import shutil
    for root, dirs, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            # Overwrite with random data 3x
            with open(filepath, 'r+b') as f:
                f.seek(0)
                f.write(os.urandom(os.path.getsize(filepath)))
                f.flush()
                os.fsync(f)
            os.remove(filepath)
    shutil.rmtree(directory)
```

---

## Phase 7: Audit & Compliance

### 7.1 Audit Log
Every data access, processing step, and transfer is logged:
```python
def audit(event_type, details):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "event": event_type,
        "details": details,
        "operator": get_current_user(),
        "ip": get_client_ip()
    }
    # Immutable log to append-only storage
    append_to_audit_log(log_entry)
```

### 7.2 Compliance Standards
- **SOC 2 Type II** — target for 2026
- **GDPR** — applicable if any EU data
- **HIPAA** — if healthcare clients with PHI (requires BAA)
- **Minnesota data privacy** — MN Statutes 13.05

### 7.3 Annual Security Review
- Penetration testing
- Access audit
- Policy review
- Incident response plan test

---

## Incident Response

If data breach suspected:
1. **Contain** — Isolate affected systems immediately
2. **Assess** — Determine scope within 24 hours
3. **Notify** — Affected clients within 72 hours (legal requirement)
4. **Remediate** — Fix root cause
5. **Review** — Post-incident report within 14 days

---

## Client Data Rights

- Client owns their data and model outputs
- We never use client data to train other clients' models
- We never share client data with third parties
- Client can request data summary or deletion at any time
- All personnel sign NDA + data handling agreement before accessing client data
