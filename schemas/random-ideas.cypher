// Willow Random Ideas & Future Enhancements
// Capturing all brainstorm ideas so they don't get lost
// These can be promoted to Tasks when ready

// ============================================
// DISTRIBUTED AGENT IDEAS
// ============================================

CREATE (idea1:RandomIdea {
  title: 'Any agent, anywhere can work on tasks via graph query',
  description: 'GitHub PR agent, AntiGravity Claude, cloud agents, N8N workflows - all query the same Task nodes. Fully distributed task execution.',
  category: 'meta-system',
  source: 'Peter insight - Dec 21',
  potential_impact: 'high',
  status: 'concept',
  created_at: datetime()
});

CREATE (idea2:RandomIdea {
  title: 'Email-triggered claim status updates',
  description: 'Cloud agent watches email inbox. When claim documents arrive, automatically updates Claim node status in graph. No human intervention.',
  category: 'automation',
  source: 'Peter example - Dec 21',
  potential_impact: 'high',
  status: 'concept',
  created_at: datetime()
});

CREATE (idea3:RandomIdea {
  title: 'Personalized user graphics generation',
  description: 'Agent detects Doris in Accounts turned 60, generates custom birthday SVG sprite, updates her User node. N8N workflow triggered by date change.',
  category: 'personalization',
  source: 'Peter example - Dec 21',
  potential_impact: 'medium',
  status: 'concept',
  created_at: datetime()
});

// ============================================
// VR & VISUALIZATION IDEAS
// ============================================

CREATE (idea4:RandomIdea {
  title: 'MetaQuest 3 VR graph visualization',
  description: 'Render entire graph as walkable 3D space. Each entity has sprite model. Real-time multi-user MMOG-style interface.',
  category: 'vr-interface',
  source: 'Peter vision - Dec 21',
  potential_impact: 'high',
  status: 'frozen',
  related_tasks: ['WILL-021'],
  created_at: datetime()
});

CREATE (idea5:RandomIdea {
  title: 'N8N agents generate SVG sprites for entities',
  description: 'When new entity created in graph, N8N workflow triggers local agent to generate SVG sprite. Stored in node property: sprite_svg or sprite_url.',
  category: 'automation',
  source: 'Peter idea - Dec 21',
  potential_impact: 'medium',
  status: 'concept',
  created_at: datetime()
});

CREATE (idea6:RandomIdea {
  title: 'Real-time event stream for VR synchronization',
  description: 'GraphEvent nodes capture all changes (NODE_CREATED, PROPERTY_UPDATED). VR clients subscribe to event stream via WebSocket. Multi-user sees changes live.',
  category: 'vr-interface',
  source: 'Architecture discussion - Dec 21',
  potential_impact: 'medium',
  status: 'concept',
  created_at: datetime()
});

CREATE (idea7:RandomIdea {
  title: 'Every entity has 3D sprite model',
  description: 'Customer, Pet, Claim, Vet, Skill - all have sprite_model property (e.g., willow_tree.glb). Spatial position {x,y,z}, color, scale for VR rendering.',
  category: 'vr-interface',
  source: 'Architecture discussion - Dec 21',
  potential_impact: 'medium',
  status: 'concept',
  created_at: datetime()
});

// ============================================
// POPULATION & NPC IDEAS
// ============================================

CREATE (idea8:RandomIdea {
  title: 'NPCs as evolving Sims characters',
  description: 'Population starts with basic demographics. Over time, NPCs develop personalities, preferences, life events. Vector personalities evolve based on interactions.',
  category: 'population',
  source: 'Peter vision - Dec 21',
  potential_impact: 'medium',
  status: 'concept',
  created_at: datetime()
});

CREATE (idea9:RandomIdea {
  title: 'Infinite Library pattern for NPC creation',
  description: 'Alternative to pre-generating 10M NPCs: Create NPCs on-demand when needed. Challenge: Need to know global stats (e.g., nut allergy prevalence) before creation.',
  category: 'population',
  source: 'Peter consideration - Dec 21',
  potential_impact: 'low',
  status: 'rejected',
  rejection_reason: 'Pre-generation simpler for MVP, allows realistic distributions',
  created_at: datetime()
});

