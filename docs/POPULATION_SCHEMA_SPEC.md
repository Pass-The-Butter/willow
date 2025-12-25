# Population Schema Specification

## Reference: Purely Pets Insurance Quote Form
**URL**: https://quote.purelypetsinsurance.co.uk/

This document maps the quote form fields to our Population database schema, ensuring NPCs can autonomously flow through the customer journey.

---

## Customer Table (Population DB)

### Required Fields from Quote Form

| Field Name | Type | Faker Method | Example | Notes |
|------------|------|--------------|---------|-------|
| `full_name` | VARCHAR(255) | `fake.name()` | "Sarah Johnson" | First + Last name |
| `email` | VARCHAR(255) | `fake.email()` | "sarah.johnson@email.co.uk" | Unique |
| `phone_mobile` | VARCHAR(20) | `fake.phone_number()` | "07700 900123" | UK mobile format |
| `address_line_1` | VARCHAR(255) | `fake.street_address()` | "42 High Street" | Primary address |
| `address_line_2` | VARCHAR(255) | `fake.secondary_address()` | "Flat 3" | Optional |
| `city` | VARCHAR(100) | `fake.city()` | "Manchester" | UK cities |
| `postcode` | VARCHAR(10) | `fake.postcode()` | "M1 2AB" | UK postcode format |
| `date_of_birth` | DATE | `fake.date_of_birth(min_age=18, max_age=80)` | "1985-06-15" | For age verification |

### Additional Fields (Not on form, for system use)

| Field Name | Type | Purpose |
|------------|------|---------|
| `id` | SERIAL PRIMARY KEY | Unique identifier |
| `personality_vector` | VECTOR(384) | Embeddings for similarity search (cat lovers, allergies, etc.) |
| `created_at` | TIMESTAMP | When NPC was generated |
| `is_active` | BOOLEAN | Can this NPC request quotes? |
| `marketing_segment` | VARCHAR(50) | Pet owner type (dog person, cat person, multi-pet, etc.) |

---

## Pet Table (Population DB / Willow AuraDB)

### Required Fields from Quote Form

| Field Name | Type | Faker/Logic | Example | Notes |
|------------|------|-------------|---------|-------|
| `pet_name` | VARCHAR(100) | `fake.first_name()` or pet names list | "Barry", "Fluffy" | Popular pet names |
| `species` | VARCHAR(50) | Random choice | "Dog", "Cat" | From dropdown |
| `breed` | VARCHAR(100) | Breed list by species | "Labrador", "British Shorthair" | Species-specific |
| `date_of_birth` | DATE | Random within last 15 years | "2020-03-10" | Age affects pricing |
| `gender` | VARCHAR(10) | Random choice | "Male", "Female" | From dropdown |
| `microchipped` | BOOLEAN | 70% true, 30% false | TRUE | Most UK pets are chipped |
| `pre_existing_conditions` | JSONB | NULL or random conditions | `["Hip dysplasia"]` | Affects coverage |
| `acquired_date` | DATE | Before or equal to DOB | "2020-04-01" | When customer got pet |

### Additional Fields

| Field Name | Type | Purpose |
|------------|------|---------|
| `id` | SERIAL PRIMARY KEY | Unique identifier |
| `customer_id` | INTEGER FK | Links to customer |
| `created_at` | TIMESTAMP | When pet was added |

---

## Quote Preferences (Generated Randomly)

When NPC "requests quote", randomize these:

| Field | Options | Default |
|-------|---------|---------|
| `cover_type` | Accident Only, Time Limited, Lifetime | Random weighted (Lifetime 60%, Time Limited 30%, Accident 10%) |
| `excess_amount` | £0, £99, £149, £199 | Random |
| `vet_fee_limit` | £2,000, £4,000, £7,000, £12,000 | Random weighted (£4k and £7k most common) |

---

## Schema SQL (Postgres)

