# Parallel Execution Strategy

**Key Insight**: Population generation (slow, bulk) and Ontology design (fast, creative) can run **in parallel**.

---

## The Split

### 🖥️ Background Process (Ollama on RTX 3090 Ti)
**Task**: WILL-009, WILL-010
**Agent**: Local Ollama via Tailscale
**Duration**: Hours to days (depending on batch size)

```bash
# SSH to PC with RTX 3090 Ti
# Start Population generator
# Let it run in background (tmux/screen session)

Generate NPCs:
  1,000 generated → Test ontology
  10,000 generated → Test quote flow
  100,000 generated → Test claim journey
  1,000,000 generated → Stress test
  10,000,000 generated → Production ready
```

**Progress tracking**:
```sql
SELECT COUNT(*) FROM customers;  -- Check progress anytime
```

### 🧠 Foreground Work (Claude + Peter)
**Tasks**: WILL-012, WILL-013, WILL-024
**Agent**: Claude Code (Sonnet 4.5)
**Duration**: Few hours to days

```cypher
Design Pet Claims ontology:
  - Customer → Pet → Quote → Policy → Claim nodes
  - Relationships and properties
  - Constraints and indexes

Implement journey:
  - Jerry finds Barry
  - Quote generation logic
  - Policy creation
  - Claim submission workflow

Test with sample NPCs:
  - Use first 100-1000 NPCs from Population DB
  - Validate data flows correctly
  - Iterate schema if needed
```

---

## Execution Timeline

### Day 1 (Session 1)
**Morning**:
- ✅ WILL-001: Reorganize files
- ✅ WILL-003: Start Docker containers
- ✅ WILL-007: SSH to bunny server
- ✅ WILL-008: Design Population schema

**Afternoon**:
- 🟡 WILL-009: Start Population generator (background)
- 🟡 WILL-012: Start designing Pet Claims ontology (foreground)

**Evening**:
- Population: 100K NPCs generated
- Ontology: Customer → Pet → Quote schema complete

### Day 2
**Morning**:
- Population: 500K NPCs (still running)
- 🟡 WILL-024: Validate Population schema against quote form
- 🟡 WILL-013: Implement Customer Journey in AuraDB

**Afternoon**:
- Population: 2M NPCs
- Test: Pull 100 random NPCs → Generate quotes → Validate

**Evening**:
- Population: 5M NPCs
- Customer Journey complete and tested

### Day 3+
- Population: 10M NPCs complete
- Ontology: Production ready
- Start MSSQL ingestion (WILL-014) if credentials available

---

## Why This Works

### 1. **No Waiting**
Don't need to wait for 10M NPCs to start building ontology. First 1K is enough to test schema.

### 2. **Fast Feedback Loop**
```
Generate 1K NPCs
   ↓
Test ontology with real data
   ↓
Find issues ("postcode format doesn't match quote form!")
   ↓
Fix Population generator
   ↓
Continue generating
```

### 3. **Resource Optimization**
- **RTX 3090 Ti**: Grinding Faker generation (GPU/CPU intensive)
- **Claude Sonnet 4.5**: Creative schema design (reasoning intensive)
- **No resource conflict**

### 4. **Incremental Validation**
| NPCs Generated | Validation Test |
|----------------|-----------------|
| 1,000 | Schema compatibility |
| 10,000 | Quote form field coverage |
| 100,000 | Quote generation at scale |
| 1,000,000 | Claim journey simulation |
| 10,000,000 | Stress test, production ready |

---

## Task Dependencies (Updated)

### Before (Sequential)
```
WILL-007 (SSH) → WILL-008 (Schema) → WILL-009 (Generator) → WILL-010 (10M) → WILL-012 (Ontology)
```
**Problem**: Must wait for all 10M NPCs before starting ontology.

### After (Parallel)
```
WILL-007 (SSH) → WILL-008 (Schema) → WILL-009 (Generator starts)
                                            ↓
                                       Background: 10M generation (WILL-010)
                                            ↓
                                       Foreground: WILL-012 (Ontology)
                                            ↓
                                       Test with first 1K NPCs
```
**Benefit**: Start ontology as soon as generator is running. Test incrementally.

---

## Communication Between Processes

### Population Generator → Ontology Design
```sql
-- Claude queries Population DB to check progress
SELECT COUNT(*) FROM customers;
SELECT COUNT(*) FROM pets;

-- Sample random NPCs for testing
SELECT * FROM customers ORDER BY RANDOM() LIMIT 100;
```

### Ontology → Population Validation
```cypher
// In AuraDB, track which NPCs have been tested
CREATE (npc:TestCustomer {
  population_id: 12345,
  tested_at: datetime(),
  quote_generated: true,
  policy_created: false
})
```

---

## Progress Tracking

### Population Generation (Postgres)
```bash
# SSH to bunny server
psql -U willow -d population

# Check progress
SELECT
  (SELECT COUNT(*) FROM customers) as customers,
  (SELECT COUNT(*) FROM pets) as pets,
  NOW() as checked_at;

# Estimated completion
SELECT
  COUNT(*) as generated,
  10000000 - COUNT(*) as remaining,
  EXTRACT(EPOCH FROM (NOW() - MIN(created_at))) / COUNT(*) * (10000000 - COUNT(*)) / 3600 as hours_remaining
FROM customers;
```

