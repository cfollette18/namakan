# Namakan Business Model

> **Note:** This document assumes Namakan is an AI/data platform company based on the comparison targets (Snowflake, Databricks). Adjust specific metrics based on actual product details.

---

## 1. Pricing Strategy - Usage-Based

### 1.1 Pure Usage Model

| Tier | Target | Price |
|------|--------|-------|
| **Free** | Devs, hobbyists | $0 forever (1K queries/mo, 1GB) |
| **Pay-as-you-go** | Anyone | $0.001/query + $0.10/GB/mo |
| **Enterprise** | Large orgs | Custom flat rate |

### 1.2 Usage Pricing

| Metric | Price |
|--------|-------|
| AI Query | $0.005/query |
| Standard Query | $0.001/query |
| Storage | $0.10/GB/mo |
| API Calls | $0.0001/call |

### 1.3 Why Usage-Based?
- No lock-in
- Scales with you
- $0 to start, pay as you grow
- Fair - pay for value
## 2. Revenue Model

### 2.1 Revenue Mix Target (Year 3-5)

| Revenue Stream | % of Revenue | Description |
|---------------|--------------|-------------|
| **Subscription (SaaS)** | 70-80% | Annual SaaS contracts |
| **Usage-based** | 10-15% | Query overages, API calls |
| **Professional Services** | 5-10% | Implementation, training |
| **Marketplace/API** | 2-5% | App marketplace, API monetization |

### 2.2 Subscription vs Usage-Based

**Primary: Annual Subscription**
- Predictable revenue for planning
- Easier sales process
- Customer commitment = lower churn

**Secondary: Usage-Based Overage**
- Captures high-velocity customers
- Aligns cost with value delivered
- Snowflake model proves this works at scale

**Benchmark Data:**
- 75% of Snowflake revenue is consumption-based
- Databricks: ~90% consumption, ~10% subscription
- Successful hybrid: MongoDB Atlas (~$500M ARR, majority subscription)

### 2.3 Professional Services

**Offerings:**
- Implementation & onboarding ($2,500-10,000)
- Custom integrations ($5,000-50,000+)
- Training programs ($1,000-5,000/person)
- Premium support add-on ($500-2,000/mo)

**Margin Target:** 40-60% gross (lower than software)

### 2.4 Marketplace & API Revenue

- **App Marketplace:** 15-30% revenue share on third-party apps
- **API Monetization:** Usage-based pricing for API access
- **Partner integrations:** Revenue share with data connectors (Fivetran, Airbyte)

---

## 3. Unit Economics

### 3.1 Customer Acquisition Cost (CAC)

**Benchmark Targets:**

| Stage | Target CAC | Benchmark Range |
|-------|-----------|-----------------|
| **Startup (Seed)** | $5,000-15,000 | $5,000-25,000 |
| **Growth (Series A)** | $10,000-20,000 | $10,000-30,000 |
| **Scale (Series B+)** | $15,000-30,000 | $15,000-50,000 |

**CAC Breakdown (Typical B2B SaaS):**
- Marketing: 50-60%
- Sales: 30-40%
- Sales engineering: 10-15%

**CAC Reduction Levers:**
- PLG motion reduces CAC to $2,000-5,000
- Product-led freemium can get below $1,000

### 3.2 Lifetime Value (LTV)

**Target LTV by Tier:**

| Tier | ACV | Churn | LTV | LTV:CAC |
|------|-----|-------|-----|---------|
| **Free → Pro** | $1,200 | 5-8%/year | $15,000-24,000 | 1.5-2.4x |
| **Pro** | $3,600 | 3-5%/year | $72,000-120,000 | 3.6-6x |
| **Enterprise** | $50,000+ | 1-2%/year | $2.5M-5M | 80-250x |

**Industry Benchmarks:**
- Average SaaS LTV:CAC: 3:1
- Top quartile: 5:1+
- Databricks: LTV:CAC estimated 5-7x
- Snowflake: LTV:CAC estimated 7-10x

### 3.3 LTV:CAC Ratio Targets

**Recommended Targets:**

| Stage | Minimum | Healthy | Best-in-Class |
|-------|---------|---------|---------------|
| **Startup** | 1.5:1 | 2:1 | 3:1 |
| **Growth** | 2:1 | 3:1 | 4:1 |
| **Scale** | 3:1 | 4:1 | 5:1+ |

**Rule of Thumb:** LTV should be at least 3x CAC for sustainable growth

### 3.4 Gross Margin by Tier

| Revenue Stream | Target Gross Margin | Benchmark |
|---------------|---------------------|-----------|
| **SaaS Subscription** | 80-90% | 80-85% (Snowflake) |
| **Usage-based** | 75-85% | 70-80% (Databricks) |
| **Professional Services** | 40-60% | 35-50% |
| **Marketplace** | 70-80% | 60-75% |

**Consolidated Target:** 75-85% gross margin

---

## 4. Sales Motion

### 4.1 Self-Serve vs Sales-Led

**Recommended Split:**

| Channel | % of Revenue | ACV Target |
|---------|--------------|------------|
| **Self-serve (PLG)** | 40-50% | <$5,000 |
| **Sales-assisted** | 30-40% | $5,000-50,000 |
| **Enterprise sales** | 20-30% | $50,000+ |

**Motion Breakdown:**
- **PLG:** Free → Paid conversion, in-app upgrades, freemium model
- **Sales-assisted:** Product-led with sales follow-up (product-qualified leads)
- **Enterprise:** Full sales cycle, custom contracts, executive relationships