```sql
-- ============================================
-- CUSTOMERS TABLE
-- ============================================
CREATE TABLE customers (
    id SERIAL PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    phone_mobile VARCHAR(20),
    address_line_1 VARCHAR(255) NOT NULL,
    address_line_2 VARCHAR(255),
    city VARCHAR(100) NOT NULL,
    postcode VARCHAR(10) NOT NULL,
    date_of_birth DATE NOT NULL,

    -- Marketing & Segmentation
    personality_vector VECTOR(384),
    marketing_segment VARCHAR(50),
    is_active BOOLEAN DEFAULT TRUE,

    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_customers_postcode ON customers(postcode);
CREATE INDEX idx_customers_city ON customers(city);
CREATE INDEX idx_customers_email ON customers(email);

-- ============================================
-- PETS TABLE
-- ============================================
CREATE TABLE pets (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id) ON DELETE CASCADE,

    -- Pet Details (from quote form)
    pet_name VARCHAR(100) NOT NULL,
    species VARCHAR(50) NOT NULL CHECK (species IN ('Dog', 'Cat')),
    breed VARCHAR(100) NOT NULL,
    date_of_birth DATE NOT NULL,
    gender VARCHAR(10) CHECK (gender IN ('Male', 'Female')),
    microchipped BOOLEAN DEFAULT FALSE,
    pre_existing_conditions JSONB,
    acquired_date DATE NOT NULL,

    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_pets_customer ON pets(customer_id);
CREATE INDEX idx_pets_species ON pets(species);
CREATE INDEX idx_pets_breed ON pets(breed);

-- ============================================
-- QUOTES TABLE (for tracking quote requests)
-- ============================================
CREATE TABLE quotes (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    pet_id INTEGER NOT NULL REFERENCES pets(id),

    -- Quote preferences
    cover_type VARCHAR(50) NOT NULL CHECK (cover_type IN ('Accident Only', 'Time Limited', 'Lifetime')),
    excess_amount DECIMAL(10,2) NOT NULL,
    vet_fee_limit DECIMAL(10,2) NOT NULL,

    -- Pricing (random for MVP)
    monthly_premium DECIMAL(10,2) NOT NULL,
    annual_premium DECIMAL(10,2) NOT NULL,

    -- Status
    status VARCHAR(50) DEFAULT 'generated' CHECK (status IN ('generated', 'accepted', 'rejected', 'expired')),

    -- Metadata
    created_at TIMESTAMP DEFAULT NOW(),
    expires_at TIMESTAMP DEFAULT NOW() + INTERVAL '30 days'
);

CREATE INDEX idx_quotes_customer ON quotes(customer_id);
CREATE INDEX idx_quotes_status ON quotes(status);
```

---

## Faker Generation Strategy

### Phase 1: Core Demographics (WILL-009)
Generate 10M customers with basic info:
```python
from faker import Faker
fake = Faker('en_GB')  # UK locale for postcodes

for i in range(10_000_000):
    customer = {
        'full_name': fake.name(),
        'email': fake.email(),
        'phone_mobile': fake.phone_number(),
        'address_line_1': fake.street_address(),
        'address_line_2': fake.secondary_address() if random() > 0.7 else None,
        'city': fake.city(),
        'postcode': fake.postcode(),
        'date_of_birth': fake.date_of_birth(min_age=18, max_age=80),
        'is_active': True
    }
    # Bulk insert to Postgres
```

### Phase 2: Pet Associations (WILL-010)
30% of customers have pets (3M pet owners):
```python
pet_names = ['Max', 'Bella', 'Charlie', 'Lucy', 'Cooper', 'Daisy', 'Buddy', 'Luna', 'Rocky', 'Molly']
dog_breeds = ['Labrador', 'German Shepherd', 'Golden Retriever', 'Bulldog', 'Beagle', 'Poodle', 'Rottweiler', 'Yorkshire Terrier', 'Boxer', 'Dachshund']
cat_breeds = ['British Shorthair', 'Persian', 'Maine Coon', 'Siamese', 'Ragdoll', 'Bengal', 'Sphynx', 'Scottish Fold', 'Birman', 'Domestic Shorthair']

for customer_id in sample(customer_ids, int(len(customer_ids) * 0.3)):
    species = random.choice(['Dog', 'Cat'])
    breeds = dog_breeds if species == 'Dog' else cat_breeds

    pet = {
        'customer_id': customer_id,
        'pet_name': random.choice(pet_names),
        'species': species,
        'breed': random.choice(breeds),
        'date_of_birth': fake.date_between(start_date='-15y', end_date='today'),
        'gender': random.choice(['Male', 'Female']),
        'microchipped': random.random() > 0.3,  # 70% chipped
        'pre_existing_conditions': random_conditions() if random() > 0.85 else None,
        'acquired_date': # Logic: same as DOB or later
    }
```

