# Namakan Admin Dashboard

**Client Portal: Model Management, Integrations, and Analytics**

---

## Overview

A web-based dashboard where clients:
1. **Connect data sources** (CRM, database, documents)
2. **Upload and manage documents** for training
3. **Chat with their fine-tuned model** (if hosted)
4. **View analytics** (usage, performance, costs)

---

## Pages / Features

### 1. Dashboard Home

**Purpose:** Overview of model health and recent activity

**Components:**
- Model status card (active/inactive, version, last trained)
- Quick stats:
  - Total queries (today/week/month)
  - Average tokens/query
  - Uptime %
- Recent activity feed (last 10 interactions)
- Quick actions: "Chat with Model", "Upload Documents", "View Analytics"

```
┌─────────────────────────────────────────────────────────────┐
│  Namakan Dashboard                    [Acme Corp ▼] [?] [⚙] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────┐           │
│  │ Model: v1.3 │ │ Queries Today│ │ Uptime      │           │
│  │ 🟢 Active   │ │    1,247    │ │   99.8%     │           │
│  └─────────────┘ └─────────────┘ └─────────────┘           │
│                                                             │
│  Recent Activity                    Quick Actions           │
│  ─────────────────                  ─────────────           │
│  2 min ago: Lead research          [💬 Chat]               │
│  5 min ago: Ticket classified       [📄 Upload]             │
│  12 min: CRM updated               [📊 Analytics]          │
│  1 hr ago: New document added       [⚙️ Integrations]        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 2. Integrations Page

**Purpose:** Connect and manage data sources

**Supported Integrations:**

| Source | Status | Last Sync | Actions |
|--------|--------|-----------|---------|
| Salesforce | 🟢 Connected | 2 min ago | [Sync] [Settings] [Disconnect] |
| PostgreSQL | 🟢 Connected | 5 min ago | [Sync] [Settings] [Disconnect] |
| Google Drive | 🟢 Connected | 1 hr ago | [Sync] [Settings] [Disconnect] |
| HubSpot | 🔴 Not connected | — | [Connect] |

**Connect New Source:**

```
┌─────────────────────────────────────────────────────────────┐
│  Connect Integration                                       │
│                                                             │
│  [🔍 Search integrations...]                               │
│                                                             │
│  Popular:                                                   │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │  Salesforce  │ │   HubSpot    │ │  PostgreSQL  │       │
│  │   [Connect]  │ │   [Connect]  │ │   [Connect]  │       │
│  └──────────────┘ └──────────────┘ └──────────────┘       │
│                                                             │
│  Other:                                                     │
│  ┌──────────────┐ ┌──────────────┐ ┌──────────────┐       │
│  │    MySQL     │ │ Google Drive │ │    S3        │       │
│  │   [Connect]  │ │   [Connect]  │ │   [Connect]  │       │
│  └──────────────┘ └──────────────┘ └──────────────┘       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Integration Setup Flow (Salesforce example):**
1. Click "Connect Salesforce"
2. OAuth popup: Client logs into Salesforce
3. Select permissions (read only)
4. Choose data to sync (Cases, Contacts, Opportunities)
5. Set sync schedule (realtime, hourly, daily)
6. Click "Connect"

---

### 3. Documents Page

**Purpose:** Upload, manage, and view training documents

**Document Library:**

```
┌─────────────────────────────────────────────────────────────┐
│  Documents                          [Upload] [Filter ▼]    │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 📄 Warranty_Policy_v3.pdf        2.4 MB    Jan 15 2026  ││
│  │    Type: SOP | Used in: Training ✅ | Last used: 3d ago ││
│  │    [View] [Edit Tags] [Delete]                          ││
│  └─────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 📄 QC_Playbook.docx             1.1 MB    Feb 2 2026   ││
│  │    Type: SOP | Used in: Training ✅ | Last used: 1d ago││
│  │    [View] [Edit Tags] [Delete]                          ││
│  └─────────────────────────────────────────────────────────┘│
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 📊 Q4_Tickets_2025.csv           4.7 MB   Dec 31 2025  ││
│  │    Type: Training Data | Records: 3,247 | Training: v1  ││
│  │    [View] [Retrain with this] [Delete]                  ││
│  └─────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────┘
```

**Upload Flow:**
1. Click "Upload"
2. Drag & drop files or browse
3. Select document type: SOP | Training Data | Contract | Other
4. Add tags (optional)
5. Upload complete
6. File appears in library

**Supported Formats:**
- PDF, DOCX, TXT, CSV, JSON, Markdown

---

### 4. Model Chat Page

**Purpose:** Test and interact with fine-tuned model

**Chat Interface:**

