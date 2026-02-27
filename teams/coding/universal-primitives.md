# UNIVERSAL DATA PRIMITIVES FOR CROSS-DOMAIN DATA CLOUD

**Date:** 2026-02-14  
**Author:** Team Lead (informed by Zeta research)  
**Purpose:** Define the foundational abstractions that work across all domains (marketing, engineering, healthcare, finance, etc.)

## CORE INSIGHT

Every domain works with data, but each has specialized models. The universal data cloud needs **abstractions that capture what's common** while allowing **domain-specific extensions**. 

Think: "Every domain has entities, relationships, and events - they just call them different names."

## THE FIVE UNIVERSAL PRIMITIVES

### 1. **ENTITY** - The "Things" in Your Domain
**What it is:** Any identifiable object or concept that data describes.

**Domain Examples:**
- **Marketing:** Customer, Campaign, Product
- **Engineering:** Service, Deployment, Incident
- **Healthcare:** Patient, Provider, Treatment
- **Finance:** Account, Transaction, Instrument
- **Generic:** User, Organization, Asset

**Universal Properties:**
- `id`: Unique identifier (domain-specific format)
- `type`: Entity type (customer, patient, service, etc.)
- `attributes`: Key-value properties
- `created_at`, `updated_at`: Timestamps
- `domain_metadata`: Domain-specific extensions

**Implementation Approach:**
```typescript
interface UniversalEntity {
  id: string;
  type: string;  // e.g., "customer", "patient", "service"
  domain: string; // e.g., "marketing", "healthcare", "engineering"
  attributes: Record<string, any>;
  relationships: EntityRelationship[];
  timestamps: {
    created_at: DateTime;
    updated_at: DateTime;
    valid_from?: DateTime; // For temporal data
    valid_to?: DateTime;
  };
  domain_extensions: Record<string, any>; // HIPAA fields, financial regulations, etc.
}
```

### 2. **RELATIONSHIP** - How Entities Connect
**What it is:** Connections between entities with semantic meaning.

**Domain Examples:**
- **Marketing:** Customer `PURCHASED` Product, Customer `ENGAGED_WITH` Campaign
- **Engineering:** Service `DEPENDS_ON` Service, Incident `AFFECTED` Deployment
- **Healthcare:** Patient `RECEIVED` Treatment, Provider `PRESCRIBED` Medication
- **Finance:** Account `OWNS` Instrument, Transaction `TRANSFERRED` Funds

**Universal Properties:**
- `source_entity`: The "from" entity
- `target_entity`: The "to" entity  
- `relationship_type`: Semantic label (PURCHASED, DEPENDS_ON, etc.)
- `strength`/`confidence`: For probabilistic relationships
- `temporal_context`: When the relationship was valid

**Implementation Approach:**
```typescript
interface UniversalRelationship {
  id: string;
  source_entity_id: string;
  target_entity_id: string;
  type: string; // Domain-specific relationship type
  attributes: Record<string, any>; // e.g., purchase_amount, dependency_criticality
  domain: string; // Which domain this relationship belongs to
  graph_properties: {
    directed: boolean;
    weight?: number;
    metadata?: Record<string, any>;
  };
}
```

### 3. **EVENT** - Things That Happen Over Time
**What it is:** Something that occurs at a specific point in time, often changing entity state.

**Domain Examples:**
- **Marketing:** Customer clicked email, Purchase completed
- **Engineering:** Deployment started, Error logged, Incident resolved
- **Healthcare:** Appointment scheduled, Medication administered, Test result received
- **Finance:** Trade executed, Payment processed, Risk alert triggered

**Universal Properties:**
- `event_type`: What happened
- `entity_id`: Which entity was involved
- `timestamp`: When it happened
- `payload`: Event-specific data
- `source`: Where the event came from

**Implementation Approach:**
```typescript
interface UniversalEvent {
  id: string;
  type: string; // e.g., "purchase", "deployment", "appointment"
  entity_id: string; // Which entity this event relates to
  timestamp: DateTime;
  payload: Record<string, any>;
  source: {
    system: string; // e.g., "salesforce", "github", "epic"
    connector_id: string;
  };
  domain: string;
  // For event sourcing/stream processing
  sequence_number?: number;
  correlation_id?: string; // For tracing across systems
}
```

### 4. **ATTRIBUTE** - Properties and Measurements
**What it is:** Characteristics, measurements, or properties of entities.

**Domain Examples:**
- **Marketing:** Customer lifetime value, Engagement score
- **Engineering:** Error rate, Response time, Uptime percentage
- **Healthcare:** Blood pressure, Lab results, Diagnosis codes
- **Finance:** Account balance, Risk score, Volatility measure

**Universal Properties:**
- `name`: Attribute identifier
- `value`: Current value (typed)
- `data_type`: string, number, boolean, datetime, etc.
- `unit_of_measure`: For quantitative attributes
- `validity_period`: When this value was accurate

