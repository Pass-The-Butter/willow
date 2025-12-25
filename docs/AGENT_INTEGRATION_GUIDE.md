# Agent Integration Guide

**How to work AS an agent in the Willow system**

Anyone (human or machine) can be an agent:
- You (Peter) can create tasks, update status, integrate with Jira
- Claude (Arch-Willow) coordinates via graph
- Ollama generates data in background
- GitHub automation creates PRs
- Jira syncs tickets bidirectionally
- Slack posts notifications
- N8N orchestrates workflows

**The pattern is always the same**: Query graph → Do work → Update graph

---

## Pattern 1: You As An Agent (Human)

### Via GitHub (Easiest)
```bash
1. Browse kanban: github.com/Pass-The-Butter/willow/projects
2. Pick a task: WILL-002 "Fix autumn BrandAsset"
3. Create branch: git checkout -b fix/will-002-autumn-brand
4. Do the work
5. Create PR, link to issue #2
6. GitHub Actions syncs status back to AuraDB
```

### Via AuraDB Direct (Advanced)
```python
# Query what you should work on
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
    "neo4j+s://e59298d2.databases.neo4j.io",
    auth=("neo4j", "PASSWORD")
)

with driver.session() as session:
    # What tasks are available?
    result = session.run("""
        MATCH (t:Task {status: 'todo', assigned_to: 'peter'})
        WHERE NOT exists((t)-[:BLOCKED_BY]->())
        RETURN t.id, t.title, t.priority
        ORDER BY t.priority DESC
        LIMIT 5
    """)

    for record in result:
        print(f"{record['t.id']}: {record['t.title']}")

    # Pick one and mark in progress
    session.run("""
        MATCH (t:Task {id: 'WILL-002'})
        SET t.status = 'in_progress',
            t.started_at = datetime()
    """)

    # Do the work...

    # Mark complete
    session.run("""
        MATCH (t:Task {id: 'WILL-002'})
        SET t.status = 'completed',
            t.completed_at = datetime()
    """)
```

### Via CLI Tool (To Be Built)
```bash
# Future: Willow CLI
willow tasks list --assigned-to peter --status todo
willow tasks start WILL-002
# ... do the work ...
willow tasks complete WILL-002 "Fixed BrandAsset URL syntax"
```

---

## Pattern 2: Jira Integration

### Goal
Sync Willow tasks ↔ Jira tickets bidirectionally

### Architecture
```
Willow (AuraDB)
    ↕ (webhook/API)
Sync Service (N8N workflow or Cloud Function)
    ↕ (Jira REST API)
Jira (tickets)
```

### Implementation Option A: N8N Workflow

**Trigger**: New Task node created in AuraDB
**Action**: Create Jira ticket

```javascript
// N8N workflow nodes:

// 1. Webhook: Listen for AuraDB task creation
//    URL: https://agilemesh.app.n8n.cloud/webhook/willow-task-created

// 2. Cypher Query: Get task details
const taskQuery = `
  MATCH (t:Task {id: $taskId})
  RETURN t.id as id,
         t.title as title,
         t.description as description,
         t.priority as priority,
         t.status as status
`;

// 3. Jira API: Create issue
const jiraPayload = {
  "fields": {
    "project": { "key": "WILLOW" },
    "summary": taskTitle,
    "description": taskDescription,
    "issuetype": { "name": "Task" },
    "priority": { "name": mapPriority(taskPriority) },
    "labels": ["willow", `task-${taskId}`]
  }
};

// 4. Update AuraDB: Store Jira ticket key
const updateQuery = `
  MATCH (t:Task {id: $taskId})
  SET t.jira_key = $jiraKey,
      t.jira_url = $jiraUrl
`;

// 5. Webhook Response: Success
```

**Reverse sync** (Jira → Willow):
```javascript
// Jira webhook on issue update
// Triggers N8N workflow
// Updates AuraDB Task node status
```

### Implementation Option B: Cloud Function

