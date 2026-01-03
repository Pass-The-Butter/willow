-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Reset Schema
DROP TABLE IF EXISTS claims CASCADE;
DROP TABLE IF EXISTS quotes CASCADE;
DROP TABLE IF EXISTS people CASCADE;
DROP TABLE IF EXISTS pets CASCADE;
DROP TABLE IF EXISTS customers CASCADE;

-- ============================================
-- CUSTOMERS TABLE (Matches Purely Pets Quote Form)
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
-- PETS TABLE (Matches Purely Pets Pet Details)
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
