# Infrastructure and Cost Estimates
## Detailed Breakdown for MVP and Scale

**Date:** February 21, 2026
**Audience:** CFO, CEO, Business Team

---

## 1. COST SUMMARY

### 1.1 MVP Monthly Costs

| Category | Component | Low Estimate | High Estimate |
|----------|-----------|--------------|---------------|
| **Compute** | EKS Cluster (3 nodes) | $1,500 | $2,500 |
| **Compute** | Spark Clusters | $2,000 | $4,000 |
| **Storage** | S3 (10TB) | $250 | $350 |
| **Database** | RDS PostgreSQL | $500 | $800 |
| **Cache** | ElastiCache | $300 | $500 |
| **AI/ML** | LLM API (Claude) | $1,000 | $2,000 |
| **Networking** | Data transfer | $200 | $400 |
| **Monitoring** | CloudWatch | $150 | $250 |
| **SSL/Cert** | ACM | $0 | $0 |
| **Total/Month** | | **$5,900** | **$10,800** |

### 1.2 Annual Costs (MVP)

| Scenario | Monthly | Annual |
|----------|---------|--------|
| Low Estimate | $5,900 | $70,800 |
| High Estimate | $10,800 | $129,600 |
| **Average** | **$8,350** | **$100,200** |

---

## 2. DETAILED INFRASTRUCTURE

### 2.1 Kubernetes Cluster (EKS)

**Purpose:** Run all platform services

| Resource | Specification | Monthly Cost |
|----------|---------------|--------------|
| 3x m6i.xlarge | 4 vCPU, 16GB RAM | $1,200 - $1,800 |
| EBS Volumes | 500GB gp3 | $100 - $150 |
| Load Balancers | 2x Application LB | $200 - $300 |
| EKS Management | $0.10/hour per cluster | $70 |
| **Total** | | **$1,500 - $2,500** |

### 2.2 Spark Cluster

**Purpose:** Query execution and data processing

**Option A: Self-Managed on EKS**

| Resource | Specification | Monthly Cost |
|----------|---------------|--------------|
| 5x r6i.2xlarge | Drivers | $1,500 - $2,000 |
| 10x r6i.xlarge | Workers | $2,000 - $3,000 |
| Spot Instances | 50% savings | -$1,000 |
| **Total** | | **$2,500 - $4,000** |

**Option B: EMR (AWS Managed)**

| Resource | Specification | Monthly Cost |
|----------|---------------|--------------|
| Master (r6i.xlarge) | 1x | $300 - $400 |
| Core (r6i.xlarge) | 5x | $1,200 - $1,600 |
| Task (r6i.xlarge) | 5x (on-demand) | $1,200 - $1,600 |
| EMR Fee | $0.18/hour | $130 |
| **Total** | | **$2,800 - $4,600** |

### 2.3 Storage (S3)

**Purpose:** Data lake storage

| Tier | Size | Cost/TB | Monthly |
|------|------|---------|---------|
| Standard | 8TB | $23 | $184 |
| Intelligent Tiering | 2TB | $25 | $50 |
| **Total** | **10TB** | | **$234** |

**Plus S3 Requests:**
- PUT/COPY: $0.005/1,000 requests
- GET/SELECT: $0.0004/1,000 requests
- **Estimated:** $50/month

### 2.4 Database (RDS PostgreSQL)

**Purpose:** Application data, metadata, catalog

| Instance | Specification | Monthly Cost |
|----------|---------------|--------------|
| db.r6i.xlarge | 4 vCPU, 32GB | $500 - $800 |
| Storage | 500GB gp3 | $125 |
| Backup | 7-day retention | Included |
| **Total** | | **$500 - $800** |

### 2.5 Cache (ElastiCache)

**Purpose:** Query result caching, session storage

| Instance | Specification | Monthly Cost |
|----------|---------------|--------------|
| cache.r6i.large | 2 vCPU, 12GB | $300 - $500 |
| **Total** | | **$300 - $500** |

### 2.6 AI/ML (LLM API)

**Purpose:** Natural language to SQL

**Anthropic Claude Pricing:**
- Input: $3/M tokens
- Output: $15/M tokens

**Estimated Usage:**
| Operation | Est. Tokens | Monthly |
|-----------|--------------|---------|
| 1,000 queries/day | 50K input, 10K output | $300 |
| 500 complex queries | 100K input, 20K output | $450 |
| 200 batch operations | 200K input, 50K output | $350 |
| Buffer/overhead | | $400 |
| **Total** | | **$1,500** |