**Deploy to Google Cloud Run**:
```python
# sync_jira.py
from flask import Flask, request
from neo4j import GraphDatabase
from jira import JIRA

app = Flask(__name__)

neo4j_driver = GraphDatabase.driver(NEO4J_URI, auth=(USER, PASS))
jira_client = JIRA(JIRA_URL, basic_auth=(JIRA_USER, JIRA_TOKEN))

@app.route('/webhook/task-created', methods=['POST'])
def task_created():
    """AuraDB webhook: Task created → Create Jira ticket"""
    task_id = request.json['task_id']

    # Get task from graph
    with neo4j_driver.session() as session:
        result = session.run("""
            MATCH (t:Task {id: $task_id})
            RETURN t.title, t.description, t.priority
        """, task_id=task_id)
        task = result.single()

    # Create Jira issue
    issue = jira_client.create_issue(
        project='WILLOW',
        summary=task['t.title'],
        description=task['t.description'],
        issuetype={'name': 'Task'},
        labels=['willow', f'task-{task_id}']
    )

    # Update graph with Jira key
    with neo4j_driver.session() as session:
        session.run("""
            MATCH (t:Task {id: $task_id})
            SET t.jira_key = $jira_key,
                t.jira_url = $jira_url
        """, task_id=task_id, jira_key=issue.key, jira_url=issue.permalink())

    return {'status': 'success', 'jira_key': issue.key}

@app.route('/webhook/jira-updated', methods=['POST'])
def jira_updated():
    """Jira webhook: Issue updated → Update AuraDB"""
    jira_key = request.json['issue']['key']
    new_status = request.json['issue']['fields']['status']['name']

    # Map Jira status to Willow status
    status_map = {
        'To Do': 'todo',
        'In Progress': 'in_progress',
        'Done': 'completed'
    }
    willow_status = status_map.get(new_status, 'todo')

    # Update graph
    with neo4j_driver.session() as session:
        session.run("""
            MATCH (t:Task {jira_key: $jira_key})
            SET t.status = $status,
                t.updated_at = datetime()
        """, jira_key=jira_key, status=willow_status)

    return {'status': 'success'}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
```

**Deploy**:
```bash
# Build container
docker build -t willow-jira-sync .

# Push to Google Container Registry
docker tag willow-jira-sync gcr.io/YOUR-PROJECT/willow-jira-sync
docker push gcr.io/YOUR-PROJECT/willow-jira-sync

# Deploy to Cloud Run
gcloud run deploy willow-jira-sync \
  --image gcr.io/YOUR-PROJECT/willow-jira-sync \
  --platform managed \
  --allow-unauthenticated \
  --set-env-vars NEO4J_URI=...,JIRA_URL=...
```

---

## Pattern 3: Linear Integration

Similar to Jira, but using Linear's GraphQL API:

```graphql
# Create Linear issue from Willow task
mutation CreateIssue($teamId: String!, $title: String!, $description: String!) {
  issueCreate(input: {
    teamId: $teamId
    title: $title
    description: $description
    labelIds: ["willow-task"]
  }) {
    success
    issue {
      id
      identifier
      url
    }
  }
}
```

**N8N node**: Linear app → "Create Issue"

---

## Pattern 4: Slack Notifications

### When task created
```javascript
// N8N workflow
// Trigger: Task created in AuraDB
// Action: Post to Slack

const slackMessage = {
  "channel": "#willow-tasks",
  "text": `New task created: ${taskTitle}`,
  "blocks": [
    {
      "type": "section",
      "text": {
        "type": "mrkdwn",
        "text": `*${taskId}: ${taskTitle}*\n${taskDescription}\n\nPriority: ${priority}\nStatus: ${status}`
      }
    },
    {
      "type": "actions",
      "elements": [
        {
          "type": "button",
          "text": { "type": "plain_text", "text": "Claim Task" },
          "action_id": "claim_task",
          "value": taskId
        },
        {
          "type": "button",
          "text": { "type": "plain_text", "text": "View in Graph" },
          "url": `https://console.neo4j.io/...`
        }
      ]
    }
  ]
};
```

### Interactive button
```python
# When user clicks "Claim Task" button
@app.route('/slack/interactive', methods=['POST'])
def slack_interactive():
    payload = json.loads(request.form['payload'])
    task_id = payload['actions'][0]['value']
    user_id = payload['user']['id']

    # Get Slack user's real name
    slack_client = WebClient(token=SLACK_BOT_TOKEN)
    user_info = slack_client.users_info(user=user_id)
    user_name = user_info['user']['real_name']

    # Update graph
    with neo4j_driver.session() as session:
        session.run("""
            MATCH (t:Task {id: $task_id})
            SET t.assigned_to = $user_name,
                t.status = 'in_progress',
                t.started_at = datetime()
        """, task_id=task_id, user_name=user_name)

    return {"text": f"{user_name} claimed task {task_id}!"}
