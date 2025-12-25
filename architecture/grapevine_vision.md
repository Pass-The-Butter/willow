# 🍇 The Grapevine: Resilient Intelligent System Architecture

> "Think Blockchain. Think Resilient Intelligent System design."

## Concept

A central, asynchronous Event Bus ("The Grapevine") where all agents publish their actions, thoughts, and discoveries. Specialized "Observer Agents" subscribe to this stream to maintain system state, update documentation, and trigger JIT context.

## Architectural Diagram

```mermaid
graph TD
    subgraph "Sources (The Swarm)"
        A1[User Interaction] -->|Action/Query| GV
        A2[Research Agent] -->|Insight| GV
        A3[Secretary Agent] -->|Minutes| GV
        A4[Dev Agent] -->|Code Change| GV
    end

    subgraph "The Grapevine (N8N Event Bus)"
        GV((Grapevine Core))
        Store[Event Ledger / Log]
    end

    subgraph "JIT Memory Swarm"
        GV -->|Trigger| Dispatcher
        Dispatcher --> SQL[SQL Scout]
        Dispatcher --> Graph[Cypher Scout]
        Dispatcher --> Vector[Vector Scout]
        Dispatcher --> Web[News Scout]

        SQL --> Curator
        Graph --> Curator
        Vector --> Curator
        Web --> Curator

        Curator{Curator Agent} -->|Fact Checked Context| GV
    end

    subgraph "Observers (Subscribers)"
        GV -->|Fast Update| Dash[Dashboard Agent]
        GV -->|Slow Sync| KM[Knowledge Manager]
        GV -->|Archive| Zep[Zep/Graphiti Memory]
    end

    Dash -->|Live Metrics| UI[AgileMesh Dashboard]
    KM -->|Commit| Repo[Willow Repo]
    KM -->|Update| Wiki[Confluence]
```

## Implementation Strategy (N8N)

1.  **The Bus**: A master N8N workflow listening on a generic webhook (`/grapevine`).
2.  **The Ledger**: Log every event to Postgres instantly (Audit Trail).
3.  **The Routing**: Use N8N "Switch" nodes to route events based on `type` (e.g., `MEMORY_UPDATE`, `TASK_COMPLETE`, `NEW_IDEA`).
4.  **The Observers**:
    - **DashboardUpdater**: Filters for metric events -> Pushes to Board.
    - **Librarian**: Filters for "Knowledge" -> Batches updates for Repo/Wiki.

## Next Steps

1.  Prototype the `Grapevine` webhook in N8N.
2.  Connect the existing `Dashboard` to listen to this bus.
3.  Build the `Curator` logic (Idea-027).
