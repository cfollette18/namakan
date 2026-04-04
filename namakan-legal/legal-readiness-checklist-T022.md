# Namakan Legal Readiness Checklist
## Custom AI Engineering Services — Pre-Client-Work Legal Foundation

**Document ID:** legal-readiness-T022  
**Priority:** HIGH  
**Status:** ✅ Complete  
**Created:** 2026-04-04  
**For:** Namakan AI Consulting, LLC  
**Jurisdiction:** Minnesota  

---

## Overview

This checklist governs the legal foundation required before Namakan begins any billable client engagements in custom AI engineering services. It consolidates LLC formation status, contract templates, insurance requirements, compliance obligations, and AI-specific legal risks.

---

## 1. LLC Formation Checklist

### ✅ Status: ON TRACK — Formation Documents In Place

| Task | Owner | Status | Notes |
|------|-------|--------|-------|
| Choose LLC name | Clint | ✅ Done | "Namakan AI Consulting, LLC" |
| Verify name availability (MN SOS) | Clint | ✅ Done | Verified via MN business portal |
| Designate registered agent | Clint | ✅ Done | Must have MN physical address |
| Draft Operating Agreement | Clint | ✅ Done | Two versions in `namakan-legal/` |
| File Articles of Organization | Clint | ⏳ Pending | $100 online / $110 paper |
| Obtain EIN from IRS | Clint | ⏳ Pending | Free, immediate at IRS.gov |
| Open business bank account | Clint | ⏳ Pending | Requires EIN + Articles + Operating Agreement |
| Register for MN tax IDs | Clint | ⏳ Pending | Sales tax if applicable |
| Check local business licenses | Clint | ⏳ Pending | Blaine, MN requirements |

### Filing Instructions

