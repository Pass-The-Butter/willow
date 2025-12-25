// ============================================
// Willow Organogram Schema
// Living project structure as a hierarchical graph
// ============================================

// --------------------------------------------
// 1. PROJECT ROOT
// --------------------------------------------
CREATE (willow:Project {
  name: "Willow",
  vision: "GraphRAG-powered insurance simulation with autonomous agents",
  created: datetime(),
  status: "Active"
});

// --------------------------------------------
// 2. DOMAINS (C-Suite Level)
// --------------------------------------------
MATCH (willow:Project {name: "Willow"})
CREATE (willow)-[:HAS_DOMAIN]->(population:Domain {
  name: "Population",
  role: "VP of Data",
  description: "Generate and manage synthetic customer/pet entities",
  owner: "Data Team"
}),
(willow)-[:HAS_DOMAIN]->(interface:Domain {
  name: "Interface",
  role: "VP of UX",
  description: "User-facing applications and APIs",
  owner: "Frontend Team"
}),
(willow)-[:HAS_DOMAIN]->(core:Domain {
  name: "Core",
  role: "VP of Engineering",
  description: "Skills, ontology, and infrastructure",
  owner: "Platform Team"
});

// --------------------------------------------
// 3. POPULATION DOMAIN COMPONENTS
// --------------------------------------------
MATCH (population:Domain {name: "Population"})
CREATE (population)-[:HAS_COMPONENT]->(generator:Component {
  name: "Generator",
  description: "Create synthetic customer and pet data",
  location: "domains/population/generator.py"
}),
(population)-[:HAS_COMPONENT]->(schema:Component {
  name: "Schema",
  description: "Database structure for population entities",
  location: "docs/POPULATION_SCHEMA_SPEC.md"
}),
(population)-[:HAS_COMPONENT]->(qa:Component {
  name: "Quality Assurance",
  description: "Validate data quality and distribution"
});

// --------------------------------------------
// 4. GENERATOR TASKS
// --------------------------------------------
MATCH (generator:Component {name: "Generator"})
CREATE (generator)-[:HAS_TASK]->(faker_task:Task {
  name: "Faker Integration",
  description: "Use Faker library for UK demographic data",
  status: "In Progress",
  assignee: "Generator Agent"
}),
(generator)-[:HAS_TASK]->(ollama_task:Task {
  name: "Ollama Integration",
  description: "Generate personality vectors using local LLM",
  status: "Not Started"
}),
(generator)-[:HAS_TASK]->(batch_task:Task {
  name: "Batch Processing",
  description: "Optimize for large-scale generation (1M+ records)",
  status: "Not Started"
});

// --------------------------------------------
// 5. SCHEMA TASKS
// --------------------------------------------
MATCH (schema:Component {name: "Schema"})
CREATE (schema)-[:HAS_TASK]->(customer_table:Task {
  name: "Customer Table",
  description: "Define customers table with Purely Pets fields",
  status: "Complete"
}),
(schema)-[:HAS_TASK]->(pet_table:Task {
  name: "Pet Table",
  description: "Define pets table with species, breed, conditions",
  status: "Complete"
}),
(schema)-[:HAS_TASK]->(quote_table:Task {
  name: "Quote Table",
  description: "Define quotes table for policy requests",
  status: "Complete"
});

// --------------------------------------------
// 6. INTERFACE DOMAIN COMPONENTS
// --------------------------------------------
MATCH (interface:Domain {name: "Interface"})
CREATE (interface)-[:HAS_COMPONENT]->(webapp:Component {
  name: "Web App",
  description: "Flask/React web interface",
  location: "domains/interface/app.py"
}),
(interface)-[:HAS_COMPONENT]->(api:Component {
  name: "API",
  description: "REST/WebSocket endpoints"
});

// --------------------------------------------
// 7. WEB APP TASKS
// --------------------------------------------
MATCH (webapp:Component {name: "Web App"})
CREATE (webapp)-[:HAS_TASK]->(landing:Task {
  name: "Landing Page",
  description: "Project overview page with links to resources",
  status: "Not Started"
}),
(webapp)-[:HAS_TASK]->(quote_form:Task {
  name: "Quote Form",
  description: "Purely Pets-style quote request form",
  status: "Not Started"
}),
(webapp)-[:HAS_TASK]->(dashboard:Task {
  name: "Dashboard",
  description: "System status and population metrics",
  status: "Not Started"
});

// --------------------------------------------
// 8. CORE DOMAIN COMPONENTS
// --------------------------------------------
MATCH (core:Domain {name: "Core"})
CREATE (core)-[:HAS_COMPONENT]->(skills:Component {
  name: "Skills",
  description: "Agent capabilities for querying and acting",
  location: "core/skills/"
}),
(core)-[:HAS_COMPONENT]->(ontology:Component {
  name: "Ontology",
  description: "Graph schema and concept definitions",
  location: "core/ontology/"
});

