// Willow Business Ontology - Claims Assessment Cycle
// Based on "Jane Winterbottom & Bobby" narrative

// ============================================
// CONSTRAINTS
// ============================================

// Unique IDs for core entities
CREATE CONSTRAINT person_id_unique IF NOT EXISTS FOR (p:Person) REQUIRE p.id IS UNIQUE;
CREATE CONSTRAINT policy_number_unique IF NOT EXISTS FOR (p:Policy) REQUIRE p.policy_number IS UNIQUE;
CREATE CONSTRAINT claim_reference_unique IF NOT EXISTS FOR (c:Claim) REQUIRE c.reference_number IS UNIQUE;
CREATE CONSTRAINT vet_practice_id_unique IF NOT EXISTS FOR (v:VetPractice) REQUIRE v.id IS UNIQUE;
CREATE CONSTRAINT pet_id_unique IF NOT EXISTS FOR (p:Pet) REQUIRE p.id IS UNIQUE;

// ============================================
// INDEXES
// ============================================

CREATE INDEX person_email IF NOT EXISTS FOR (p:Person) ON (p.email);
CREATE INDEX pet_name IF NOT EXISTS FOR (p:Pet) ON (p.name);
CREATE INDEX diagnosis_code IF NOT EXISTS FOR (d:Diagnosis) ON (d.code);

// ============================================
// SCHEMA DEFINITION (DOCUMENTATION ONLY)
// ============================================

// Nodes:
// - Person: {id, name, email, phone}
// - Address: {line1, postcode}
// - Pet: {id, name, species, date_of_birth}
// - Breed: {name, species}
// - Policy: {policy_number, start_date, premium_amount, premium_currency}
// - Insurer: {name}
// - Underwriter: {name}
// - Claim: {reference_number, incident_date, status, description}
// - VetPractice: {id, name, email}
// - Diagnosis: {code, description}
// - Document: {type, content, timestamp}
// - Interaction: {type, notes, timestamp}
// - Agent: {name, role}

// Relationships:
// (:Person)-[:LIVES_AT]->(:Address)
// (:Person)-[:OWNS]->(:Pet)
// (:Pet)-[:IS_BREED]->(:Breed)
// (:Policy)-[:COVERS]->(:Pet)
// (:Policy)-[:OWNED_BY]->(:Person)
// (:Policy)-[:UNDERWRITTEN_BY]->(:Underwriter)
// (:Policy)-[:INSURED_BY]->(:Insurer)
// (:Claim)-[:FILED_AGAINST]->(:Policy)
// (:Claim)-[:INVOLVES]->(:Pet)
// (:Pet)-[:VISITED]->(:VetPractice)
// (:VetPractice)-[:DIAGNOSED]->(:Diagnosis)
// (:Diagnosis)-[:FOR]->(:Pet)
// (:Person)-[:SUBMITTED]->(:Document)
// (:Broker)-[:CONTACTED]->(:VetPractice)
// (:Assessor)-[:ASSESSED]->(:Claim)
// (:Agent)-[:RESEARCHED]->(:Diagnosis)