### Ontology Development (AuraDB)
```cypher
// Check node counts
MATCH (n) RETURN labels(n)[0] as type, count(n) as count ORDER BY count DESC;

// Check Pet Claims nodes
MATCH (c:Customer)-[:OWNS]->(p:Pet)-[:COVERED_BY]->(pol:Policy)
RETURN count(DISTINCT c) as customers_with_policies;
```

---

## Testing Strategy

### Phase 1: Schema Validation (First 100 NPCs)
```python
# Pull 100 NPCs from Population DB
customers = fetch_customers(limit=100)

# For each customer, attempt to:
for customer in customers:
    try:
        # Fill quote form fields
        quote_data = {
            'full_name': customer.full_name,
            'email': customer.email,
            # ... all fields from quote form
        }

        # Validate against schema
        validate_quote_form(quote_data)

    except ValidationError as e:
        print(f"Customer {customer.id} failed: {e}")
        # Fix Population generator
```

### Phase 2: Quote Flow (First 1K NPCs)
```python
# Generate quotes for 1K customers
for customer in fetch_customers(limit=1000):
    pet = customer.get_random_pet()
    quote = generate_quote(customer, pet)

    # Create nodes in AuraDB
    create_customer_node(customer)
    create_pet_node(pet)
    create_quote_node(quote)

# Verify in AuraDB
# MATCH (c:Customer)-[:REQUESTED]->(q:Quote)-[:FOR_PET]->(p:Pet)
# RETURN count(*) as quotes_generated;
```

### Phase 3: Customer Journey (First 10K NPCs)
```python
# Simulate full journey for 10K customers
for customer in fetch_customers(limit=10000):
    # Jerry finds Barry
    pet = create_pet_for_customer(customer)

    # Jerry requests quote
    quote = generate_quote(customer, pet)

    # 30% accept quote
    if random() < 0.3:
        policy = create_policy(quote)

        # 10% of policies lead to claims
        if random() < 0.1:
            claim = simulate_claim(pet, policy)
```

---

## Success Criteria

### Population Generation
- ✅ 10M customers with valid UK data
- ✅ 3M pets (30% ownership rate)
- ✅ All fields match quote form requirements
- ✅ Data distributions realistic (70% microchipped, etc.)

### Ontology Design
- ✅ Customer Journey nodes created (Customer → Pet → Quote → Policy → Claim)
- ✅ Relationships defined and tested
- ✅ Can ingest 100 NPCs successfully
- ✅ Quote generation works with real Population data
- ✅ Claim workflow functions end-to-end

---

## Risk Mitigation

### Risk: Population generator crashes at 5M
**Mitigation**:
- Use tmux/screen for persistence
- Checkpoint every 100K (save progress)
- Resume from last checkpoint

### Risk: Ontology schema doesn't match Population data
**Mitigation**:
- Test with first 100 NPCs immediately
- WILL-024 validates schema against quote form
- Adjust generator before reaching 1M

### Risk: Quote form adds new required field
**Mitigation**:
- Population schema includes all current fields
- WILL-024 validation catches gaps
- Can backfill data if needed (UPDATE customers SET...)

---

## Commands to Start

### Start Population Generator (Background)
```bash
# SSH to PC with RTX 3090 Ti
ssh peter@desktop-via-tailscale

# Start in tmux session
tmux new -s population

# Run generator
python3 generate_population.py --total 10000000 --batch 10000

# Detach: Ctrl+B, then D
# Reattach later: tmux attach -t population
```

### Start Ontology Design (Foreground)
```bash
# In Willow project
cd /Volumes/Delila/dev/Willow

# Work on WILL-012
python3 skills/query_my_tasks.py
# Shows: WILL-012 - Design Pet Claims sub-ontology

# Create schema file
nano schemas/pet-claims-ontology.cypher
```

---

## Monitoring Both Processes

### Dashboard Query
```bash
# Check both at once
echo "=== Population Progress ==="
ssh bunny@bunny "psql -U willow -d population -c 'SELECT COUNT(*) FROM customers;'"

echo "=== Ontology Progress ==="
python3 << EOF
from neo4j import GraphDatabase
import certifi, os
os.environ['SSL_CERT_FILE'] = certifi.where()
driver = GraphDatabase.driver("neo4j+s://e59298d2.databases.neo4j.io", auth=("neo4j", "c2U7h1mwvmYn2k2cr_Fp9EaUrZaLZdEQ3_Cawt6zvyU"))
with driver.session() as session:
    result = session.run("MATCH (n) WHERE n:Customer OR n:Pet OR n:Quote RETURN labels(n)[0] as type, count(n) as count")
    for record in result:
        print(f"{record['type']}: {record['count']}")
driver.close()
EOF
```

---

## Next Session Checklist

**Before starting ontology work:**
- [ ] WILL-001: Reorganize files ✓
- [ ] WILL-003: Start containers ✓
- [ ] WILL-007: SSH to bunny ✓
- [ ] WILL-008: Design Population schema ✓
- [ ] WILL-009: START Population generator (background)

**Then immediately:**
- [ ] WILL-012: Design Pet Claims ontology (foreground)
- [ ] WILL-024: Validate first 100 NPCs against quote form

**No waiting required!** 🚀

---

**Built**: December 21, 2025
**Strategy**: Parallel execution for maximum efficiency
**Status**: Ready to execute 🌳