**With OpenAI GPT-4 fallback:** +$500-1,000/month

### 2.7 Networking

| Component | Description | Monthly |
|-----------|-------------|---------|
| NAT Gateway | $0.045/GB processed | $100 - $200 |
| Data Transfer Out | First 1GB free, then $0.09/GB | $100 - $200 |
| VPN/Direct Connect | Not needed for MVP | $0 |
| **Total** | | **$200 - $400** |

### 2.8 Monitoring

| Service | Description | Monthly |
|---------|-------------|---------|
| CloudWatch | Logs, metrics, alarms | $100 - $200 |
| DataDog (optional) | Better APM | +$200-400 |
| **Total** | | **$100 - $200** (if self-managed) |

---

## 3. COST REDUCTION STRATEGIES

### 3.1 Spot Instances

**Savings:** 50-70% on compute

| Before | After |
|--------|-------|
| $4,000/month | $1,500-2,000/month |

**Implementation:** Use Spot for non-critical Spark workers

### 3.2 Reserved Instances

**Savings:** 30-50% on baseline

| Before | After |
|--------|-------|
| $2,500/month | $1,500-1,800/month |

**Implementation:** Reserve core infrastructure

### 3.3 S3 Intelligent Tiering

**Savings:** Auto-tier for infrequent access

**Savings:** 10-20% on storage

### 3.4 Query Result Caching

**Savings:** 20-40% on LLM costs

**Implementation:** Cache common queries

### 3.5 Combined Potential Savings

| Category | Full Price | Optimized | Savings |
|----------|------------|-----------|---------|
| Compute | $5,000 | $2,500 | 50% |
| Storage | $300 | $250 | 15% |
| LLM | $2,000 | $1,200 | 40% |
| **Total** | **$7,300** | **$3,950** | **46%** |

---

## 4. SCALING COSTS

### 4.1 Mid-Market (50 users, 100TB)

| Category | MVP (10TB) | Mid-Market (100TB) |
|----------|------------|-------------------|
| Compute (K8s) | $2,000 | $5,000 |
| Compute (Spark) | $4,000 | $15,000 |
| Storage (S3) | $300 | $3,000 |
| Database | $800 | $1,500 |
| Cache | $500 | $1,000 |
| AI/ML | $2,000 | $10,000 |
| Networking | $400 | $2,000 |
| Monitoring | $200 | $500 |
| **Total** | **$10,200** | **$38,000** |

### 4.2 Enterprise (200 users, 1PB)

| Category | Cost |
|----------|------|
| Compute (K8s) | $15,000 |
| Compute (Spark) | $50,000 |
| Storage (S3) | $25,000 |
| Database | $3,000 |
| Cache | $2,000 |
| AI/ML | $40,000 |
| Networking | $5,000 |
| Monitoring | $1,000 |
| **Total** | **$141,000** |

### 4.3 Cost Per User

| Tier | Users | Monthly Cost | Cost/User |
|------|-------|--------------|-----------|
| MVP | 10 | $8,350 | $835 |
| Mid-Market | 50 | $38,000 | $760 |
| Enterprise | 200 | $141,000 | $705 |

---

## 5. ONE-TIME COSTS

### 5.1 Initial Setup

| Item | Cost | Notes |
|------|------|-------|
| Architecture Design | $10-20K | Engineering or internal |
| Dev Environment Setup | $5-10K | Team onboarding |
| Security Review | $10-20K | Third-party audit |
| Legal/Compliance | $5-15K | Terms, privacy |
| **Total** | **$30-65K** | |

### 5.2 Development Costs

| Phase | Duration | Team Size | Cost |
|-------|----------|-----------|------|
| MVP Development | 6 months | 5-7 | $300-500K |
| Beta/Launch | 3 months | 7-10 | $200-350K |
| Year 1 Total | 9 months | | **$500-850K** |

---

## 6. BREAK-EVEN ANALYSIS

### 6.1 Revenue Per Customer

| Tier | Monthly Price | Annual |
|------|---------------|--------|
| Startup | $1,000 | $12,000 |
| Growth | $5,000 | $60,000 |
| Enterprise | $25,000 | $300,000 |

### 6.2 Customer Count for Break-Even

**At MVP pricing ($8K/month infrastructure):**