// --------------------------------------------
// 9. SPECIFICATIONS & CRITERIA
// --------------------------------------------
MATCH (faker_task:Task {name: "Faker Integration"})
CREATE (faker_task)-[:MUST_SATISFY]->(faker_criteria:TestCriteria {
  validation: "Generate 1000 customers with valid UK postcodes",
  performance: "Complete generation in under 60 seconds",
  quality: "Zero NULL values in required fields (name, email, postcode)",
  distribution: "Age distribution skewed 25-45 for pet owners"
}),
(faker_task)-[:REQUIRES]->(faker_spec:Specification {
  library: "Faker",
  locale: "en_GB",
  fields: ["full_name", "email", "phone_mobile", "address", "postcode", "date_of_birth"],
  reference: "domains/population/specification.md"
});

MATCH (landing:Task {name: "Landing Page"})
CREATE (landing)-[:MUST_SATISFY]->(landing_criteria:TestCriteria {
  responsive: "Mobile and desktop compatible",
  performance: "Load time under 2 seconds",
  content: "Include links to GitHub, Jira, Confluence, AuraDB",
  branding: "Use Willow project name and tagline"
}),
(landing)-[:REQUIRES]->(landing_spec:Specification {
  framework: "Flask + Jinja2 templates",
  style: "Minimal, professional",
  reference: "MISSION_CONTROL.md (for links)"
});

// --------------------------------------------
// 10. TASK DEPENDENCIES
// --------------------------------------------
MATCH (ollama_task:Task {name: "Ollama Integration"}),
      (faker_task:Task {name: "Faker Integration"})
CREATE (ollama_task)-[:DEPENDS_ON]->(faker_task);

MATCH (batch_task:Task {name: "Batch Processing"}),
      (faker_task:Task {name: "Faker Integration"}),
      (ollama_task:Task {name: "Ollama Integration"})
CREATE (batch_task)-[:DEPENDS_ON]->(faker_task),
       (batch_task)-[:DEPENDS_ON]->(ollama_task);

MATCH (quote_form:Task {name: "Quote Form"}),
      (landing:Task {name: "Landing Page"})
CREATE (quote_form)-[:DEPENDS_ON]->(landing);

// --------------------------------------------
// 11. DIARY SYSTEM EXAMPLE
// --------------------------------------------
MATCH (faker_task:Task {name: "Faker Integration"})
CREATE (faker_task)-[:HAS_DIARY_ENTRY]->(entry1:DiaryEntry {
  agent: "Chief Officer",
  timestamp: datetime(),
  status: "In Progress",
  notes: "Updated specification.md to include Purely Pets alignment. Schema now references POPULATION_SCHEMA_SPEC.md for detailed field mapping."
});

// --------------------------------------------
// 12. RFC SYSTEM EXAMPLE
// --------------------------------------------
MATCH (generator:Component {name: "Generator"})
CREATE (generator)-[:HAS_RFC]->(rfc1:RFC {
  id: "RFC-001",
  title: "Use pgvector personality embeddings vs separate vector table",
  author: "Chief Officer",
  rationale: "Current spec shows separate vector columns (personality_vector). Consider if this should be JSONB embeddings or dedicated vector index.",
  status: "Open",
  created: datetime(),
  priority: "Medium"
});

// --------------------------------------------
// 13. MESSAGE SYSTEM EXAMPLE
// --------------------------------------------
MATCH (faker_task:Task {name: "Faker Integration"}),
      (customer_table:Task {name: "Customer Table"})
CREATE (faker_task)-[:SENT_MESSAGE]->(msg1:Message {
  from: "Generator Agent",
  to: "Schema Agent",
  subject: "Confirm personality_vector dimensions",
  body: "Spec says 384 dimensions for personality_vector. Is this aligned with Ollama embedding model?",
  timestamp: datetime(),
  status: "Unread",
  priority: "High"
})-[:TARGETS]->(customer_table);

// --------------------------------------------
// 14. INDEXES FOR FAST TRAVERSAL
// --------------------------------------------
CREATE INDEX task_status_idx FOR (t:Task) ON (t.status);
CREATE INDEX task_name_idx FOR (t:Task) ON (t.name);
CREATE INDEX component_name_idx FOR (c:Component) ON (c.name);
CREATE INDEX domain_name_idx FOR (d:Domain) ON (d.name);
CREATE INDEX rfc_status_idx FOR (r:RFC) ON (r.status);
CREATE INDEX message_status_idx FOR (m:Message) ON (m.status);
