// Willow Task Management Schema
// Tasks, Sprints, and Roadmap stored AS graph nodes
// The specification IS the product

// ============================================
// TASK NODES
// ============================================

// Sprint: Bootstrap
CREATE (sprint1:Sprint {
  name: 'Bootstrap',
  status: 'active',
  started_at: datetime('2025-12-21T00:00:00Z'),
  goal: 'Get Willow infrastructure running and skills executing'
});

// Sprint: Population System
CREATE (sprint2:Sprint {
  name: 'Population System',
  status: 'planned',
  goal: 'Generate 10M synthetic NPCs for test customers'
});

// Sprint: Pet Claims Journey
CREATE (sprint3:Sprint {
  name: 'Pet Claims Journey',
  status: 'planned',
  goal: 'Implement customer journey ontology for insurance demo'
});

// ============================================
// BOOTSTRAP TASKS
// ============================================

CREATE (t1:Task {
  id: 'WILL-001',
  title: 'Reorganize file structure to match docker-compose',
  description: 'Move files to ./infrastructure/neo4j, ./core/api, ./core/skills, ./domains/',
  status: 'todo',
  priority: 'critical',
  assigned_to: 'claude',
  created_at: datetime()
});

CREATE (t2:Task {
  id: 'WILL-002',
  title: 'Fix autumn BrandAsset in AuraDB',
  description: 'Logo URL caused syntax error during schema load - needs manual fix',
  status: 'todo',
  priority: 'low',
  assigned_to: 'claude',
  created_at: datetime()
});

CREATE (t3:Task {
  id: 'WILL-003',
  title: 'Start Docker containers',
  description: 'docker-compose up -d --build (MCP, API, N8N, Population DB)',
  status: 'todo',
  priority: 'critical',
  assigned_to: 'claude',
  created_at: datetime()
});

CREATE (t4:Task {
  id: 'WILL-004',
  title: 'Test skill execution - get_skills()',
  description: 'Verify MCP can query available skills from graph',
  status: 'todo',
  priority: 'high',
  assigned_to: 'claude',
  created_at: datetime()
});

CREATE (t5:Task {
  id: 'WILL-005',
  title: 'Test skill execution - hello_world',
  description: 'Execute hello_world skill via Willow API',
  status: 'todo',
  priority: 'high',
  assigned_to: 'claude',
  created_at: datetime()
});

CREATE (t6:Task {
  id: 'WILL-006',
  title: 'Test skill execution - retrieve_conversation_context',
  description: 'Query decisions by keyword (e.g. "Docker") to verify memory retrieval',
  status: 'todo',
  priority: 'high',
  assigned_to: 'claude',
  created_at: datetime()
});

// ============================================
// POPULATION SYSTEM TASKS
// ============================================

CREATE (t7:Task {
  id: 'WILL-007',
  title: 'SSH to bunny server and verify access',
  description: 'ssh bunny@bunny with Chocolate1! password, verify 128GB Xeon specs',
  status: 'todo',
  priority: 'high',
  assigned_to: 'claude',
  created_at: datetime()
});

CREATE (t8:Task {
  id: 'WILL-008',
  title: 'Design Population schema (Postgres)',
  description: 'Tables for NPCs: demographics, addresses, vector personalities',
  status: 'todo',
  priority: 'medium',
  assigned_to: 'claude',
  created_at: datetime()
});

CREATE (t9:Task {
  id: 'WILL-009',
  title: 'Create Population generator agent',
  description: 'Use Faker to generate English customers with postcodes, mobiles',
  status: 'todo',
  priority: 'medium',
  assigned_to: 'claude',
  created_at: datetime()
});

CREATE (t10:Task {
  id: 'WILL-010',
  title: 'Generate initial 10M NPCs',
  description: 'Run population generator to create 10 million synthetic customers',
  status: 'todo',
  priority: 'low',
  assigned_to: 'claude',
  created_at: datetime()
});

CREATE (t11:Task {
  id: 'WILL-011',
  title: 'Add vector embeddings to NPCs',
  description: 'Generate personality vectors (cat lovers, allergies, politics)',
  status: 'todo',
  priority: 'low',
  assigned_to: 'claude',
  created_at: datetime()
});

// ============================================
// PET CLAIMS JOURNEY TASKS
// ============================================

CREATE (t12:Task {
  id: 'WILL-012',
  title: 'Design Pet Claims sub-ontology',
  description: 'Nodes: Customer, Pet, Policy, Claim, Vet, Treatment, Diagnosis, Payment',
  status: 'todo',
  priority: 'high',
  assigned_to: 'claude',
  created_at: datetime()
});

