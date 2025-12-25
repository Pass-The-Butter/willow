# Population Component Specification

## Overview
The **Population** component is responsible for generating and managing the synthetic insured entities ("Customers") that drive the Willow system. These entities serve as the substrate for claims, policy decisions, and customer journey simulations.

**Product Context**: This population is designed to align with **Purely Pets Insurance** quote flow and eligibility requirements. See [POPULATION_SCHEMA_SPEC.md](../../docs/POPULATION_SCHEMA_SPEC.md) for full field mapping.

## Data Store
- **Type**: Relational Database (Postgres)
- **Extensions**: `pgvector` (Vector Optimized storage for customer attributes)
- **Target Host**: `Bunny` - Xeon Server (Ubuntu, 128GB RAM)
- **Database Name**: `population`

## Entity Definitions

### 1. Customer (Primary Entity)

Represents a potential or actual pet insurance customer, aligned with Purely Pets quote form fields.

#### Core Attributes (from Quote Form)
| Field | Type | Description | Faker Method |
|-------|------|-------------|--------------|
| `id` | SERIAL PRIMARY KEY | Unique identifier | Auto-increment |
| `full_name` | VARCHAR(255) | First + Last name | `fake.name()` |
| `email` | VARCHAR(255) UNIQUE | Email address | `fake.email()` (UK locale) |
| `phone_mobile` | VARCHAR(20) | UK mobile number | `fake.phone_number()` |
| `address_line_1` | VARCHAR(255) | Primary address | `fake.street_address()` |
| `address_line_2` | VARCHAR(255) | Secondary address (optional) | `fake.secondary_address()` |
| `city` | VARCHAR(100) | UK city | `fake.city()` |
| `postcode` | VARCHAR(10) | UK postcode | `fake.postcode()` |
| `date_of_birth` | DATE | Age 18-80 | `fake.date_of_birth(min_age=18, max_age=80)` |

#### Extended Attributes (System Use)
| Field | Type | Description |
|-------|------|-------------|
| `personality_vector` | VECTOR(384) | Embeddings for similarity search (preferences, behaviors) |
| `marketing_segment` | VARCHAR(50) | Pet owner type (dog person, cat person, multi-pet) |
| `is_active` | BOOLEAN | Can this customer request quotes? |
| `created_at` | TIMESTAMP | When customer was generated |
| `updated_at` | TIMESTAMP | Last modification |

### 2. Pet (Linked Entity)

Represents pets owned by customers, aligned with Purely Pets pet details form.

#### Core Attributes (from Quote Form)
| Field | Type | Description | Logic |
|-------|------|-------------|-------|
| `id` | SERIAL PRIMARY KEY | Unique identifier | Auto-increment |
| `customer_id` | INTEGER FK | Links to customer | References customers(id) |
| `pet_name` | VARCHAR(100) | Pet's name | Random from pet names list |
| `species` | VARCHAR(50) | "Dog" or "Cat" | Random choice (species dropdown) |
| `breed` | VARCHAR(100) | Breed name | Species-specific breed list |
| `date_of_birth` | DATE | Pet's age (0-15 years) | Random within last 15 years |
| `gender` | VARCHAR(10) | "Male" or "Female" | Random choice |
| `microchipped` | BOOLEAN | Is pet microchipped? | 70% TRUE, 30% FALSE |
| `pre_existing_conditions` | JSONB | Medical conditions (affects coverage) | NULL or random conditions list |
| `acquired_date` | DATE | When customer got pet | On or after pet DOB |

#### Extended Attributes
| Field | Type | Description |
|-------|------|-------------|
| `created_at` | TIMESTAMP | When pet was added |
| `updated_at` | TIMESTAMP | Last modification |

### 3. Quote (Generated Interactions)

Tracks quote requests made by customers for their pets.

| Field | Type | Description | Logic |
|-------|------|-------------|-------|
| `id` | SERIAL PRIMARY KEY | Unique identifier | Auto-increment |
| `customer_id` | INTEGER FK | References customers(id) | |
| `pet_id` | INTEGER FK | References pets(id) | |
| `cover_type` | VARCHAR(50) | Accident Only, Time Limited, Lifetime | Random weighted (Lifetime 60%, Time Limited 30%, Accident 10%) |
| `excess_amount` | DECIMAL(10,2) | £0, £99, £149, £199 | Random choice |
| `vet_fee_limit` | DECIMAL(10,2) | £2,000, £4,000, £7,000, £12,000 | Random weighted (£4k/£7k most common) |
| `monthly_premium` | DECIMAL(10,2) | Calculated premium | Random for MVP |
| `annual_premium` | DECIMAL(10,2) | Calculated premium | monthly * 12 |
| `status` | VARCHAR(50) | generated, accepted, rejected, expired | Default: generated |
| `created_at` | TIMESTAMP | When quote was generated | |
| `expires_at` | TIMESTAMP | Quote expiry (30 days) | created_at + 30 days |

## Generation Logic

### Demographics (UK-Focused)
- **Locale**: Use Faker `en_GB` for UK-specific postcodes, phone numbers, addresses
- **Age Distribution**: Slight skew towards 25-45 demographic (typical pet owners)
- **Pet Ownership**: ~30% of generated customers should have pets (realistic UK rate)
- **Multi-Pet Households**: 15% of pet owners have 2+ pets

### Realistic Constraints
- **Microchip Rate**: 70% of pets are microchipped (UK standard)
- **Cover Type Preferences**: Lifetime cover most popular (60%), then Time Limited (30%), Accident Only (10%)
- **Breed Distribution**: Use common UK breeds (Labradors, British Shorthairs, etc.)
- **Pre-existing Conditions**: 10-15% of pets have conditions (hip dysplasia, allergies, etc.)

### Ollama Integration
- **Inference**: Use Ollama (running on Frank) via `http://frank:11434/api/generate`
- **Model**: `deepseek-r1:32b` for reasoning about pet personalities and customer segments
- **Vector Generation**: Generate `personality_vector` embeddings for semantic search

## Interfaces

### Generation Script
- **Location**: `domains/population/generator.py` or `domains/population/remote_generator.py`
- **Execution**: Runs on Frank (Windows 11, Ollama installed)
- **Batch Size**: Generate N customers in configurable batches
- **Output**: Bulk insert into Postgres on Bunny

### Database Access
- **Read-Only**: Analysis skills query via SQL
- **CRUD**: Generator has write access for population seeding

## Reference Documentation
For complete SQL schema and Purely Pets field mapping, see:
- [POPULATION_SCHEMA_SPEC.md](../../docs/POPULATION_SCHEMA_SPEC.md)
