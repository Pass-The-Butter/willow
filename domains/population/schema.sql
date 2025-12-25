-- Schema for Population Database
-- Derived from remote_generator.py

CREATE TABLE IF NOT EXISTS people (
    id UUID PRIMARY KEY,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    age INT,
    risk_score FLOAT,
    policy_start_date DATE,
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS quotes (
    id UUID PRIMARY KEY,
    person_id UUID REFERENCES people(id),
    product_type TEXT,
    premium_amount NUMERIC(10, 2),
    status TEXT,
    created_at DATE,
    valid_until DATE,
    text TEXT -- LLM Generated Quote
);

CREATE TABLE IF NOT EXISTS claims (
    id UUID PRIMARY KEY,
    quote_id UUID REFERENCES quotes(id),
    incident_date DATE,
    report_date DATE,
    description TEXT,
    claim_amount NUMERIC(10, 2),
    status TEXT,
    created_at DATE
);

-- Indexes for performance
CREATE INDEX IF NOT EXISTS idx_people_active ON people(active);
CREATE INDEX IF NOT EXISTS idx_quotes_person ON quotes(person_id);
CREATE INDEX IF NOT EXISTS idx_claims_quote ON claims(quote_id);