```
┌─────────────────────────────────────────────────────────────┐
│  Acme Support AI v1.3                    [Retrain] [⚙️]   │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ 🟢 Model Active | 1,247 queries today | Latency: 45ms   ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │                    💬 AI Support                       ││
│  │ ─────────────────────────────────────────────────────── ││
│  │  [User]                                               ││
│  │  Customer says valve is leaking after 2 weeks...       ││
│  │                                                         ││
│  │                              [AI] ✓                     ││
│  │  Category: Quality - Warranty Claim                    ││
│  │  Escalation Level: L2                                 ││
│  │  Response: "We apologize for the inconvenience...     ││
│  │  ─────────────────────────────────────────────────     ││
│  │  Sources: Warranty_Policy_v3.pdf (Section 4.2)        ││
│  │  Confidence: 94%                                       ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  ┌─────────────────────────────────────────────────────────┐│
│  │ Type your message...                          [Send →] ││
│  └─────────────────────────────────────────────────────────┘│
│                                                             │
│  [📋 History] [📊 Analytics] [⚙️ Settings]                   │
└─────────────────────────────────────────────────────────────┘
```

**Features:**
- Real-time streaming responses
- Show which documents were used (citations)
- Confidence score per response
- Copy response
- Flag response (thumbs down = feedback for retraining)
- Chat history

---

### 5. Analytics Page

**Purpose:** Usage stats and model performance

**Overview Tab:**

```
┌─────────────────────────────────────────────────────────────┐
│  Analytics (Last 30 Days)              [📅 Last 30 days ▼] │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Usage                         Performance                  │
│  ┌────────────────────┐        ┌────────────────────────┐  │
│  │ Total Queries: 34,521│       │ Avg Latency: 45ms      │  │
│  │ Today: 1,247        │       │ P95 Latency: 120ms     │  │
│  │ Yesterday: 1,102     │       │ Error Rate: 0.3%       │  │
│  │ ┌──────────────────┐│       │                        │  │
│  │ │    ▁▂▃▅▆▇█▇▅▃▂▁│  │       │ Quality Rating: 4.2/5 │  │
│  │ │  Queries/Day      ││       │ 👍 89% | 👎 11%       │  │
│  │ └──────────────────┘│       └────────────────────────┘  │
│  └────────────────────┘                                    │
│                                                             │
│  Category Distribution           Escalation Breakdown       │
│  ┌────────────────────┐        ┌────────────────────────┐  │
│  │ Quality: 45%  ████ │        │ L1 (Auto):    72%      │  │
│  │ Billing:  25%  ██  │        │ L2 (Review):  23%     │  │
│  │ Shipping: 18%  █   │        │ L3 (Escalate): 5%     │  │
│  │ Other:    12%  █   │        └────────────────────────┘  │
│  └────────────────────┘                                    │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Training Tab:**

```
┌─────────────────────────────────────────────────────────────┐
│  Training History                                           │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Version | Date       | Records | Quality | Status          │
│  ─────────────────────────────────────────────────────────  │
│  v1.3    | Feb 15 2026| 4,521   | 4.5/5  | 🟢 Active      │
│  v1.2    | Jan 20 2026| 3,247   | 4.2/5  | Retired       │
│  v1.1    | Dec 10 2025| 2,100   | 3.8/5  | Retired       │
│  v1.0    | Nov 1 2025 | 1,500   | 3.5/5  | Retired       │
│                                                             │
│  [Train New Version]                                        │
│                                                             │
│  Next Scheduled Retrain: March 15, 2026                   │
│  Triggers: [📅 Scheduled] [☑️ Manual Only]                 │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Cost Tab:**

```
┌─────────────────────────────────────────────────────────────┐
│  Cost Analysis (February 2026)                              │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Hosting:           $200.00                                │
│  Compute (overage): $15.34                                 │
│  Storage:           $12.00                                  │
│  ─────────────────────────────────                          │
│  Total:             $227.34                                │
│                                                             │
│  Query Breakdown:                                           │
│  34,521 queries × $0.0004 = $13.81                        │
│  (included in base plan)                                    │
│                                                             │
│  [Download Invoice] [Set Budget Alert]                      │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

---

### 6. Settings Page

**Sections:**
- Account & Billing
- API Keys (for external integrations)
- Team Members (add/remove users)
- Notifications (email, Slack alerts)
- Model Settings (temperature, max tokens)
- Security (2FA, IP allowlist)

---

## Technical Architecture

### Frontend

```
/dashboard
├── /integrations      # CRM/DB connections
├── /documents         # Document library
├── /chat              # Model chat interface
├── /analytics         # Usage stats
└── /settings          # Account settings
```

**Stack:**
- Next.js (reuse existing frontend)
- Tailwind CSS
- React Query (for API calls)
- Recharts (for analytics charts)

### Backend

**API Endpoints:**

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/api/dashboard/integrations` | GET, POST | List/add integrations |
| `/api/dashboard/integrations/:id` | PUT, DELETE | Update/disconnect |
| `/api/dashboard/documents` | GET, POST, DELETE | Manage documents |
| `/api/dashboard/chat` | POST | Send to model |
| `/api/dashboard/analytics` | GET | Usage stats |
| `/api/dashboard/training` | GET, POST | Trigger/view training |

