# Population Developer - Task Guide

**Date:** 22 December 2025  
**Agent:** Population Developer (Running on Frank)  
**Priority:** High

## 📧 Message Received from Captain

> Database audit complete - Action required
> 
> GOOD NEWS: Your new Purely Pets schema works perfectly (100 customers, 24 pets, proper UK data).  
> BAD NEWS: Found legacy `people` table with 3.4M records using old schema.  
> 
> Recommend:
> 1. Drop old tables (people/quotes/policies/claims)
> 2. Scale NEW schema (customers/pets) to target volumes
> 3. Implement quote generation

## 📊 Current Database State (Bunny)

```
 table_name |  count  
------------+---------
 customers  |     100  ✅ NEW schema (Purely Pets)
 pets       |      24  ✅ NEW schema (Purely Pets)
 quotes     |       0  ⚠️  Empty - needs generation
 people     | 3426400  ❌ OLD schema (legacy)
```

## ✅ Action Plan

### Phase 1: Clean Up Legacy Schema (15 minutes)
**Status:** Ready to execute  
**Risk:** Low (old data, can be archived if needed)

1. **Backup old data** (optional but recommended):
   ```bash
   ssh bunny@bunny "docker exec willow-population-db pg_dump -U willow -d population -t people -t quotes -t policies -t claims > /tmp/legacy_backup_$(date +%Y%m%d).sql"
   ```

2. **Drop old tables**:
   ```bash
   ssh bunny@bunny "docker exec willow-population-db psql -U willow -d population -c 'DROP TABLE IF EXISTS people CASCADE; DROP TABLE IF EXISTS policies CASCADE; DROP TABLE IF EXISTS claims CASCADE;'"
   ```

3. **Verify cleanup**:
   ```bash
   ssh bunny@bunny "docker exec willow-population-db psql -U willow -d population -c '\dt'"
   ```

### Phase 2: Scale Population Data (30 minutes)
**Status:** Blocked by Faker Integration task completion  
**Current:** 100 customers, 24 pets  
**Target:** 10,000+ customers, 5,000+ pets

**Prerequisites:**
- Complete "Faker Integration" task (currently In Progress)
- Verify `domains/population/generator.py` or `remote_generator.py` can scale

**Approach:**
1. Review current generation script
2. Add batch processing capability
3. Run generation for target volume
4. Verify data quality (UK postcodes, realistic breeds, etc)

### Phase 3: Generate Quotes (45 minutes)
**Status:** Blocked by Phase 2  
**Dependencies:** Need customers and pets before generating quotes

**Requirements:**
- Each customer should have 1-3 quotes
- Quote fields: `customer_id`, `pet_id`, `cover_type`, `excess_amount`, `vet_fee_limit`, `premium_monthly`, `created_at`
- Cover types: 'Accident Only', 'Time Limited', 'Maximum Benefit', 'Lifetime'
- Realistic pricing based on pet type, age, pre-existing conditions

**Implementation:**
```python
# Pseudo-code for quote generation
for customer in customers:
    num_quotes = random.randint(1, 3)
    for _ in range(num_quotes):
        pet = random.choice(customer.pets)
        cover_type = random.choice(COVER_TYPES)
        premium = calculate_premium(pet, cover_type)
        create_quote(customer, pet, cover_type, premium)
```

## 📝 Next Steps for Population Developer

1. **Immediate (Today):** 
   - Drop legacy tables (Phase 1)
   - Send confirmation message to Captain

2. **This Week:**
   - Complete Faker Integration task
   - Scale to 10K customers (Phase 2)
   - Generate quotes (Phase 3)

3. **Log Progress:**
   ```python
   # Use Feature Agent to log work
   python core/agents/feature_agent.py "Population → Generator → [Task Name]"
   ```

## 🔗 Related Resources

- **Generator Location:** `domains/population/generator.py`, `domains/population/remote_generator.py`
- **Schema Spec:** `domains/population/specification.md`
- **Database Host:** Bunny (bunny@bunny)
- **Database Container:** willow-population-db
- **Connection:** `postgresql://willow:willowdev123@bunny:5432/population`

## 💬 Communication

**To send message back to Captain:**
```python
from neo4j import GraphDatabase

with driver.session() as session:
    session.run('''
        CREATE (m:Message {
            from: "Population Developer",
            to: "Captain (Chief Officer)",
            subject: "Legacy cleanup complete - Scaling in progress",
            body: "Dropped 3.4M legacy records. NEW schema confirmed working. Now scaling to 10K customers...",
            priority: "Medium",
            timestamp: datetime(),
            read: false
        })
    ''')
```