CREATE (idea10:RandomIdea {
  title: 'Vector similarity for marketing segmentation',
  description: 'Find similar customers via personality vectors: cat lovers, allergy sufferers, political views. Enable targeted marketing campaigns based on similarity search.',
  category: 'marketing',
  source: 'Peter requirement - Dec 21',
  potential_impact: 'high',
  status: 'planned',
  related_tasks: ['WILL-011'],
  created_at: datetime()
});

// ============================================
// BRAND & DESIGN IDEAS
// ============================================

CREATE (idea11:RandomIdea {
  title: 'Canva MCP for autonomous brand evolution',
  description: 'Claude queries BrandAsset nodes, requests new seasonal themes from Canva via MCP. Brand evolves autonomously based on context (season, campaigns, events).',
  category: 'brand',
  source: 'Handover doc + discussion - Dec 21',
  potential_impact: 'medium',
  status: 'frozen',
  related_tasks: ['WILL-020'],
  created_at: datetime()
});

CREATE (idea12:RandomIdea {
  title: 'Brand evolution timeline in graph',
  description: 'BrandAsset nodes linked via EVOLVED_FROM relationships. Track design lineage: autumn_v1 → autumn_v2 → autumn_v3. Historical brand audit trail.',
  category: 'brand',
  source: 'Architecture discussion - Dec 21',
  potential_impact: 'low',
  status: 'concept',
  created_at: datetime()
});

// ============================================
// SKILL SYSTEM IDEAS
// ============================================

CREATE (idea13:RandomIdea {
  title: 'Skill-creation-skill (meta-skill)',
  description: 'A skill that writes new skills and stores them as nodes. Claude creates hello_world_v2, saves code to /skills, creates Skill node. Self-modifying system.',
  category: 'meta-system',
  source: 'Architecture discussion - Dec 21',
  potential_impact: 'high',
  status: 'concept',
  created_at: datetime()
});

CREATE (idea14:RandomIdea {
  title: 'Skills linked via CREATED_BY relationships',
  description: 'Track skill lineage: which skill created which other skill. Skill genealogy tree. Meta-insight into system evolution.',
  category: 'meta-system',
  source: 'Architecture discussion - Dec 21',
  potential_impact: 'low',
  status: 'concept',
  created_at: datetime()
});

// ============================================
// ONTOLOGY & DATA MODELING IDEAS
// ============================================

CREATE (idea15:RandomIdea {
  title: 'Department ACLs (Palantir/Timbr strategy)',
  description: 'Same graph, different security scopes. Claims dept sees customer journey, Underwriting sees risk models, Vets see treatments. Sub-ontology views via AuraDB ACLs.',
  category: 'security',
  source: 'Peter strategy - Dec 21',
  potential_impact: 'high',
  status: 'concept',
  created_at: datetime()
});

CREATE (idea16:RandomIdea {
  title: 'Process documents stored as graph nodes',
  description: 'Assessment rules, complaint processes, underwriting guidelines stored in graph. Or separate knowledge graph with cross-references. Queryable policy documents.',
  category: 'knowledge-management',
  source: 'Peter idea - Dec 21',
  potential_impact: 'medium',
  status: 'frozen',
  related_tasks: ['WILL-023'],
  created_at: datetime()
});

CREATE (idea17:RandomIdea {
  title: 'Multi-graph architecture for separate domains',
  description: 'Main Willow graph for operations. Separate graphs for: knowledge base, audit logs, historical archives. Graphs reference each other via federation.',
  category: 'architecture',
  source: 'Peter consideration - Dec 21',
  potential_impact: 'low',
  status: 'concept',
  notes: 'Keep single graph with ACLs first, only split if performance requires',
  created_at: datetime()
});

CREATE (idea18:RandomIdea {
  title: 'Customer journey story defines ontology',
  description: 'Rather than business-first modeling, design graph around customer experience. Jerry finds Barry → Quote → Policy → Claim. Story IS the schema.',
  category: 'ontology-design',
  source: 'Peter philosophy - Dec 21',
  potential_impact: 'high',
  status: 'adopted',
  related_tasks: ['WILL-012', 'WILL-013'],
  created_at: datetime()
});