**Auth:**
- Clerk or NextAuth for dashboard login
- Per-client API keys for integrations

### Database

**Schema (Supabase or PostgreSQL):**

```sql
-- Clients
CREATE TABLE clients (
  id UUID PRIMARY KEY,
  name TEXT,
  plan TEXT, -- starter, professional, enterprise
  created_at TIMESTAMP
);

-- Integrations
CREATE TABLE integrations (
  id UUID PRIMARY KEY,
  client_id UUID REFERENCES clients(id),
  type TEXT, -- salesforce, postgres, gdrive
  credentials_encrypted JSONB,
  last_sync TIMESTAMP,
  status TEXT
);

-- Documents
CREATE TABLE documents (
  id UUID PRIMARY KEY,
  client_id UUID REFERENCES clients(id),
  filename TEXT,
  storage_url TEXT,
  type TEXT,
  tags TEXT[],
  uploaded_at TIMESTAMP
);

-- Training runs
CREATE TABLE training_runs (
  id UUID PRIMARY KEY,
  client_id UUID REFERENCES clients(id),
  version TEXT,
  record_count INT,
  quality_score FLOAT,
  status TEXT,
  trained_at TIMESTAMP
);

-- Usage logs (for analytics)
CREATE TABLE usage_logs (
  id UUID PRIMARY KEY,
  client_id UUID REFERENCES clients(id),
  query TEXT,
  response TEXT,
  tokens INT,
  latency_ms INT,
  created_at TIMESTAMP
);
```

### Storage

| Data | Storage | Service |
|------|---------|---------|
| Documents | Client's files | AWS S3 or Google Cloud Storage |
| Credentials | Encrypted | AWS Secrets Manager |
| Model files | Trained weights | S3 or shared Drive |
| Usage logs | Analytics | PostgreSQL or ClickHouse |

---

## MVP Scope

**Phase 1 (MVP - 4-6 weeks):**
- [ ] Dashboard layout and navigation
- [ ] Document upload and library
- [ ] Basic chat interface
- [ ] Simple analytics (query count, latency)
- [ ] Static integration cards (no real OAuth yet)

**Phase 2:**
- [ ] Real OAuth integrations (Salesforce, HubSpot)
- [ ] Chat history
- [ ] Training trigger
- [ ] Cost tracking

**Phase 3:**
- [ ] Full analytics
- [ ] Team management
- [ ] API keys
- [ ] Webhooks for client integrations

---

## Cost to Build

| Component | Effort | Cost |
|-----------|--------|------|
| Frontend (MVP) | 2-3 weeks | $2,000-4,000* |
| Backend (MVP) | 1-2 weeks | $1,000-2,000* |
| Auth integration | 2-3 days | $500* |
| Database design | 2-3 days | $500* |
| **Total MVP** | **4-6 weeks** | **$4,000-7,000** |

*Rough estimate at $150/hr

---

## Pricing for Clients

| Feature | Starter | Professional | Enterprise |
|---------|---------|--------------|------------|
| Dashboard access | ✅ | ✅ | ✅ |
| Document storage | 1GB | 10GB | 100GB |
| Integrations | 1 | 3 | Unlimited |
| Chat interface | ✅ | ✅ | ✅ |
| Analytics | Basic | Full | Full + Export |
| API access | ❌ | ✅ | ✅ |
| Training per quarter | 1 | 2 | 4 |
| **Monthly price** | **$250** | **$500** | **$1,000** |

---

## Design Direction

**Style:** Clean, minimal, Linear/Shopify-inspired

**Colors:**
- Primary: Teal (#0D9488)
- Background: White/off-white
- Text: Dark slate
- Success: Green
- Error: Red
- Muted: Gray

**Typography:**
- Headings: Inter Bold
- Body: Inter Regular
- Monospace (code): JetBrains Mono

**Icons:** Lucide or Heroicons

---

## Next Steps

1. **Design mockups** — Figma or rough sketches
2. **Tech stack decision** — Use existing Next.js + new backend?
3. **Database choice** — Supabase (easy) vs. PostgreSQL (flexible)
4. **Auth provider** — Clerk vs. NextAuth

Want me to draft the database schema, API spec, or start building components?