```

---

## Pattern 5: GitHub Codespaces Integration

### Automatic branch creation
```yaml
# .github/workflows/task-to-branch.yml
name: Task to Branch

on:
  issues:
    types: [labeled]

jobs:
  create-branch:
    if: contains(github.event.issue.labels.*.name, 'task')
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2

      - name: Extract task ID
        id: task
        run: |
          TASK_ID=$(echo "${{ github.event.issue.title }}" | grep -oP 'WILL-\d+')
          echo "task_id=$TASK_ID" >> $GITHUB_OUTPUT

      - name: Create branch
        run: |
          BRANCH_NAME="task/${{ steps.task.outputs.task_id }}-$(echo '${{ github.event.issue.title }}' | sed 's/WILL-[0-9]*: //' | tr ' ' '-' | tr '[:upper:]' '[:lower:]')"
          git checkout -b "$BRANCH_NAME"
          git push origin "$BRANCH_NAME"

      - name: Comment on issue
        uses: actions/github-script@v6
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: `Branch created: \`${process.env.BRANCH_NAME}\`\n\nOpen in Codespaces: [Start coding](https://github.com/codespaces/new?ref=${process.env.BRANCH_NAME})`
            })
```

---

## Pattern 6: OpenAI Codex Integration

### AI pair programming on tasks
```python
# codex_agent.py
import openai
from neo4j import GraphDatabase

def codex_agent_work_on_task(task_id):
    """Use Codex to implement a task"""

    # Get task details from graph
    with neo4j_driver.session() as session:
        result = session.run("""
            MATCH (t:Task {id: $task_id})
            RETURN t.title, t.description, t.related_skills
        """, task_id=task_id)
        task = result.single()

    # Generate code using Codex
    prompt = f"""
    Task: {task['t.title']}
    Description: {task['t.description']}

    Generate Python code to implement this task.
    Follow Willow coding standards.
    Include error handling and logging.
    """

    response = openai.Completion.create(
        model="code-davinci-002",
        prompt=prompt,
        max_tokens=500
    )

    generated_code = response.choices[0].text

    # Save to file
    filename = f"skills/{task_id.lower().replace('-', '_')}.py"
    with open(filename, 'w') as f:
        f.write(generated_code)

    # Create PR
    # ... GitHub API to create PR ...

    return filename
```

---

## Pattern 7: Email-Driven Task Creation

### Forward email → Create task
```python
# email_to_task.py (N8N or Cloud Function)
import imaplib
import email
from neo4j import GraphDatabase

def check_inbox():
    """Monitor inbox, create tasks from emails"""

    # Connect to email
    mail = imaplib.IMAP4_SSL('imap.gmail.com')
    mail.login('willow@company.com', PASSWORD)
    mail.select('inbox')

    # Search for unread emails with [WILLOW-TASK] in subject
    _, messages = mail.search(None, '(UNSEEN SUBJECT "[WILLOW-TASK]")')

    for msg_id in messages[0].split():
        # Fetch email
        _, msg_data = mail.fetch(msg_id, '(RFC822)')
        email_body = msg_data[0][1]
        email_message = email.message_from_bytes(email_body)

        # Parse
        subject = email_message['subject'].replace('[WILLOW-TASK]', '').strip()
        body = email_message.get_payload()
        sender = email_message['from']

        # Create task in graph
        task_id = generate_task_id()  # e.g., WILL-025

        with neo4j_driver.session() as session:
            session.run("""
                CREATE (t:Task {
                    id: $task_id,
                    title: $title,
                    description: $body,
                    requested_by: $sender,
                    status: 'todo',
                    priority: 'medium',
                    created_at: datetime(),
                    source: 'email'
                })

                MATCH (sys:System {name: 'Willow'})
                MATCH (s:Sprint {status: 'active'})
                CREATE (s)-[:CONTAINS_TASK]->(t)
            """, task_id=task_id, title=subject, body=body, sender=sender)

        # Mark email as read
        mail.store(msg_id, '+FLAGS', '\\Seen')

        # Reply to sender
        send_email(
            to=sender,
            subject=f"Task Created: {task_id}",
            body=f"Your request has been created as task {task_id}.\n\nView: https://github.com/Pass-The-Butter/willow/issues/{task_id}"
        )