// ============================================
// INFRASTRUCTURE IDEAS
// ============================================

CREATE (idea19:RandomIdea {
  title: 'Google Cloud Run for serverless Willow API',
  description: 'Deploy Willow API as serverless container on Cloud Run. Auto-scaling, pay-per-use. Triggered by graph events or HTTP requests.',
  category: 'infrastructure',
  source: 'Peter resources - Dec 21',
  potential_impact: 'low',
  status: 'concept',
  notes: 'Docker-based API works fine for MVP, Cloud Run for production scale',
  created_at: datetime()
});

CREATE (idea20:RandomIdea {
  title: 'Local Ollama agent for bulk NPC generation',
  description: 'RTX 3090 Ti runs Ollama locally via Tailscale. Handles Faker-based generation of 10M NPCs. Saves Claude credits, faster parallel generation.',
  category: 'population',
  source: 'Peter resources - Dec 21',
  potential_impact: 'high',
  status: 'adopted',
  related_tasks: ['WILL-009', 'WILL-010'],
  created_at: datetime()
});

CREATE (idea21:RandomIdea {
  title: 'Sora integration for VR enhancements',
  description: 'Use Sora (OpenAI video generation) to create dynamic visualizations for VR interface. Generate animated customer journeys, claim flow videos.',
  category: 'vr-interface',
  source: 'Peter resources - Dec 21',
  potential_impact: 'low',
  status: 'frozen',
  notes: 'Cool but not MVP critical',
  created_at: datetime()
});

// ============================================
// RELATIONSHIPS TO EXISTING NODES
// ============================================

// Link ideas to System
MATCH (sys:System {name: 'Willow'})
MATCH (idea:RandomIdea)
CREATE (sys)-[:HAS_FUTURE_IDEA]->(idea);

// Link high-impact ideas to Insights
MATCH (idea1:RandomIdea {title: 'Any agent, anywhere can work on tasks via graph query'})
CREATE (insight:Insight {
  text: 'Graph-based specification enables distributed agent coordination',
  description: 'By storing tasks, decisions, and skills as nodes, any agent (GitHub, Claude, N8N, cloud) can query what needs doing and execute autonomously.',
  category: 'distributed-systems',
  created_at: datetime()
})
CREATE (idea1)-[:INSPIRED_INSIGHT]->(insight);

MATCH (idea18:RandomIdea {title: 'Customer journey story defines ontology'})
MATCH (insight:Insight {text: 'Graph ontologies enable systems to be self-aware'})
CREATE (idea18)-[:INSPIRED_INSIGHT]->(insight);

// Link adopted ideas to related tasks
MATCH (idea20:RandomIdea {title: 'Local Ollama agent for bulk NPC generation'})
MATCH (t:Task {id: 'WILL-009'})
CREATE (idea20)-[:IMPLEMENTED_BY_TASK]->(t);

MATCH (idea18:RandomIdea {title: 'Customer journey story defines ontology'})
MATCH (t:Task {id: 'WILL-012'})
CREATE (idea18)-[:IMPLEMENTED_BY_TASK]->(t);

// ============================================
// INDEXES
// ============================================

CREATE INDEX random_idea_category IF NOT EXISTS FOR (r:RandomIdea) ON (r.category);
CREATE INDEX random_idea_status IF NOT EXISTS FOR (r:RandomIdea) ON (r.status);
CREATE INDEX random_idea_impact IF NOT EXISTS FOR (r:RandomIdea) ON (r.potential_impact);

// ============================================
// USEFUL QUERIES
// ============================================

// Show all high-impact ideas still in concept phase
// MATCH (r:RandomIdea {potential_impact: 'high', status: 'concept'}) RETURN r.title, r.description;

// Find ideas by category
// MATCH (r:RandomIdea {category: 'vr-interface'}) RETURN r.title, r.status;

// Show adopted ideas and their implementing tasks
// MATCH (r:RandomIdea {status: 'adopted'})-[:IMPLEMENTED_BY_TASK]->(t:Task) RETURN r.title, t.id, t.status;

// Ideas that became insights
// MATCH (r:RandomIdea)-[:INSPIRED_INSIGHT]->(i:Insight) RETURN r.title, i.text;
