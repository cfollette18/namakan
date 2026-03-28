## 1. Pricing Strategy

### 1.1 Usage-Based Pricing Model

**Core: Pay only for what you use. No seats, no subscriptions.**

| Tier | Target Segment | Price | What's Included |
|------|---------------|-------|-----------------|
| **Free** | Developers, hobbyists | $0 forever | 1,000 queries/month, 1GB storage |
| **Pay-as-you-go** | Anyone | $0.001/query + $0.10/GB storage | Unlimited scale, pay monthly |
| **Enterprise** | Large orgs | Custom flat rate | Dedicated infra, SLA, unlimited |

### 1.2 Usage Pricing

| Metric | Price | Notes |
|--------|-------|-------|
| **AI Query** | $0.005/query | Natural language to SQL |
| **Standard Query** | $0.001/query | SQL executed |
| **Storage** | $0.10/GB/month | First 1GB free |
| **API Calls** | $0.0001/call | REST API access |

### 1.3 Why Usage-Based?

- **No lock-in:** Leave anytime, pay only what you used
- **Scales with you:** Startup pays $10, enterprise pays $10K
- **Fair:** You only pay for value received
- **Founder-friendly:** No big subscription commitments

### 1.4 Comparison

| Metric | Namakan | Snowflake | Databricks |
|--------|---------|-----------|------------|
| **Model** | Pure usage | Usage + storage | Usage (DBU) |
| **Entry** | $0 | ~$2/credit | ~$0.07/DBU |
| **Free forever** | Yes | No | Limited |
| **Predictability** | Low | Medium | Medium |