```

**Usage**:
```
From: peter@semanticarts.com
To: willow@company.com
Subject: [WILLOW-TASK] Add pricing engine for quotes

Hi Willow,

We need a pricing engine that calculates premiums based on:
- Pet age
- Breed risk factors
- Coverage type
- Excess amount

Can you create a task for this?

Thanks,
Peter
```

Result: Creates WILL-025 automatically

---

## Pattern 8: Voice-Activated Task Management

### Alexa/Google Home skill
```python
# alexa_skill.py
from ask_sdk_core.skill_builder import SkillBuilder
from neo4j import GraphDatabase

sb = SkillBuilder()

@sb.request_handler(can_handle_func=lambda input:
    input.request_type == "IntentRequest" and
    input.intent.name == "WhatAreMyTasks")
def what_are_my_tasks_handler(handler_input):
    """Alexa, ask Willow what my tasks are"""

    with neo4j_driver.session() as session:
        result = session.run("""
            MATCH (t:Task {assigned_to: 'peter', status: 'todo'})
            WHERE NOT exists((t)-[:BLOCKED_BY]->())
            RETURN t.id, t.title, t.priority
            ORDER BY t.priority DESC
            LIMIT 3
        """)

        tasks = []
        for record in result:
            tasks.append(f"{record['t.id']}: {record['t.title']}")

        if tasks:
            speech = f"You have {len(tasks)} tasks. " + ". ".join(tasks)
        else:
            speech = "You have no pending tasks. Great job!"

    return handler_input.response_builder.speak(speech).response

@sb.request_handler(can_handle_func=lambda input:
    input.request_type == "IntentRequest" and
    input.intent.name == "CompleteTask")
def complete_task_handler(handler_input):
    """Alexa, tell Willow I completed task WILL-001"""

    task_id = handler_input.request.intent.slots['task_id'].value

    with neo4j_driver.session() as session:
        session.run("""
            MATCH (t:Task {id: $task_id})
            SET t.status = 'completed',
                t.completed_at = datetime()
        """, task_id=task_id)

    speech = f"Marked {task_id} as completed. Great work!"
    return handler_input.response_builder.speak(speech).response

lambda_handler = sb.lambda_handler()
```

---

## Pattern 9: Mobile App (Future)

### React Native app querying Willow
```javascript
// WillowMobileApp.js
import React, { useEffect, useState } from 'react';
import { View, Text, FlatList, Button } from 'react-native';
import axios from 'axios';

const WillowApp = () => {
  const [tasks, setTasks] = useState([]);

  useEffect(() => {
    fetchTasks();
  }, []);

  const fetchTasks = async () => {
    // Call Willow API
    const response = await axios.get('https://willow-api.company.com/tasks/my-tasks');
    setTasks(response.data.tasks);
  };

  const claimTask = async (taskId) => {
    await axios.post(`https://willow-api.company.com/tasks/${taskId}/claim`);
    fetchTasks(); // Refresh
  };

  return (
    <View>
      <Text style={{fontSize: 24, fontWeight: 'bold'}}>My Willow Tasks</Text>
      <FlatList
        data={tasks}
        renderItem={({item}) => (
          <View style={{padding: 10, borderBottom: '1px solid #ccc'}}>
            <Text style={{fontWeight: 'bold'}}>{item.id}: {item.title}</Text>
            <Text>{item.description}</Text>
            <Text>Priority: {item.priority} | Status: {item.status}</Text>
            {item.status === 'todo' && (
              <Button title="Claim Task" onPress={() => claimTask(item.id)} />
            )}
          </View>
        )}
        keyExtractor={item => item.id}
      />
    </View>
  );
};
```

---

## The Universal Pattern

**All integrations follow the same flow:**

```
1. QUERY
   ↓ (What work is available?)
   Graph (AuraDB) or API (Willow API)