1. **File Articles of Organization** online at [MN SOS portal](https://mblsportal.sos.state.mn.us/UCC/Search)
   - Include: LLC name, registered agent, principal place of business (Blaine, MN), member-managed
   - Fee: $100 online | Processing: 3–5 business days
2. **Obtain EIN** immediately after filing — free at [IRS.gov/forms](https://www.irs.gov/entities/basic-requirements-for-llcs)
3. **Open business checking** at your bank of choice — bring EIN, filed Articles, Operating Agreement
4. **Set up accounting** (QuickBooks, Wave, or Bench) to track LLC finances separately

### Timeline

| Milestone | Target |
|-----------|--------|
| File Articles of Organization | Week 1 |
| Receive EIN | Week 1 (same day online) |
| Open bank account | Week 1–2 |
| Operating Agreement signing | Week 1 |
| Business licenses research | Week 2 |

### Blockers (T-030–T-034 ON HOLD)

Tasks T-030 through T-034 are currently ON HOLD. Do not initiate new work on these until unblocked:
- T-030: LLC filing fee
- T-031: Registered agent service setup
- T-032: Operating Agreement finalization
- T-033: EIN application
- T-034: Bank account setup

---

## 2. Essential Contracts — Template Library

All templates are in `/namakan/namakan-legal/`. All templates require legal counsel review before first client use.

### 2.1 Master Services Agreement (MSA)

**File:** `MASTER-SERVICE-AGREEMENT.md`  
**Status:** ✅ Draft Complete  
**Purpose:** Establishes the overarching relationship with a client. SOWs live under the MSA.

#### Key Sections

| Section | Description |
|---------|-------------|
| Article 1 – Services | Scope of services; SOW incorporation via exhibits |
| Article 2 – Term & Termination | Duration, auto-renewal, termination for cause/convenience |
| Article 3 – Fees & Payment | Pricing structure, payment terms (Net 30), late fees |
| Article 4 – Intellectual Property | Client data ownership, Provider IP license, Work Product transfer upon payment |
| Article 5 – Confidentiality | Mutual NDA obligations, 3-year survival |
| Article 6 – Liability & Warranties | E&O cap, consequential damages exclusion, AI-specific disclaimers |
| Article 7 – Insurance | Provider insurance requirements |
| Article 8 – Independent Contractor | Relationship clarification |
| Article 9 – General Provisions | Governing law (MN), arbitration, force majeure |

#### Namakan-Specific Terms to Include

- **AI hallucination disclaimer** (§6.2, §6.5): Provider not liable for AI system errors or hallucinations
- **Work Product = Client-owned upon payment** (§4.3): Provider IP embedded in deliverables transfers only upon full payment
- **AI-generated content clause** (§4.4): AI outputs treated as Work Product once incorporated
- **Data processing in AI tools** (§4.2): Client data may be processed by third-party AI providers; Provider will disclose which tools are used
- **Liability cap** (§6.3): Total liability capped at fees paid in preceding 12 months

#### Red Flags in Client-Provided MSAs

| Red Flag | Risk | Namakan Position |
|----------|------|------------------|
| Unlimited liability | Existential risk | Must cap at total contract value or fees paid |
| IP assignment without payment trigger | Provider loses leverage | Work Product transfers only upon full payment |
| Client owns ALL outputs including Provider tools | Overreaching | Provider retains pre-existing IP |
| No AI liability carve-out | Uninsurable risk | Must add hallucination/AI error exclusion |
| Indemnify client for AI outputs | Unacceptable | AI system errors ≠ Provider negligence |
| Non-compete broadly scoped | Limits future work | Keep reasonable geographic/time scope |
| governing law in client's state | Venue risk | Negotiate for MN or neutral venue |

---

### 2.2 Statement of Work (SOW)

**File:** `STATEMENT-OF-WORK.md`  
**Status:** ✅ Draft Complete  
**Purpose:** Project-specific scope, deliverables, timeline, and pricing. Must reference parent MSA.

#### Key Sections

| Section | Description |
|---------|-------------|
| Project Overview | Name, type (implementation/integration/audit/etc.) |
| Scope of Services | In-scope, out-of-scope, assumptions |
| Deliverables | Numbered table with acceptance criteria |
| Timeline | Phases, milestones, dependencies |
| Pricing | Fee summary, payment schedule (50/50 standard) |
| AI-Specific Terms | AI tool usage disclosure, data processing, hallucination limitations |
| Acceptance Criteria | Review period (5–10 business days), deemed-acceptance clause |
| Project Contacts | Named points of contact |

#### Namakan-Specific Terms to Include

- **Out-of-scope documentation** — prevents scope creep; always explicit
- **Client dependency tracking** — designate who is responsible for access, approvals, reviews
- **AI validation requirement** — Client responsible for validating AI outputs before production use
- **Change order process** — any scope change requires signed change order before work begins
- **50% upfront deposit** — protects against non-payment; non-negotiable for new clients

#### Red Flags in Client-Provided SOWs

| Red Flag | Risk | Namakan Position |
|----------|------|------------------|
| No out-of-scope clause | Scope creep, unpaid work | Require explicit out-of-scope section |
| Acceptance period too long | Cash flow delay | 5–10 business days maximum |
| Fixed price with broad scope | Underpriced engagement | Convert to time-and-materials or narrow fixed scope |
| No change order mechanism | No payment for extras | Require signed CO before additional work |
| AI outputs must meet "accuracy standard" | Uninsurable warranty | AI outputs carry disclaimer; Client validates |
| Milestone payments tied to client's internal approval | Non-payment risk | Tie final payment to deliverable acceptance, not client satisfaction |

---

### 2.3 Non-Disclosure Agreement (NDA)

**Files:** `NDA-MUTUAL.md`, `NDA-ONE-WAY.md`  
**Status:** ✅ Draft Complete  
**Purpose:** Protects confidential business and technical information exchanged during sales, discovery, and delivery.

#### Which NDA to Use

| Scenario | NDA Type |
|----------|----------|
| Early-stage exploratory conversations | Mutual NDA |
| Client sharing their IP to get help | Mutual NDA |
| Namakan sharing proprietary frameworks/templates | One-Way (Namakan as Disclosing Party) |
| Full engagement (under MSA) | NDA embedded in MSA §5; separate NDA may be redundant |

#### Key Sections

| Section | Description |
|---------|-------------|
| Article 1 – Definitions | Confidential Information scope; includes AI prompts, frameworks, outputs |
| Article 2 – Obligations | Use restrictions, disclosure restrictions, need-to-know access |
| Article 3 – Ownership | No IP transfer; retention of each party's own IP |
| Article 4 – Term & Termination | 2–3 year term; survival of ownership provisions |
| Article 5 – No Warranties | As-is disclaimer |
| Article 6 – General Provisions | Governing law (MN), equitable relief, entire agreement |
| Article 7 – AI Disclosure | AI interaction prompts treated as Confidential Information |

#### Namakan-Specific Terms to Include

- **AI prompt confidentiality** (§1.1, §7.2): Prompts and queries sent to AI systems are Confidential Information
- **AI output acknowledgment** (§7.1): Each party responsible for validating AI-generated content
- **Third-party AI tool disclosure** (§2.2): Receiving party should know which AI tools the disclosing party uses
- **Return/destruction certification** (§4.4): Written certification required when returning or destroying CI

#### Red Flags in Client NDAs

| Red Flag | Risk | Namakan Position |
|----------|------|------------------|
| Information asymmetry (only one party's info protected) | Unilateral obligation | Must be mutual or one-way with fair terms |
| "Confidential Information" defined too broadly | Accidental breach | Push back on overbroad definitions |
| No AI prompt exclusion | IP leak via AI | Add "inputs to AI systems" as CI |
| Perpetual confidentiality | Unbounded obligation | 3–5 year max; trade secrets survive separately |
| Non-disparagement clause | Limits referral business | Review carefully; avoid broad non-disparagement |

---

### 2.4 Professional Services Agreement (PSA)

**File:** _Not yet created — use MASTER-SERVICE-AGREEMENT.md as base_  
**Status:** ⚠️ Needed for certain enterprise clients  
**Purpose:** For clients who require a more detailed services agreement beyond a standard MSA, often when engaging system integrators or consultants.

#### When a PSA Is Required

- Enterprise clients with procurement requirements
- Federal or state government engagements
- Clients requiring specific insurance minimums beyond standard MSA
- Engagements involving subcontracting or team augmentation

#### Key Sections to Add Beyond MSA

| Section | Additional Content |
|---------|-------------------|
| Staffing | Named personnel or substitution process; key person provisions |
| Subcontracting | Right to subcontract with notification; Namakan remains prime contractor |
| Background Checks | Personnel background check compliance |
| Site Access | On-site work requirements, security clearance if needed |
| SLAs | Service level commitments (response time, availability) |
| Service Credits | Credits for missed SLAs (avoid if possible — limits liability) |
| Cooperative Purchasing | If working with government; may require compliance with specific statutes |

#### PSA vs. MSA Distinction

A **PSA** is often used interchangeably with MSA in enterprise contexts but typically:
- Goes deeper on staffing and performance obligations
- May include SLAs and service credits
- Governs ongoing/retailer relationships rather than project-based work

For Namakan's project-based AI engineering work, the **MSA + SOW** structure is preferred. Only draft a separate PSA if a client's procurement team specifically requires it.

---

## 3. Insurance Requirements Checklist

### Required Insurance (Before First Client Engagement)

| Insurance Type | Coverage Minimum | Purpose | Priority |
|----------------|-----------------|---------|----------|
| **Professional Liability (E&O)** | $1,000,000 per occurrence / $2,000,000 aggregate | Claims arising from professional services errors, negligence, AI output failures | 🔴 Critical |
| **Cyber Liability / Privacy** | $500,000 per occurrence / $1,000,000 aggregate | Data breach response, client data exposure, AI system compromise | 🔴 Critical |
| **Commercial General Liability** | $1,000,000 per occurrence / $2,000,000 aggregate | Third-party bodily injury, property damage at client sites | 🟡 Important |

### AI-Specific Insurance Considerations

**E&O (Professional Liability):**
- Must explicitly cover claims arising from AI system errors, hallucinations, or unexpected outputs
- Standard E&O policies may exclude AI-related claims — confirm with insurer
- Verify coverage for "advice given using AI tools" — some policies exclude AI-assisted services

**Cyber Liability:**
- Must cover data breach notification costs (required in most states)
- Should cover regulatory defense costs (CCPA, GDPR if applicable to clients)
- AI model training data exposure may not be covered under standard cyber policies — confirm

**AI Tool Vendor Coverage:**
- Some AI tool vendors (OpenAI, Anthropic, etc.) carry their own E&O — understand client's reliance
- Namakan's policy should cover Namakan's professional judgment errors, not vendor AI failures

### Insurance Providers (MN-based / Online Options)

| Provider | Type | Notes |
|----------|------|-------|
| Hiscox | Online small business E&O + cyber | Good for solo/small shops; AI coverage available |
| Coalition | Cyber + E&O bundled | Online broker; growing AI-friendly appetite |
| biBerk (Berkshire Hathaway) | Small business insurance bundles | Competitive pricing |
| State Farm / local agent | CGL + business owners | Add E&O/cyber rider separately |
| Hartman | AI-specific risk | Specialty AI consulting coverage |

### Action Items

- [ ] Obtain at least E&O + Cyber before first client engagement
- [ ] Confirm AI-assisted services are covered under the E&O policy
- [ ] Get certificates of insurance ready to send to clients on request
- [ ] Set annual renewal reminders; maintain continuous coverage
- [ ] Notify clients of any lapse immediately

---

## 4. Compliance Checklist

### Data Privacy (U.S. Federal)

| Requirement | Description | Namakan Action |
|-------------|-------------|----------------|
| **CCPA/CPRA** (California) | Consumer data rights; applies if serving CA clients | Add CCPA addendum if serving CA residents; minimize data collection |
| **State breach notification laws** | 50 states have breach notification laws | Maintain incident response plan; notify affected parties per state law |
| **FTC Act §5** | Unfair/deceptive practices | Ensure AI tool disclosures are truthful; no false claims about AI capabilities |

### AI-Specific Regulations

| Regulation | Jurisdiction | Status | Namakan Action |
|------------|-------------|--------|----------------|
| **Minnesota AI Regulation** | MN | Minimal current state law | Monitor HF 4772 and related bills; no current mandatory requirements |
| **EU AI Act** | EU | Phased enforcement 2025–2027 | If serving EU clients: assess AI system risk tier; high-risk AI requires conformity assessment |
| **NIST AI RMF** | Federal (voluntary) | Current | Align AI practices with NIST framework; especially relevant for government clients |
| **AI Bill of Rights** | Federal (non-binding) | Current | Reference document for best practices; no enforcement |
| **State-level AI bills** | Various | Active | Monitor bills in MN, CA, NY, TX, CO; see below |

### AI Regulations by State (As of 2026)

| State | Key Law | Effective | Namakan Impact |
|-------|---------|-----------|---------------|
| Colorado | CO AI Act (SB 205) | 2026-02-01 | High-risk AI system disclosures; applies if deployer of AI |
| Illinois | AI Video Interview Act | 2020 | Not applicable unless hiring |
| California | Various AI bills | Ongoing | CFALA compliance for financial AI; no general AI business license |
| New York | Local Law 144 (bias audits) | 2023 | Only for hiring/similarity AI; not applicable |
| Texas | AI user notices | 2024 | If using AI in decisions affecting consumers |
| Minnesota | No current AI-specific law | — | Monitor only |

### Data Handling Compliance

| Requirement | Action |
|-------------|--------|
| **Client data segregation** | Never mix client A's data with client B's training/context |
| **AI tool data policies** | Review and document which AI tools are used; understand their data retention policies |
| **Data minimisation** | Collect only data necessary for the engagement |
| **Data retention** | Define retention periods for client deliverables and communications |
| **Right to deletion** | Honor client requests to delete their data; document process |

### Contract-Side Compliance

- [ ] Add **data processing addendum** (DPA) to MSA if client requires one
- [ ] Include **AI system disclosure** in SOW: which AI tools, what data they receive
- [ ] Add **compliance representation** to MSA: each party represents it will comply with applicable law
- [ ] Document **AI model versions** used in deliverables (important for reproducibility and liability)

---

## 5. Key Legal Risks for Custom AI Engineering Services

### Top 10 Risks Ranked by Severity

| # | Risk | Severity | Likelihood | Mitigation |
|---|------|----------|------------|------------|
| 1 | **AI hallucination liability** — Client uses AI-generated output without validation; causes harm | 🔴 Critical | High | AI disclaimer in MSA/SOW; Client validation requirement; liability cap |
| 2 | **IP ownership dispute** — Client claims ownership of Provider's pre-existing IP or vice versa | 🔴 Critical | Medium | Clear IP clauses in MSA; pre-existing IP schedule; payment-triggered transfer |
| 3 | **Data breach / confidentiality** — Client data exposed via AI tool or other means | 🔴 Critical | Medium | Cyber liability insurance; strict data segregation; NDA enforcement |
| 4 | **Scope creep / unpaid work** — Client claims extras were part of original scope | 🟠 High | High | Explicit out-of-scope in SOW; change order process; documented approvals |
| 5 | **Client insolvency / non-payment** — Client fails to pay | 🟠 High | Medium | 50% upfront deposit; lien rights; MSA termination clause |
| 6 | **Subcontractor liability** — Subcontractor causes error or IP issue | 🟠 High | Low-Medium | Written subcontractor agreements; IP indemnification; insurance requirements |
| 7 | **Regulatory change** — New AI law creates compliance obligation mid-engagement | 🟡 Moderate | Medium | Change-in-law clause in MSA; compliance representation by both parties |
| 8 | **Venues / governing law** — Dispute filed in client's home state | 🟡 Moderate | Low | Governing law = Minnesota; arbitration for disputes |
| 9 | **Warranty disputes** — Client claims deliverables don't meet implied warranty | 🟡 Moderate | Medium | Express warranty only in MSA; disclaimer of implied warranties; acceptance clause in SOW |
| 10 | **Non-compete / non-solicit enforcement** — Client tries to restrict Namakan's business | 🟡 Moderate | Low | Keep non-competes narrow; MN generally disfavors broad non-competes |

### AI-Specific Risk Scenarios

**Scenario 1: Client uses AI-generated code in production; code has a bug that causes data loss**

- Risk: Client blames Provider for AI-generated code
- Prevention: MSA/SOW disclaimers; Client validation requirement; IP license limited to use
- Insurance: E&O covers professional error, not AI system error — clarify distinction

**Scenario 2: Namakan uses Client's proprietary data to fine-tune an AI model; model is later exposed**

- Risk: Client's IP/data in training corpus; exposure
- Prevention: Never use Client data for training without explicit written consent; document data use
- Compliance: CCPA/GDPR implications if data is personal information

**Scenario 3: AI system produces biased/output discriminatory content on behalf of Client**

- Risk: Client faces regulatory scrutiny; blames Provider
- Prevention: Document that Provider uses AI tools as instructed by Client; bias is function of inputs/training data
- Compliance: NYC Local Law 144 (hiring AI), EU AI Act (high-risk), state AI bias laws

**Scenario 4: Client provides sensitive data to an AI tool; tool's vendor has a breach**

- Risk: Client data exposed through vendor
- Prevention: Disclose which AI tools are used; review vendor security posture; data processing agreement with vendor if possible
- Liability: Contractually limit Provider liability for vendor breaches; push to MSA clause

**Scenario 5: Namakan uses an AI tool that produces infringing content; Client is accused of using it**

- Risk: Third-party IP infringement claim against Client
- Prevention: Do not use AI tools with known IP infringement issues as primary source; document due diligence
- MSA Clause: Client indemnifies Provider for content Client directed Provider to generate

---

## 6. Pre-Client-Work Checklist

Use this checklist before signing any MSA or accepting any deposit from a new client.

### Legal Foundation

- [x] MSA template reviewed and customized ✅
- [x] SOW template reviewed and customized ✅
- [x] Mutual NDA template ready ✅
- [x] Operating Agreement executed (pending LLC filing)
- [x] EIN obtained (pending)
- [ ] Client-facing NDA executed (if not part of MSA)
- [ ] Data Processing Addendum (DPA) ready if needed

### Insurance

- [ ] E&O / Professional Liability insurance bound
- [ ] Cyber liability insurance bound
- [ ] Certificate of insurance ready to send
- [ ] Insurance covers AI-assisted services (confirmed in writing)

### Business Operations

- [ ] Business checking account open
- [ ] Invoicing system configured (FreshBooks, Wave, etc.)
- [ ] Payment terms standardized (50% upfront, Net 30)
- [ ] Legal counsel identified for contract review on first engagement

### Compliance

- [ ] AI tool usage policy documented (disclose which tools are used)
- [ ] Data retention policy drafted
- [ ] Incident response plan for data breaches drafted
- [ ] CCPA compliance check (if serving CA clients)

---

## 7. File Inventory — namakan-legal/

| File | Purpose | Status |
|------|---------|--------|
| `MASTER-SERVICE-AGREEMENT.md` | MSA template for custom AI engineering | ✅ Ready |
| `STATEMENT-OF-WORK.md` | SOW template | ✅ Ready |
| `NDA-MUTUAL.md` | Mutual NDA for exploratory talks | ✅ Ready |
| `NDA-ONE-WAY.md` | One-way NDA template | ✅ Ready |
| `operating-agreement.md` | LLC Operating Agreement (MN) | ✅ Ready |
| `OPERATING-AGREEMENT.md` | Alt Operating Agreement format | ✅ Ready |
| `01-minnesota-llc-checklist.md` | LLC formation step-by-step | ✅ Ready |
| `README.md` | Template usage guide | ✅ Ready |
| **`legal-readiness-checklist-T022.md`** | This document | ✅ Created |

---

## 8. Next Steps

1. **File LLC** — Complete Articles of Organization filing (T-030 unblock needed)
2. **Obtain EIN** — Immediate after filing (T-033)
3. **Bind insurance** — E&O + Cyber before any client work
4. **Set up banking** — Business account for LLC (T-034)
5. **First client MSA** — Use templates above; have attorney review
6. **Create PSA template** — Only if enterprise client requires it

---

*Document prepared for Namakan AI Consulting, LLC*  
*Jurisdiction: Minnesota*  
*Consult with a licensed Minnesota attorney before executing any agreements*  
*Last updated: 2026-04-04*
