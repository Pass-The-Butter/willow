// Communications Domain - Telegram Integration
// N8N-powered real-time messaging for Willow agent swarm
// Created: 22 December 2025

// Domain
CREATE (d:Domain {
    name: "Communications",
    description: "Real-time messaging and notifications between agents and humans"
})

// Component
CREATE (c:Component {
    name: "Telegram Integration",
    description: "N8N-powered Telegram bot for inter-agent and human messaging",
    location: "infrastructure/telegram/"
})

// Specification
CREATE (s:Specification {
    platform: "Telegram Bot API",
    orchestration: "N8N (free trial)",
    architecture: "Webhook-based, async messaging",
    auth: "Telegram bot token + N8N webhook URLs",
    features: "Agent → Agent, Agent → Human, Human → Agent, Status updates",
    reference: "https://core.telegram.org/bots/api"
})

// Task 1: N8N Workflow Setup
CREATE (t1:Task {
    name: "N8N Workflow Setup",
    description: "Create N8N workflow with Telegram bot and webhook endpoints",
    status: "Not Started",
    priority: "High",
    estimated_hours: 2
})

CREATE (ac1:TestCriteria {
    telegram_bot: "Bot created via @BotFather, token stored in vault",
    n8n_workflow: "Workflow with Telegram trigger + webhook nodes",
    test_message: "Can send/receive test message via Telegram",
    error_handling: "Failed messages logged to organogram diary"
})

// Task 2: Agent Message Interface
CREATE (t2:Task {
    name: "Agent Message Interface",
    description: "Python skill for agents to send Telegram messages",
    status: "Not Started",
    priority: "High",
    estimated_hours: 1.5
})

CREATE (ac2:TestCriteria {
    skill_created: "core/skills/send_telegram.py with send_message(recipient, body) function",
    authentication: "Uses N8N webhook URL from .env",
    formatting: "Supports markdown formatting for code blocks and links",
    async: "Non-blocking, returns immediately"
})

// Task 3: Organogram Integration
CREATE (t3:Task {
    name: "Organogram Integration",
    description: "Mirror organogram messages to Telegram group",
    status: "Not Started",
    priority: "Medium",
    estimated_hours: 2
})

CREATE (ac3:TestCriteria {
    message_sync: "When Message node created in organogram, send to Telegram",
    formatting: "Format: [FROM] → [TO]: [SUBJECT] with body preview",
    group_setup: "Create Willow Team group with all agents + Captain",
    notifications: "High priority messages trigger notifications"
})

// Task 4: Status Broadcasting
CREATE (t4:Task {
    name: "Status Broadcasting",
    description: "Send sprint status updates and task completions to Telegram",
    status: "Not Started",
    priority: "Low",
    estimated_hours: 1
})

CREATE (ac4:TestCriteria {
    pm_integration: "PM Agent posts sprint status on completion percentage changes",
    task_completion: "Feature Agent posts when task marked complete",
    error_alerts: "System errors posted to group",
    format: "Emoji-rich, concise updates"
})

// Relationships
MATCH (p:Project {name: "Willow"})
MATCH (d:Domain {name: "Communications"})
MERGE (p)-[:HAS_DOMAIN]->(d)

MATCH (d:Domain {name: "Communications"})
MATCH (c:Component {name: "Telegram Integration"})
MERGE (d)-[:HAS_COMPONENT]->(c)

MATCH (c:Component {name: "Telegram Integration"})
MATCH (s:Specification {platform: "Telegram Bot API"})
MERGE (c)-[:HAS_SPECIFICATION]->(s)

MATCH (c:Component {name: "Telegram Integration"})
MATCH (t:Task {name: "N8N Workflow Setup"})
MERGE (c)-[:HAS_TASK]->(t)

MATCH (c:Component {name: "Telegram Integration"})
MATCH (t:Task {name: "Agent Message Interface"})
MERGE (c)-[:HAS_TASK]->(t)

MATCH (c:Component {name: "Telegram Integration"})
MATCH (t:Task {name: "Organogram Integration"})
MERGE (c)-[:HAS_TASK]->(t)

MATCH (c:Component {name: "Telegram Integration"})
MATCH (t:Task {name: "Status Broadcasting"})
MERGE (c)-[:HAS_TASK]->(t)

// Acceptance Criteria
MATCH (t:Task {name: "N8N Workflow Setup"})
MATCH (ac:TestCriteria {telegram_bot: "Bot created via @BotFather, token stored in vault"})
MERGE (t)-[:HAS_ACCEPTANCE_CRITERIA]->(ac)

MATCH (t:Task {name: "Agent Message Interface"})
MATCH (ac:TestCriteria {skill_created: "core/skills/send_telegram.py with send_message(recipient, body) function"})
MERGE (t)-[:HAS_ACCEPTANCE_CRITERIA]->(ac)

MATCH (t:Task {name: "Organogram Integration"})
MATCH (ac:TestCriteria {message_sync: "When Message node created in organogram, send to Telegram"})
MERGE (t)-[:HAS_ACCEPTANCE_CRITERIA]->(ac)

MATCH (t:Task {name: "Status Broadcasting"})
MATCH (ac:TestCriteria {pm_integration: "PM Agent posts sprint status on completion percentage changes"})
MERGE (t)-[:HAS_ACCEPTANCE_CRITERIA]->(ac)

// Dependencies
MATCH (t:Task {name: "Agent Message Interface"})
MATCH (t2:Task {name: "N8N Workflow Setup"})
MERGE (t)-[:DEPENDS_ON]->(t2)

MATCH (t:Task {name: "Organogram Integration"})
MATCH (t2:Task {name: "Agent Message Interface"})
MERGE (t)-[:DEPENDS_ON]->(t2)

MATCH (t:Task {name: "Status Broadcasting"})
MATCH (t2:Task {name: "Organogram Integration"})
MERGE (t)-[:DEPENDS_ON]->(t2)