2. WORK
   ↓ (Do the task)
   Code, design, test, document

3. UPDATE
   ↓ (Report completion)
   Graph (AuraDB) or API (Willow API)

4. NOTIFY (optional)
   ↓ (Tell stakeholders)
   Slack, email, GitHub comment
```

**Example implementations:**
- **GitHub**: Browse kanban → Create PR → GitHub Actions updates graph
- **Jira**: Webhook creates ticket → Work in Jira → Webhook updates graph
- **Email**: Send email → Task created → Work done → Reply sent
- **Voice**: Ask Alexa → Tasks read aloud → Voice command → Graph updated
- **Mobile**: Open app → See tasks → Tap "claim" → Graph updated

---

## Your Integration (Peter)

**What you asked**: "How can I do things as an agent? Like create a Jira ticket?"

### Option 1: Via N8N (Easiest)
```
1. Create N8N workflow:
   - Trigger: Webhook (you send POST request)
   - Action: Create Jira ticket
   - Action: Create Task node in AuraDB
   - Response: "Task created!"

2. Bookmark URL: https://agilemesh.app.n8n.cloud/webhook/create-task

3. Use it:
   curl -X POST https://agilemesh.app.n8n.cloud/webhook/create-task \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Add pricing engine",
       "description": "We need to calculate premiums",
       "priority": "high",
       "create_jira": true
     }'
```

### Option 2: Via Python Script
```python
# peter_create_task.py
from neo4j import GraphDatabase
from jira import JIRA

# Your function
def create_task(title, description, priority='medium', create_jira=False):
    # Generate task ID
    task_id = get_next_task_id()  # e.g., WILL-025

    # Create in AuraDB
    with neo4j_driver.session() as session:
        session.run("""
            CREATE (t:Task {
                id: $task_id,
                title: $title,
                description: $description,
                priority: $priority,
                status: 'todo',
                created_at: datetime()
            })
        """, task_id=task_id, title=title, description=description, priority=priority)

    # Optionally create Jira ticket
    if create_jira:
        jira = JIRA('https://your-company.atlassian.net', basic_auth=(EMAIL, API_TOKEN))
        issue = jira.create_issue(
            project='WILLOW',
            summary=title,
            description=description,
            issuetype={'name': 'Task'}
        )

        # Link back to graph
        session.run("""
            MATCH (t:Task {id: $task_id})
            SET t.jira_key = $jira_key
        """, task_id=task_id, jira_key=issue.key)

    print(f"Created {task_id}: {title}")
    if create_jira:
        print(f"Jira ticket: {issue.key}")

    return task_id

# Usage
if __name__ == "__main__":
    create_task(
        title="Add pricing engine for quotes",
        description="Calculate premiums based on age, breed, coverage type",
        priority="high",
        create_jira=True
    )
```

### Option 3: Via Willow CLI (To Be Built)
```bash
# Future tool
willow create task \
  --title "Add pricing engine" \
  --description "Calculate premiums..." \
  --priority high \
  --jira
```

---

## Summary: You ARE An Agent

**Peter, you can:**

1. ✅ **Create tasks** (via Python, N8N, email, voice, etc.)
2. ✅ **Claim tasks** (via GitHub, Jira, Slack button, mobile app)
3. ✅ **Update status** (via any integration)
4. ✅ **Query roadmap** (via AuraDB, API, CLI tool)
5. ✅ **Integrate with ANY tool** (Jira, Linear, Asana, Monday, etc.)

**The graph coordinates everyone. You're just another agent in the system - the most important one!**

---

**Next Steps:**
1. Pick integration pattern (I recommend N8N for quick start)
2. I'll build the webhook/workflow
3. You can create tasks from anywhere (email, curl, browser, etc.)
4. Jira/Linear/Slack get auto-updated

**Want me to build one of these integrations now?** 🌳