CREATE (t13:Task {
  id: 'WILL-013',
  title: 'Implement Customer Journey schema',
  description: 'Jerry finds Barry → Quote → Policy → Symptoms → Vet → Claim → Payment',
  status: 'todo',
  priority: 'high',
  assigned_to: 'claude',
  created_at: datetime()
});

CREATE (t14:Task {
  id: 'WILL-014',
  title: 'Connect to MSSQL claims database',
  description: 'Ingest real pet claims data from Peter\'s MSSQL (credentials TBD)',
  status: 'blocked',
  priority: 'medium',
  assigned_to: 'claude',
  blocked_reason: 'Waiting for MSSQL credentials from Peter',
  created_at: datetime()
});

CREATE (t15:Task {
  id: 'WILL-015',
  title: 'Implement Accumulating Snapshot for Claims',
  description: 'Track claim state changes: submitted → info_requested → assessed → paid',
  status: 'todo',
  priority: 'medium',
  assigned_to: 'claude',
  created_at: datetime()
});

// ============================================
// GITHUB & VERSION CONTROL TASKS
// ============================================

CREATE (t16:Task {
  id: 'WILL-016',
  title: 'Initialize Git repository',
  description: 'git init, .gitignore for credentials, initial commit',
  status: 'todo',
  priority: 'high',
  assigned_to: 'claude',
  created_at: datetime()
});

CREATE (t17:Task {
  id: 'WILL-017',
  title: 'Push to github.com/Pass-The-Butter/willow',
  description: 'Clear old repo, push new Willow codebase',
  status: 'todo',
  priority: 'medium',
  assigned_to: 'claude',
  created_at: datetime()
});

CREATE (t18:Task {
  id: 'WILL-018',
  title: 'Create GitHub Project kanban board',
  description: 'Columns: Backlog, Next Sprint, In Progress, Done, Frozen',
  status: 'in_progress',
  priority: 'medium',
  assigned_to: 'claude',
  created_at: datetime()
});

CREATE (t19:Task {
  id: 'WILL-019',
  title: 'Sync AuraDB tasks to GitHub Issues',
  description: 'Create GitHub issues from Task nodes, link to Project board',
  status: 'todo',
  priority: 'low',
  assigned_to: 'claude',
  created_at: datetime()
});

// ============================================
// BACKLOG / FROZEN TASKS
// ============================================

CREATE (t20:Task {
  id: 'WILL-020',
  title: 'Integrate Canva MCP for brand evolution',
  description: 'Claude can autonomously request new logos/themes from Canva',
  status: 'frozen',
  priority: 'low',
  assigned_to: 'claude',
  created_at: datetime()
});

CREATE (t21:Task {
  id: 'WILL-021',
  title: 'Build VR interface for MetaQuest 3',
  description: 'Render graph as walkable 3D space with entity sprites',
  status: 'frozen',
  priority: 'low',
  assigned_to: 'claude',
  created_at: datetime()
});

CREATE (t22:Task {
  id: 'WILL-022',
  title: 'Implement pricing engine for quotes',
  description: 'Real premium calculations (using random prices for MVP)',
  status: 'frozen',
  priority: 'low',
  assigned_to: 'claude',
  created_at: datetime()
});

CREATE (t23:Task {
  id: 'WILL-023',
  title: 'Store process documents as graph nodes',
  description: 'Assessment rules, complaint processes in graph or separate KB',
  status: 'frozen',
  priority: 'low',
  assigned_to: 'claude',
  created_at: datetime()
});

// ============================================
// TASK RELATIONSHIPS
// ============================================

// Sprint assignments
MATCH (s1:Sprint {name: 'Bootstrap'})
MATCH (t:Task) WHERE t.id IN ['WILL-001', 'WILL-002', 'WILL-003', 'WILL-004', 'WILL-005', 'WILL-006', 'WILL-016', 'WILL-017', 'WILL-018']
CREATE (s1)-[:CONTAINS_TASK]->(t);

MATCH (s2:Sprint {name: 'Population System'})
MATCH (t:Task) WHERE t.id IN ['WILL-007', 'WILL-008', 'WILL-009', 'WILL-010', 'WILL-011']
CREATE (s2)-[:CONTAINS_TASK]->(t);

MATCH (s3:Sprint {name: 'Pet Claims Journey'})
MATCH (t:Task) WHERE t.id IN ['WILL-012', 'WILL-013', 'WILL-014', 'WILL-015']
CREATE (s3)-[:CONTAINS_TASK]->(t);