| Plan | Price | Customers Needed |
|------|-------|-----------------|
| Startup | $1,000/mo | 8 |
| Growth | $5,000/mo | 2 |
| Enterprise | $25,000/mo | 1 |

**Realistic Year 1:**
- Month 1-6: 0-5 Startup customers
- Month 7-12: 5-15 Startup + 1-3 Growth
- Break-even: ~20-30 customers

---

## 7. COST MANAGEMENT RECOMMENDATIONS

### 7.1 Immediate Actions

1. **Use Spot Instances** - Save 50% on Spark
2. **Enable S3 Intelligent Tiering** - Save 15% on storage
3. **Implement Query Caching** - Save 30% on LLM costs
4. **Set Budget Alerts** - Prevent surprise bills

### 7.2 Medium-Term

1. **Reserved Instances** - Save 30% on baseline
2. **Right-sizing** - Monitor and adjust
3. **Cost Allocation Tags** - Track by customer

### 7.3 Long-Term

1. **Multi-Cloud** - Leverage pricing differences
2. **Custom LLM** - Reduce per-token costs
3. **Build vs Buy** - In-house more components

---

## 8. INFRASTRUCTURE DIAGRAM

```
┌─────────────────────────────────────────────────────────────────┐
│                         AWS Region (us-east-1)                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │                    VPC (10.0.0.0/16)                     │  │
│  │                                                           │  │
│  │  ┌─────────────────────────────────────────────────────┐ │  │
│  │  │              Public Subnet (10.0.1.0/24)           │ │  │
│  │  │  ┌─────────────┐  ┌─────────────┐                 │ │  │
│  │  │  │   ALB       │  │   NAT GW    │                 │ │  │
│  │  │  └─────────────┘  └─────────────┘                 │ │  │
│  │  └─────────────────────────────────────────────────────┘ │  │
│  │                                                            │  │
│  │  ┌─────────────────────────────────────────────────────┐ │  │
│  │  │            Private Subnet (10.0.2.0/24)             │ │  │
│  │  │  ┌──────────────┐ ┌──────────────┐ ┌────────────┐ │ │  │
│  │  │  │   EKS        │ │   RDS        │ │  Elasti    │ │ │  │
│  │  │  │   (K8s)     │ │  PostgreSQL   │ │  Cache    │ │ │  │
│  │  │  └──────────────┘ └──────────────┘ └────────────┘ │ │  │
│  │  └─────────────────────────────────────────────────────┘ │  │
│  │                                                            │  │
│  │  ┌─────────────────────────────────────────────────────┐ │  │
│  │  │           Private Subnet (10.0.3.0/24)             │ │  │
│  │  │  ┌──────────────┐ ┌──────────────┐ ┌────────────┐ │ │  │
│  │  │  │  Spark       │ │  Spark       │ │  Spark    │ │ │  │
│  │  │  │  Master      │ │  Core        │ │  Workers  │ │ │  │
│  │  │  └──────────────┘ └──────────────┘ └────────────┘ │ │  │
│  │  └─────────────────────────────────────────────────────┘ │  │
│  │                                                            │  │
│  │  ┌─────────────────────────────────────────────────────┐ │  │
│  │  │           Private Subnet (10.0.4.0/24)             │ │  │
│  │  │  ┌──────────────┐ ┌──────────────┐               │ │  │
│  │  │  │   S3 Bucket  │ │   S3 Bucket  │               │ │  │
│  │  │  │  (Data Lake) │ │  (Artifacts) │               │ │  │
│  │  │  └──────────────┘ └──────────────┘               │ │  │
│  │  └─────────────────────────────────────────────────────┘ │  │
│  │                                                            │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

---

## 9. RECOMMENDATIONS FOR CFO

### 9.1 Budget Ask

| Category | Year 1 |
|----------|--------|
| Infrastructure | $100-150K |
| Development | $500-850K |
| One-time | $30-65K |
| **Total** | **$630K - $1.1M** |

### 9.2 Monthly Run Rate

| Phase | Monthly |
|-------|---------|
| MVP (Month 1-6) | $8-15K |
| Growth (Month 7-12) | $25-50K |
| Year 2 (estimated) | $100-200K |

### 9.3 Key Cost Drivers

1. **LLM costs** - Scale with usage (manage via caching)
2. **Compute** - Manage via Spot instances
3. **Storage** - Grows linearly with data

---

*Document Owner: Technical Team*
*Last Updated: 2026-02-21*
