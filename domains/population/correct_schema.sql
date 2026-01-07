-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Reset Schema
DROP TABLE IF EXISTS claims CASCADE;
DROP TABLE IF EXISTS quotes CASCADE;
DROP TABLE IF EXISTS pets CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

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

    -- Pet Details
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
-- QUOTES TABLE
-- ============================================
CREATE TABLE quotes (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    pet_id INTEGER NOT NULL REFERENCES pets(id),

    -- Quote preferences
    cover_type VARCHAR(50) NOT NULL CHECK (cover_type IN ('Accident Only', 'Time Limited', 'Lifetime')),
    excess_amount DECIMAL(10,2) NOT NULL,
    vet_fee_limit DECIMAL(10,2) NOT NULL,

    -- Pricing
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

-- ============================================
-- CLAIMS TABLE
-- ============================================
CREATE TABLE claims (
    id SERIAL PRIMARY KEY,
    customer_id INTEGER NOT NULL REFERENCES customers(id),
    pet_id INTEGER NOT NULL REFERENCES pets(id),
    quote_id INTEGER REFERENCES quotes(id),
    
    incident_date DATE NOT NULL,
    report_date DATE NOT NULL,
    claim_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'FILED' CHECK (status IN ('FILED', 'INVESTIGATING', 'APPROVED', 'PAID', 'DENIED')),
    description TEXT,
    
    -- Metadata
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_claims_customer ON claims(customer_id);
CREATE INDEX idx_claims_status ON claims(status);