// Task dependencies (blocks relationships)
MATCH (t1:Task {id: 'WILL-001'}), (t3:Task {id: 'WILL-003'})
CREATE (t3)-[:BLOCKED_BY]->(t1);

MATCH (t3:Task {id: 'WILL-003'}), (t4:Task {id: 'WILL-004'})
CREATE (t4)-[:BLOCKED_BY]->(t3);

MATCH (t3:Task {id: 'WILL-003'}), (t5:Task {id: 'WILL-005'})
CREATE (t5)-[:BLOCKED_BY]->(t3);

MATCH (t3:Task {id: 'WILL-003'}), (t6:Task {id: 'WILL-006'})
CREATE (t6)-[:BLOCKED_BY]->(t3);

MATCH (t7:Task {id: 'WILL-007'}), (t8:Task {id: 'WILL-008'})
CREATE (t8)-[:BLOCKED_BY]->(t7);

MATCH (t8:Task {id: 'WILL-008'}), (t9:Task {id: 'WILL-009'})
CREATE (t9)-[:BLOCKED_BY]->(t8);

MATCH (t9:Task {id: 'WILL-009'}), (t10:Task {id: 'WILL-010'})
CREATE (t10)-[:BLOCKED_BY]->(t9);

MATCH (t12:Task {id: 'WILL-012'}), (t13:Task {id: 'WILL-013'})
CREATE (t13)-[:BLOCKED_BY]->(t12);

// Link tasks to decisions
MATCH (t7:Task {id: 'WILL-007'}), (d:Decision {text: 'Population Database on Xeon server for synthetic customers'})
CREATE (t7)-[:IMPLEMENTS_DECISION]->(d);

MATCH (t12:Task {id: 'WILL-012'}), (d:Decision {text: 'Define ontology through Customer Journey story'})
CREATE (t12)-[:IMPLEMENTS_DECISION]->(d);

MATCH (t15:Task {id: 'WILL-015'}), (d:Decision {text: 'Use Accumulating Snapshot pattern for claim state'})
CREATE (t15)-[:IMPLEMENTS_DECISION]->(d);

// Link tasks to skills they require
MATCH (t5:Task {id: 'WILL-005'}), (s:Skill {name: 'hello_world'})
CREATE (t5)-[:TESTS_SKILL]->(s);

MATCH (t6:Task {id: 'WILL-006'}), (s:Skill {name: 'retrieve_conversation_context'})
CREATE (t6)-[:TESTS_SKILL]->(s);

MATCH (t14:Task {id: 'WILL-014'}), (s:Skill {name: 'ingest_mssql_claims'})
CREATE (t14)-[:REQUIRES_SKILL]->(s);

// Link GitHub tasks to System
MATCH (sys:System {name: 'Willow'})
MATCH (t:Task) WHERE t.id IN ['WILL-018', 'WILL-019']
CREATE (sys)-[:HAS_META_TASK]->(t);

// ============================================
// INDEXES & CONSTRAINTS
// ============================================

CREATE CONSTRAINT task_id_unique IF NOT EXISTS
FOR (t:Task) REQUIRE t.id IS UNIQUE;

CREATE INDEX task_status IF NOT EXISTS FOR (t:Task) ON (t.status);
CREATE INDEX task_priority IF NOT EXISTS FOR (t:Task) ON (t.priority);
CREATE INDEX sprint_name IF NOT EXISTS FOR (s:Sprint) ON (s.name);

// ============================================
// USEFUL QUERIES
// ============================================

// What tasks am I working on right now?
// MATCH (t:Task {status: 'in_progress', assigned_to: 'claude'}) RETURN t;

// What's blocking the skill tests?
// MATCH path = (blocker:Task)-[:BLOCKED_BY*]->(t:Task) WHERE t.id STARTS WITH 'WILL-004' RETURN path;

// What decisions led to the Population tasks?
// MATCH (t:Task)-[:IMPLEMENTS_DECISION]->(d:Decision) WHERE t.id STARTS WITH 'WILL-0' AND t.id <= 'WILL-011' RETURN t.title, d.text;

// Show all tasks in Bootstrap sprint
// MATCH (s:Sprint {name: 'Bootstrap'})-[:CONTAINS_TASK]->(t:Task) RETURN t ORDER BY t.priority DESC;

// What can I work on next? (tasks not blocked, status=todo, high priority)
// MATCH (t:Task {status: 'todo'}) WHERE NOT exists((t)-[:BLOCKED_BY]->()) AND t.priority IN ['critical', 'high'] RETURN t ORDER BY t.priority DESC;
