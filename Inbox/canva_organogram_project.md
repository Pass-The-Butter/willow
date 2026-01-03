# WILLOW ORGANOGRAM CANVA PROJECT
## Ready-to-Deploy Meeseeks Project Definition

**Copy this entire YAML block and feed it to your Meeseeks PM agent.**

---

```yaml
PROJECT_DEFINITION:
  name: "Willow Organogram Canva Visualizer"
  
  goal: |
    Create a professional, interactive organizational chart in Canva that:
    1. Visualizes the complete Willow project structure from Neo4j AuraDB
    2. Shows hierarchy: Project → Domains → Components → Tasks
    3. Uses Willow brand identity (colors, fonts, styling)
    4. Is readable, shareable, and updatable
    5. Can be regenerated when graph changes
  
  constraints:
    budget:
      - "Must use free Canva tier - no premium features"
      - "No additional tools or services requiring payment"
    
    technical:
      - "Cannot connect Canva directly to Neo4j (use export/import pattern)"
      - "Must handle ~10 domains, ~30 components, ~100 tasks"
      - "Must remain performant with future growth to 500+ nodes"
    
    branding:
      - "MUST use Willow brand kit ID: kAG8Kb3PjZ4"
      - "Follow Willow-Autumn theme where applicable"
    
    timeline:
      - "Complete in single work session (3-4 hours max)"
      - "Each iteration must be completable in < 1 hour"
  
  deliverables:
    1_data_extraction:
      file: "organogram_export.py"
      purpose: "Python script to query Neo4j and extract structure"
      requirements:
        - "Uses credentials from /Volumes/Delila/dev/Willow/.env"
        - "Queries complete Project → Domain → Component → Task hierarchy"
        - "Includes metadata: status, assignee, completion percentage"
        - "Exports to JSON format optimized for Canva consumption"
        - "Handles missing/optional fields gracefully"
        - "Includes example data for testing without DB connection"
    
    2_canva_generator:
      file: "canva_organogram_builder.py"
      purpose: "Script to create Canva chart from exported data"
      requirements:
        - "Uses Canva MCP/API integration if available"
        - "Applies Willow brand kit automatically"
        - "Creates hierarchical layout (tree structure)"
        - "Adds color coding by domain"
        - "Includes status indicators (icons/colors)"
        - "Generates shareable link"
        - "Stores design ID for future updates"
    
    3_canva_chart:
      type: "Canva Design"
      purpose: "The actual organizational chart visualization"
      requirements:
        - "Complete hierarchy visible"
        - "Nodes show: name, type, status"
        - "Relationships clearly indicated"
        - "Responsive layout (works at different zoom levels)"
        - "Legend explaining color codes and status icons"
        - "Willow branding prominent"
    
    4_documentation:
      file: "README_organogram.md"
      purpose: "User guide for Peter"
      requirements:
        - "How to run extraction script"
        - "How to regenerate chart when data changes"
        - "How to customize appearance in Canva"
        - "Troubleshooting common issues"
        - "Future enhancement suggestions"
  
  acceptance_criteria:
    data_extraction:
      - criterion: "Script connects to Neo4j using .env credentials"
        test: "Run script, verify no connection errors"
        evidence: "Console output showing successful connection"
      
      - criterion: "Extracts complete graph structure"
        test: "Inspect JSON output, count nodes at each level"
        evidence: "JSON file with expected node counts matching current DB state"
      
      - criterion: "Handles edge cases (missing assignees, null status)"
        test: "Check JSON for defensive handling of optional fields"
        evidence: "JSON validates without null errors"
      
      - criterion: "Export completes in < 30 seconds"
        test: "Time script execution"
        evidence: "Timestamp logs showing < 30s runtime"
    
    canva_creation:
      - criterion: "Chart uses Willow brand kit"
        test: "Inspect Canva design, verify brand kit ID in metadata"
        evidence: "Screenshot showing brand colors/fonts applied"
      
      - criterion: "All domains visible as top-level nodes"
        test: "Count domain nodes in chart"
        evidence: "Visual confirmation + node count = JSON export count"
      
      - criterion: "Components nest under correct domains"
        test: "Verify parent-child relationships match graph"
        evidence: "Side-by-side comparison of JSON hierarchy vs Canva layout"
      
      - criterion: "Tasks show status accurately"
        test: "Spot-check 10 random tasks in chart vs Neo4j"
        evidence: "List showing task name, chart status, DB status (must match)"
      
      - criterion: "Chart is readable with 100+ nodes"
        test: "View at 100%, 50%, 25% zoom"
        evidence: "Screenshots at each zoom level showing text remains readable"
      
      - criterion: "Shareable link works"
        test: "Open link in incognito browser"
        evidence: "Incognito screenshot of chart loading successfully"
    
    regeneration:
      - criterion: "Can update chart when data changes"
        test: "Modify test task in Neo4j, re-run scripts, verify change appears in chart"
        evidence: "Before/after screenshots showing updated task"
      
      - criterion: "Documentation is self-sufficient"
        test: "Follow README steps without prior knowledge"
        evidence: "Third-party confirmation or detailed step-by-step execution log"
  
  context:
    neo4j_access:
      uri: "neo4j+s://e59298d2.databases.neo4j.io"
      credentials_location: "/Volumes/Delila/dev/Willow/.env"
      note: "Full credentials available in .env file (NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)"
    
    current_graph_structure:
      schema: |
        (:Project)-[:HAS_DOMAIN]->(:Domain)
        (:Domain)-[:HAS_COMPONENT]->(:Component)
        (:Component)-[:HAS_TASK]->(:Task)
      
      typical_counts:
        domains: "~10"
        components: "~30" 
        tasks: "~100"
      
      node_properties:
        Project: "name"
        Domain: "name, description"
        Component: "name, description"
        Task: "name, status, assignee, completed_at, priority"
    
    canva_integration:
      brand_kit_id: "kAG8Kb3PjZ4"
      brand_name: "Willow"
      available_tools: "Claude has Canva connector with generate, export, create capabilities"
      
    willow_theme:
      primary_colors: "Autumn palette (warm oranges, browns, golds)"
      style: "Professional yet approachable, data-driven, clean"
    
    reference_files:
      bios: "/Volumes/Delila/dev/Willow/BIOS.md"
      tier_zero: "/Volumes/Delila/Projects/willow-baton/tier_zero/personality_tier_zero.md"
      ontology: "/Volumes/Delila/Projects/willow-baton/ontology/ontology.json"
    
    success_examples:
      good_organogram: "Clear hierarchy, intuitive navigation, status at-a-glance"
      bad_organogram: "Cluttered, hard to read, static/non-updatable"
  
  technical_notes:
    python_environment:
      - "Python 3.12 available"
      - "neo4j driver must be installed: pip install neo4j certifi"
      - "Prefer standard library where possible"
    
    canva_api:
      - "Use Claude's Canva connector tools (generate-design, export-design)"
      - "Alternative: generate JSON, manual import (less ideal)"
      - "Export formats: PDF, PNG, or shareable link preferred"
    
    data_flow:
      - "Neo4j → Python export script → JSON file"
      - "JSON file → Canva builder script → Canva design"
      - "Canva design → Shareable link + downloadable export"
    
    performance_considerations:
      - "Large graphs: consider collapsible sections or multi-page designs"
      - "Initial load: query optimization (use LIMIT for testing)"
      - "Future: pagination or domain-filtered views"
  
  risks_and_mitigations:
    risk_1:
      issue: "Canva may not support programmatic creation of org charts"
      mitigation: "Fall back to CSV/JSON export + manual import workflow"
      impact: "Medium - requires manual step but still achievable"
    
    risk_2:
      issue: "Graph too large for single chart"
      mitigation: "Create domain-specific sub-charts or use collapsible sections"
      impact: "Low - can iterate on visualization strategy"
    
    risk_3:
      issue: "Neo4j connection issues from sandbox"
      mitigation: "Peter runs extraction script locally, provides JSON to agent"
      impact: "Low - workflow adjustment only"

  iteration_strategy:
    iteration_1:
      focus: "Get basic extraction and simple chart working"
      deliverable: "Proof of concept with test data"
    
    iteration_2:
      focus: "Add branding, improve layout, status indicators"
      deliverable: "Polished chart with Willow theme"
    
    iteration_3:
      focus: "Documentation, regeneration workflow, edge case handling"
      deliverable: "Complete system ready for production use"
```

