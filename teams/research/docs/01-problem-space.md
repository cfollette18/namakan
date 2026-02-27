# Deep Problem Space Analysis: Data Cloud Platforms

## Executive Summary

This document captures real pain points from users of existing data cloud platforms (Snowflake, Databricks, BigQuery, Redshift) gathered from Reddit, Hacker News, forums, and industry discussions.

---

## 1. SNOWFLAKE PAIN POINTS

### 1.1 Cost Complexity and Unpredictability

**Primary Complaints:**
- "Snowflake is $$$$. That is if you are lazy who does not read documentation"
- Users report 2-3x cost increases during peak periods
- Complex credit consumption model hard to predict
- Enterprise contracts can run $300K-2M+/year

**Specific Issues:**
- Virtual warehouse sizing is non-trivial
- Storage costs accumulate silently
- Query optimization requires expertise
- "Lazy" users get blindsided by bills

**User Quotes:**
> "We were paying $50K/month and couldn't figure out why. Turns out we had warehouses running 24/7."

> "The pricing calculator is useless. Actual usage bears no resemblance."

### 1.2 Limited Customization and Flexibility

**Primary Complaints:**
- Can't configure target schemas in OpenFlow CDC
- Customizing workflows locks users out of updates
- No native primary key enforcement
- Security model is "confusing" and "messy"

**Specific Issues:**
- OpenFlow: "biggest downside - cannot configure target snowflake schema"
- Custom workflow updates = locked out of future updates
- Security RBAC requires careful upfront planning

### 1.3 Usability Issues

**Primary Complaints:**
- No SQL auto-complete in classic UI
- Tasks are "pretty bad and get really messy over time"
- Environment variables scattered across processors
- Error logs are "janky to navigate"

**Specific Issues:**
- Must switch between old and new UI for different features
- No unified UI for workflow variable management
- Scheduling simple queries requires external tools

### 1.4 Real-Time Limitations

**Primary Complaints:**
- "While real-time is tough with Snowflake and it is more like 5-10 second near real-time"
- No true streaming at sub-second latency
- Snowpipe has limitations

---

## 2. DATABRICKS PAIN POINTS

### 2.1 Complexity and Learning Curve

**Primary Complaints:**
- "Good luck understanding Databricks execution profile!"
- Configuration is "complex" and "messy"
- More DIY than Snowflake's "it just works"

**Specific Issues:**
- Spark is hard to optimize
- Multiple tools to manage (Spark, Delta Lake, MLflow)
- Steeper SQL skills required

### 2.2 Cost Management

**Primary Complaints:**
- DBU (Databricks Unit) consumption hard to predict
- Can be expensive for certain workloads
- Cloud infrastructure costs add up

### 2.3 Ecosystem Fragmentation

**Primary Complaints:**
- Need multiple tools for complete solution
- No "batteries included" experience
- Integration complexity

---

## 3. GENERAL DATA PLATFORM PAIN POINTS

### 3.1 Tool Sprawl

**User Complaints from HN:**
> "While at our prior roles as data engineers, we've both felt the pain of data APIs. We either had to spend weeks building out data pipelines in house or spend a lot on ETL tools like Fivetran."

> "We felt like second class citizens with how we were told to get data - 'just loop through this API 1000 times', 'you probably won't get rate limited' (we did)"

**Common Issues:**
- Multiple ETL tools required (Fivetran, HVR, IICS, AWS DMS, Snowpipe)
- High licensing costs for multiple tools
- Complex multi-vendor environments

### 3.2 Cross-Cloud Complexity

**Common Issues:**
- Moving data between clouds is "difficult"
- No native cross-cloud sync in most platforms
- Each cloud has separate account/management

### 3.3 Data Quality Gaps

**From Monte Carlo (Data Observability Company):**
> "More than 40% of companies don't trust the outputs of their AI/ML models"
> "More than 45% of companies cite data quality as the top obstacle to AI success"

**Common Issues:**
- No native data quality in platforms
- Silent data failures
- Data quality is always "someone else's problem"

### 3.4 API/Developer Experience

**Common Issues:**
- Poor APIs for programmatic access
- Limited CLI functionality
- Not designed for modern developer workflows
- "Enterprise software from 1990s" feel

---

## 4. MARKET PROBLEMS

### 4.1 Vendor Lock-In

**Common Complaints:**
- Proprietary formats (Snowflake)
- Hard to export data
- "Hostage" concerns
- Migration is painful

### 4.2 Hidden Complexity

**Common Complaints:**
- "Works out of the box" but optimization is hard
- Features exist but are undocumented
- Best practices require consulting

### 4.3 Support Quality

**Common Complaints:**
- Support varies by contract tier
- Community forums are hit or miss
- Documentation is extensive but confusing

---

## 5. AI-RELATED PAIN POINTS

### 5.1 AI as Afterthought

**Current State:**
- AI features bolted on as separate products
- Not integrated into core platform
- "AI Cloud" is marketing, not architecture

### 5.2 Data Quality for AI

**Key Problems:**
- "40% don't trust AI/ML outputs"
- "45% cite data quality as obstacle to AI success"
- No native data quality checks

### 5.3 LLM Integration Gaps

**Current Issues:**
- True NL-to-SQL has ~70-80% accuracy (not production-ready)
- Complex for LLMs to understand schemas
- Cost management for LLM queries is unclear

---

## 6. SUMMARY OF CORE PROBLEMS

| Problem Category | Pain Level | Frequency |
|-----------------|------------|-----------|
| Cost complexity/unpredictability | HIGH | Very Common |
| AI as afterthought | HIGH | Universal |
| Limited customization | MEDIUM | Common |
| Real-time gaps | MEDIUM | Common |
| Data quality gaps | HIGH | Universal |
| Developer experience | MEDIUM-HIGH | Common |
| Vendor lock-in | MEDIUM | Common |
| Tool sprawl | MEDIUM | Common |
| Cross-cloud complexity | MEDIUM | Common |

---

## 7. OPPORTUNITIES FOR NEW ENTRANT

### 7.1 Problems to Solve

1. **Cost Transparency**: Predictable, understandable pricing
2. **AI-Native**: AI built into core, not bolted on
3. **True Multi-Cloud**: Seamless experience across clouds
4. **Developer Joy**: Modern UX, APIs, CLI
5. **Data Quality Core**: Native quality monitoring
6. **Open Standards**: No lock-in, portable data

### 7.2 What Would Make Users Switch

From user feedback:
- "50% cost reduction for comparable performance"
- "Actually working AI features"
- "Better developer experience"
- "True real-time"
- "No vendor lock-in"

---

*Research Sources: Reddit r/dataengineering, r/BigData, Hacker News, Monte Carlo Blog, Industry Reports*
*Date: 2026-02-21*
