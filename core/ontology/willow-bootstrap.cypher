// Willow Bootstrap Schema
// Creates initial graph structure with skills, brand assets, decisions, and system metadata
// Run this after Neo4j container starts

// ============================================
// SYSTEM METADATA
// ============================================

CREATE (sys:System {
  name: 'Willow',
  version: '0.1.0',
  environment: 'development',
  created_at: datetime(),
  description: 'Autonomous graph ontology system where capabilities live as nodes'
});

// ============================================
// PROJECT MANAGEMENT ONTOLOGY (New)
// ============================================

// The Willow Super-Project
CREATE (proj:Project {
  name: 'Willow',
  description: 'Autonomous Living Ontology',
  status: 'active',
  created_at: datetime()
});

// Link System to Project
MATCH (sys:System {name: 'Willow'})
MATCH (proj:Project {name: 'Willow'})
CREATE (sys)-[:IS_IMPLEMENTATION_OF]->(proj);

// Components (Domains)
CREATE (pop:Component {
  name: 'Population',
  path: '/domains/population',
  description: 'Entity generation and management (The People)',
  store: 'postgres',
  status: 'planned'
});

CREATE (ui:Component {
  name: 'Interface',
  path: '/domains/interface',
  description: '3D/VR MMOG-style interface elements (The World)',
  status: 'planned'
});

CREATE (brand:Component {
  name: 'Brand',
  path: '/domains/brand',
  description: 'Brand identity, assets, and design rules (The Identity)',
  status: 'active'
});

// ============================================
// INFRASTRUCTURE ONTOLOGY
// ============================================

CREATE (mac:ComputeResource {
  name: 'Mac Mini M4',
  role: 'Development Controller',
  os: 'macOS',
  specs: '16GB RAM',
  network: 'Tailscale'
});

CREATE (xeon:ComputeResource {
  name: 'Xeon Server',
  role: 'Population Host',
  os: 'Ubuntu',
  specs: '128GB RAM',
  network: 'Tailscale'
});

CREATE (win:ComputeResource {
  name: 'Win 11 PC',
  role: 'Compute Node',
  os: 'Windows 11',
  gpu: 'NVIDIA RTX 3090ti',
  specs: '64GB RAM',
  network: 'Tailscale'
});

// Link Infrastructure
MATCH (proj:Project {name: 'Willow'})
MATCH (r:ComputeResource)
CREATE (proj)-[:HAS_RESOURCE]->(r);

// Link Components to Resources
MATCH (pop:Component {name: 'Population'})
MATCH (xeon:ComputeResource {name: 'Xeon Server'})
CREATE (pop)-[:HOSTED_ON]->(xeon);

CREATE (core:Component {
  name: 'Core',
  path: '/core',
  description: 'System kernel, API, and Ontology',
  status: 'active'
});

// Link Projects to Components
MATCH (proj:Project {name: 'Willow'})
MATCH (c:Component)
CREATE (proj)-[:HAS_COMPONENT]->(c);

// ============================================
// SKILLS
// ============================================

// Python Skill: Hello World
CREATE (hello:Skill {
  name: 'hello_world',
  language: 'python',
  code_path: '/core/skills/hello_world.py',
  mcp_compatible: true,
  description: 'First skill - proves the system works',
  parameters: ['name'],
  created_at: datetime()
});

// Python Skill: Retrieve Conversation Context
CREATE (memory:Skill {
  name: 'retrieve_conversation_context',
  language: 'python',
  code_path: '/core/skills/retrieve_conversation_context.py',
  mcp_compatible: true,
  description: 'Query decisions and insights from graph by keyword',
  parameters: ['keyword', 'depth', 'limit'],
  created_at: datetime()
});

// Python Skill: Ingest MSSQL Claims (Placeholder - likely to move to Population)
CREATE (ingest:Skill {
  name: 'ingest_mssql_claims',
  language: 'python',
  code_path: '/core/skills/ingest_mssql_claims.py',
  mcp_compatible: true,
  description: 'Read from MSSQL and create graph nodes',
  parameters: ['table', 'limit'],
  status: 'planned'
});
// ============================================
// INSURANCE ONTOLOGY (Jerry & Barry Story)
// ============================================

// Entity: Pet (Asset)
CREATE (pet_def:Decision {
    text: 'Ontology: Pet defined as Insured Asset',
    phase: 'ontology',
    confidence: 'high'
});

// We don't instantiate the Class nodes here typically, 
// but we define the schema relationships implicitly via usage or explicit Schema nodes if we were using a metamodel.
// For now, let's create a placeholder Concept node for documentation in the graph.

CREATE (c_person:Component {name: 'Person Concept', type: 'Concept', description: 'Represents a human (Jerry)'});
CREATE (c_pet:Component {name: 'Pet Concept', type: 'Concept', description: 'Represents an animal (Barry)'});
CREATE (c_policy:Component {name: 'Policy Concept', type: 'Concept', description: 'Insurance Contract'});
CREATE (c_claim:Component {name: 'Claim Concept', type: 'Concept', description: 'Request for indemnification'});

// Link Concepts to Domains
MATCH (pop:Component {name: 'Population'})
MATCH (core:Component {name: 'Core'})

MERGE (pop)-[:OWNS_CONCEPT]->(c_person)
MERGE (core)-[:OWNS_CONCEPT]->(c_policy)
MERGE (core)-[:OWNS_CONCEPT]->(c_claim)
MERGE (pop)-[:OWNS_CONCEPT]->(c_pet) // Pets live in population? Or separate Asset domain? Let's say Population for now.