---

## USAGE

### Deploy this project:

```bash
# In Claude Code with Meeseeks agents configured:

"Use the meeseeks-pm-willow-organogram agent with this project definition:

[PASTE THE YAML ABOVE]
"
```

### The system will:

1. **PM analyzes** requirements, researches Canva best practices
2. **PM creates** implementation brief for Implementer
3. **Implementer builds** extraction script, Canva generator, chart
4. **PM spawns Tester** to validate each acceptance criterion
5. **If tests fail**, PM creates correction brief (up to 3 iterations)
6. **PM reports** final status to Peter

### Expected Outputs:

```
/Volumes/Delila/dev/Willow/organogram/
├── organogram_export.py          # Neo4j extraction script
├── canva_organogram_builder.py   # Chart generator
├── willow_organogram_data.json   # Exported graph structure
├── README_organogram.md          # User documentation
└── .canva_design_id              # For future updates
```

Plus: Shareable Canva link to live organizational chart

---

## CUSTOMIZATION NOTES

### To focus on different aspects:

**Want faster iterations?**
- Reduce complexity in acceptance_criteria
- Simplify deliverables to MVP only

**Need different output format?**
- Modify deliverable 3 to specify PDF, PNG, or interactive HTML

**Different brand theme?**
- Update canva_integration.brand_kit_id
- Adjust willow_theme colors

### To use with different graph structures:

- Update current_graph_structure section
- Modify typical_counts to match your data
- Adjust acceptance criteria node counts

---

**This is a complete, production-ready Meeseeks project definition.**

Just feed it to your PM agent and watch the swarm work.
