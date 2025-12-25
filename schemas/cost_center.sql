-- Cost Center Schema for Willow
-- "We can only manage what we can see."

CREATE TABLE IF NOT EXISTS token_usage (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    agent_name VARCHAR(50),      -- e.g., "Economical Audit", "Delegation Matrix"
    model_name VARCHAR(50),      -- e.g., "llama3-70b", "gpt-4-turbo"
    intent VARCHAR(50),          -- e.g., "CODE", "CREATIVE", "AUDIT"
    input_tokens INT DEFAULT 0,
    output_tokens INT DEFAULT 0,
    estimated_cost_usd DECIMAL(10, 6),
    conversation_id VARCHAR(100) -- To link back to N8N or Session
);

-- Index for reporting
CREATE INDEX idx_usage_timestamp ON token_usage(timestamp);
CREATE INDEX idx_usage_model ON token_usage(model_name);

-- TODO: Create a View for "Daily Spend"
-- CREATE VIEW daily_spend AS ...