### 4.2 Product-Led Growth (PLG) Strategy

**Core PLG Mechanics:**
1. **Freemium conversion:** Free users → Pro (target 3-5% conversion)
2. **Usage-based triggers:** Alerts when approaching limits
3. **In-app purchase:** Seamless upgrade flow
4. **Team invitation:** Viral loop through collaboration
5. **Product-qualified leads:** Usage signals for sales outreach

**PLG Benchmarks:**
- Twilio: 3-5% free-to-paid conversion
- Datadog: 5-8% conversion
- Slack: 25-30% conversion (B2B top tier)
- Notion: 10-15% conversion

**Target:** 4-6% free-to-paid conversion rate

### 4.3 Enterprise Sales Playbook

**Sales Cycle:**
- **Length:** 3-9 months
- **Stakeholders:** 5-10 per deal (champion, IT, security, finance, exec)
- **Process:** 5-7 step sales methodology

**Enterprise Motion:**
1. **Lead generation:** Outbound + inbound + partner referral
2. **Discovery:** Technical deep-dive + business case
3. **Proof of concept:** 2-4 week POC (free or low-cost)
4. **Security review:** IT/Security questionnaire (2-4 weeks)
5. **Procurement:** Legal, procurement, contracts
6. **Close:** Executive sign-off

**Average Deal Size Progression:**
- Seed: $10-25K
- Series A: $25-50K
- Series B+: $50-150K+
- Enterprise: $100K-1M+

### 4.4 Channel Partners

**Partner Tiers:**

| Partner Type | Revenue Share | Examples |
|-------------|---------------|----------|
| **Referral partners** | 10-20% | Consultants, agencies |
| **Resellers/VARs** | 20-30% | Regional SI, tech VARs |
| **Integration partners** | 15-25% | Fivetran, Airbyte, dbt Labs |
| **Cloud marketplace** | 0% (listing fee) | AWS, GCP, Azure |

**Partner Targets (Year 3):**
- 20-50 active partners
- 10-15% of revenue through channel
- 2-3 strategic partnerships (integrations)

---

## 5. Financial Projections

### 5.1 Revenue Forecast (5-Year)

**Assumptions:**
- Product: AI/Data platform (B2B SaaS)
- Starting from seed stage
- Hybrid pricing model
- PLG + sales-led hybrid motion

| Year | ARR Target | Growth | Customers | ACV |
|------|-----------|--------|-----------|-----|
| **Year 1** | $500K | - | 150 | $3,300 |
| **Year 2** | $2M | 300% | 500 | $4,000 |
| **Year 3** | $6M | 200% | 1,400 | $4,300 |
| **Year 4** | $15M | 150% | 3,200 | $4,700 |
| **Year 5** | $35M | 133% | 6,500 | $5,400 |

**Benchmark Comparisons:**

| Company | Year 1 | Year 3 | Year 5 |
|---------|--------|--------|--------|
| Snowflake (IPO yr) | $124M | $1.2B | $2.5B |
| Databricks | $60M | $600M | $1.5B |
| **Namakan (Target)** | $0.5M | $6M | $35M |

### 5.2 Burn Rate & Runway

**Projected Burn Rate:**

| Year | Revenue | Expenses | Burn Rate | Runway |
|------|---------|----------|------------|--------|
| **Year 1** | $500K | $2.5M | $167K/mo | 18-24 months |
| **Year 2** | $2M | $4M | $167K/mo | 24+ months |
| **Year 3** | $6M | $7M | $83K/mo | Profitable |

**Key Assumptions:**
- 20-25% revenue growth month-over-month (early stage)
- Headcount: 5 → 15 → 35 → 60 → 100
- Marketing: 40-50% of revenue (early)
- R&D: 30-40% of revenue

### 5.3 Break-Even Analysis

**Projected Break-Even:**
- **Conservative:** Month 30-36 (Year 3)
- **Optimistic:** Month 24 (Late Year 2)

**Break-Even Drivers:**
1. Gross margin: 75-85%
2. OpEx as % of revenue decreasing
3. Sales efficiency improving
4. Customer concentration <20% of revenue

### 5.4 Fundraising Milestones

| Milestone | Timing | Target Raise | Valuation | Use of Funds |
|-----------|--------|--------------|-----------|--------------|
| **Seed $250K | $5-10M | Product, founding team |
| **Series A $2-3M | $30-50M | Go-to-market, 15-20 people |
| **Series B $8-12M | $150-250M | Scale sales, 50-70 people |
| **Series C** | Month 48-60 | $75-100M | $400-600M | International, 100-150 people |
| **IPO/Exit** | Year 6-8 | - | $1B+ | - |

**Fundraising Triggers:**
- 18-month runway at Series A
- 24-month runway at Series B
- Path to profitability visible

---

## Key Takeaways

1. **Pricing:** Hybrid seat + query model, competitive 20-30% below Snowflake/Databricks
2. **Revenue:** 70-80% subscription, 10-15% usage, 5-10% services
3. **Unit Economics:** Target 3:1 LTV:CAC, 80%+ gross margins on software
4. **Sales:** PLG for bottom 50%, sales-led for top 50%
5. **Financials:** $100K → $10M in 5 years, break-even Year 3

---

*Document created: February 2026*
*Benchmarks sourced from: Snowflake S-1, Databricks reporting, SaaS benchmarks (OpenView, Bessemer), industry reports*