**Implementation Approach:**
```typescript
interface UniversalAttribute {
  entity_id: string;
  name: string;
  value: any;
  data_type: 'string' | 'number' | 'boolean' | 'datetime' | 'object' | 'array';
  metadata: {
    unit?: string; // e.g., "USD", "mmHg", "ms"
    precision?: number;
    confidence?: number; // For derived/estimated values
    source?: string; // How this value was determined
  };
  temporal: {
    valid_from: DateTime;
    valid_to?: DateTime; // For historical values
    observed_at: DateTime; // When we learned this value
  };
}
```

### 5. **CONTEXT** - Domain-Specific Meaning
**What it is:** The semantic framework that gives data meaning within a domain.

**Domain Examples:**
- **Marketing:** Campaign taxonomy, Customer segments, Channel definitions
- **Engineering:** Service taxonomy, Severity levels, Environment definitions
- **Healthcare:** ICD-10 codes, LOINC codes, Drug classifications
- **Finance:** Instrument classifications, Risk categories, Regulatory frameworks

**Universal Properties:**
- `context_type`: What kind of context (taxonomy, ontology, schema)
- `domain`: Which domain this applies to
- `version`: Context evolves over time
- `mappings`: How this context relates to other contexts
- `rules`: Domain-specific business rules

**Implementation Approach:**
```typescript
interface UniversalContext {
  id: string;
  type: 'taxonomy' | 'ontology' | 'schema' | 'classification' | 'regulation';
  domain: string;
  version: string;
  name: string; // e.g., "ICD-10", "Service Catalog", "Product Taxonomy"
  elements: Record<string, any>; // The actual context definitions
  mappings: {
    to_other_contexts: Array<{
      context_id: string;
      mapping_rules: any[];
    }>;
  };
  // For AI understanding
  natural_language_descriptions?: Record<string, string>;
  synonyms?: Record<string, string[]>;
}
```

## DOMAIN PLUGIN ARCHITECTURE

### How Domains Extend Universal Primitives:

```
Universal Primitive Layer
    ↓
[Domain Plugin System]
    ↓
Marketing Plugin      Engineering Plugin     Healthcare Plugin     Finance Plugin
- Customer entity     - Service entity       - Patient entity      - Account entity
- Purchase event      - Deployment event     - Treatment event     - Transaction event
- Campaign context    - Incident context     - ICD-10 context      - FINRA context
```

### Plugin Components:
1. **Entity Types:** Domain-specific entity definitions
2. **Relationship Types:** Domain-specific relationship semantics
3. **Event Schemas:** Domain-specific event structures
4. **Context Definitions:** Domain taxonomies and ontologies
5. **Compliance Rules:** Domain regulations (HIPAA, FINRA, etc.)
6. **UI Components:** Domain-specific visualizations and workflows

## QUERYING ACROSS DOMAINS

### Universal Query Language:
```sql
-- Marketing query
FIND Customers 
WHERE last_purchase_date > '2024-01-01' 
AND total_spent > 1000

-- Engineering query  
FIND Services
WHERE error_rate > 0.01 
IN LAST 24 HOURS

-- Cross-domain query (the magic!)
FIND Entities
WHERE type IN ('Customer', 'Patient', 'Account')
AND created_this_month = true
-- Platform understands these are similar concepts across domains
```

### Natural Language Understanding:
- **User:** "Show me high-value customers"
- **AI:** Understands "high-value" means different things in different domains
  - Marketing: Lifetime value > $10,000
  - Healthcare: Patients with complex chronic conditions
  - Finance: Accounts with > $1M balance
- **Response:** Domain-appropriate interpretation based on context

## IMPLEMENTATION STRATEGY

### Phase 1: Universal Core
1. Implement the 5 universal primitives
2. Basic entity-relationship graph database
3. Simple query engine for universal queries

### Phase 2: Domain Plugins
1. Marketing plugin (learn from Zeta)
2. Engineering plugin (logs, metrics, deployments)
3. Healthcare plugin (patients, treatments, compliance)
4. Finance plugin (accounts, transactions, regulations)

### Phase 3: Cross-Domain Intelligence
1. AI that understands domain context
2. Cross-domain relationship discovery
3. Universal insights generation

## KEY INNOVATIONS

### 1. **Domain-Aware Type System**
- Entities have both universal and domain-specific types
- Type inheritance: `Patient` is-a `Entity` with healthcare extensions
- Dynamic type checking based on domain context

### 2. **Context-Preserving Queries**
- Queries remember which domain they're in
- Automatic domain inference when possible
- Clear context switching when needed

### 3. **Pluggable Compliance**
- Each domain plugin brings its compliance rules
- Universal compliance engine enforces rules
- Audit trails for cross-domain compliance

### 4. **Progressive Domain Learning**
- Platform learns new domains from usage
- Few-shot learning for domain-specific concepts
- Community-contributed domain plugins

## CONCLUSION

The universal data cloud needs **abstractions, not specialization**. By identifying the five universal primitives (Entity, Relationship, Event, Attribute, Context), we can build a platform that works for any domain while maintaining the simplicity and magic that users expect.

**Think different:** Instead of building "Zeta for healthcare" and "Zeta for engineering" separately, we build **one platform** that understands all domains through a common lens.

---
**Next:** Incorporate these primitives into the revised architecture plan