### Phase 3: Vector Personalities (WILL-011)
Generate embeddings for similarity search:
```python
# Using sentence-transformers or OpenAI embeddings
personality_traits = [
    "loves cats", "allergic to dogs", "urban dweller",
    "rural farmer", "vegetarian", "conservative voter",
    "labour supporter", "gym enthusiast", "bookworm",
    "outdoor adventurer", "tech savvy", "traditional values"
]

# Each customer gets 3-5 random traits
# Embed traits to create personality_vector
```

---

## Data Quality Constraints

### UK-Specific
- ✅ Postcodes: Valid UK format (e.g., "SW1A 1AA", "M1 2AB")
- ✅ Phone numbers: UK mobile format (07xxx xxxxxx)
- ✅ Addresses: British street names, cities
- ✅ Names: English-sounding names

### Business Logic
- ✅ Customers must be 18+ years old
- ✅ Pets must be < 15 years old (typical insurance limit)
- ✅ `acquired_date` >= `pet.date_of_birth`
- ✅ Email addresses must be unique
- ✅ Microchip rate: ~70% (realistic UK stat)

### Data Distribution
- 30% of customers have pets (3M pet owners)
- 60% dogs, 40% cats (realistic UK ratio)
- 70% choose Lifetime cover (most popular)
- 15% have pre-existing conditions (realistic)

---

## Integration with Willow Ontology

When NPC "requests quote", data flows:

```
Population DB (Postgres)          Willow (AuraDB)
     ↓                                  ↓
Customer table ──────→ CREATE (:Customer) node
     ↓                                  ↓
Pet table ───────────→ CREATE (:Pet) node
     ↓                                  ↓
Quote generated ─────→ CREATE (:Quote) node
     ↓                                  ↓
Quote accepted ──────→ CREATE (:Policy) node
     ↓                                  ↓
Pet gets sick ───────→ CREATE (:Claim) node
```

**Relationships created:**
```cypher
(:Customer)-[:OWNS]->(:Pet)
(:Customer)-[:REQUESTED]->(:Quote)
(:Quote)-[:FOR_PET]->(:Pet)
(:Quote)-[:CONVERTED_TO]->(:Policy)
(:Policy)-[:COVERS]->(:Pet)
(:Claim)-[:AGAINST]->(:Policy)
(:Claim)-[:FOR_PET]->(:Pet)
```

---

## Validation Checklist (WILL-024)

- [ ] All quote form fields mapped to schema
- [ ] UK-specific data (postcodes, phones, addresses)
- [ ] Age constraints (customer 18+, pet <15 years)
- [ ] Data distribution realistic (30% pet owners, etc.)
- [ ] Faker locale set to `en_GB`
- [ ] Vector embeddings compatible with AuraDB vector search
- [ ] Quote form fields tested with sample NPC data
- [ ] Integration points defined (Postgres → AuraDB)

---

## Next Steps

1. **WILL-008**: Design this schema in Postgres on bunny server
2. **WILL-024**: Validate against quote form (this doc)
3. **WILL-009**: Build Faker generator using Ollama on RTX 3090 Ti
4. **WILL-010**: Generate 10M NPCs
5. **Test**: Random sample of 100 NPCs can fill quote form

**Success metric**: Any NPC can autonomously request a quote and have all required fields populated.

---

**Reference URL**: https://quote.purelypetsinsurance.co.uk/
**Updated**: December 21, 2025
**Status**: Specification ready for WILL-008 implementation 🌳