// ============================================
// BRAND ASSETS
// ============================================

CREATE (autumn:BrandAsset {
  season: 'autumn',
  active: true,
  palette_json: '{"primary": "#8B9D83", "accent": "#C17A5C", "grey": "#A89F91", "burgundy": "#6B4444", "background": "#F5F1E8"}',
  logo_url: 'https://www.canva.com/d/r1GY4_LfcJpg1xA',
  description: 'Minimalist geometric willow tree - autumn palette',
  created_at: datetime()
});

// Seasonal variant placeholders
CREATE (winter:BrandAsset {
  season: 'winter',
  active: false,
  description: 'Winter seasonal variant',
  status: 'designed',
  created_at: datetime()
});

CREATE (spring:BrandAsset {
  season: 'spring',
  active: false,
  description: 'Spring seasonal variant',
  status: 'designed',
  created_at: datetime()
});

CREATE (summer:BrandAsset {
  season: 'summer',
  active: false,
  description: 'Summer seasonal variant',
  status: 'designed',
  created_at: datetime()
});

// Link Brand Component to Brand Assets
MATCH (brand:Component {name: 'Brand'})
MATCH (ba:BrandAsset)
CREATE (brand)-[:MANAGES_ASSET]->(ba);

// ============================================
// DECISIONS (Conversational Memory)
// ============================================

CREATE (dec1:Decision {
  text: 'Use Docker MCP for full stack autonomy',
  rationale: 'Claude can manage entire infrastructure without manual setup. Enables fully autonomous system management and easy iteration.',
  made_at: datetime('2025-12-21T00:00:00Z'),
  suggested_by: 'Claude Desktop',
  confidence: 'high',
  phase: 'architecture'
});

CREATE (dec2:Decision {
  text: 'Store conversational memory in AuraDB alongside domain data',
  rationale: 'Cost control for PoC, semantic coherence between decisions and domain knowledge',
  made_at: datetime('2025-12-21T00:00:00Z'),
  suggested_by: 'Peter',
  confidence: 'high',
  phase: 'architecture'
});

CREATE (dec3:Decision {
  text: 'Skills stored as graph nodes',
  rationale: 'System becomes self-describing and introspectable. Claude can query "what can I do?" by querying the ontology itself.',
  made_at: datetime('2025-12-21T00:00:00Z'),
  suggested_by: 'Claude Desktop',
  confidence: 'high',
  phase: 'core-innovation'
});

CREATE (dec4:Decision {
  text: 'Build educational presentation with pet insurance narrative',
  rationale: 'Demonstrates SQL→Graph transformation using relatable customer journey story',
  made_at: datetime('2025-12-21T00:00:00Z'),
  suggested_by: 'Claude Desktop',
  phase: 'education'
});

CREATE (dec5:Decision {
  text: 'Autumn as primary brand season',
  rationale: 'Warm, professional palette. Willow tree naturally associated with nature and seasons.',
  made_at: datetime('2025-12-21T00:00:00Z'),
  suggested_by: 'Claude Desktop',
  phase: 'branding'
});

CREATE (dec6:Decision {
  text: 'Spec-Driven Architecture',
  rationale: 'The Graph (Spec + Memory) is the source of truth ("The Product"). Code is a projection.',
  made_at: datetime(),
  suggested_by: 'Peter'
});

// ============================================
// RELATIONSHIPS
// ============================================

// Connect decisions to system
MATCH (sys:System {name: 'Willow'})
MATCH (dec:Decision)
MERGE (sys)-[:HAS_DECISION]->(dec);

// Connect skills to components (Skills belong to Core for now)
MATCH (core:Component {name: 'Core'})
MATCH (skill:Skill)
MERGE (core)-[:PROVIDES_CAPABILITY]->(skill);

// ============================================
// INDEXES AND CONSTRAINTS
// ============================================

CREATE CONSTRAINT skill_name_unique IF NOT EXISTS FOR (s:Skill) REQUIRE s.name IS UNIQUE;
CREATE CONSTRAINT system_name_unique IF NOT EXISTS FOR (s:System) REQUIRE s.name IS UNIQUE;
CREATE CONSTRAINT project_name_unique IF NOT EXISTS FOR (p:Project) REQUIRE p.name IS UNIQUE;
CREATE CONSTRAINT component_name_unique IF NOT EXISTS FOR (c:Component) REQUIRE c.name IS UNIQUE;

CREATE INDEX skill_language IF NOT EXISTS FOR (s:Skill) ON (s.language);
CREATE INDEX brand_season IF NOT EXISTS FOR (b:BrandAsset) ON (b.season);

// ============================================
// VECTOR INDEXES
// ============================================

// Index for Semantic Search on Specifications
// Note: Requires Neo4j 5.x+ and GenAI plugin or similar capability. 
// Standard AuraDB supports vector indexes.
CREATE VECTOR INDEX spec_content_index IF NOT EXISTS
FOR (s:Specification) ON (s.embedding)
OPTIONS {indexConfig: {
 `vector.dimensions`: 1536,
 `vector.similarity_function`: 'cosine'
}};

// Index for Semantic Search on Decisions
CREATE VECTOR INDEX decision_text_index IF NOT EXISTS
FOR (d:Decision) ON (d.embedding)
OPTIONS {indexConfig: {
 `vector.dimensions`: 1536,
 `vector.similarity_function`: 'cosine'
}};
