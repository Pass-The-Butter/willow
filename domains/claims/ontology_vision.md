# Willow Business Ontology Vision: The Claims Assessment Cycle

## Origin Story

_Based on the "Jane Winterbottom & Bobby" narrative._

This ontology is designed to capture the lifecycle of an insurance policy and a subsequent claim, specifically focusing on the data capture points from the "Purely Pets" quote page through to claims settlement.

### The Narrative

1.  **Customer Acquisition**: Jane Winterbottom (Person) lives at 76 Acaicia Drive (Address) and buys Bobby (Pet, Cocker Spaniel) on 14/02/2024.
2.  **Policy Inception**: Jane accepts a quote from Affinity (Insurer) with a specific Underwriter. Policy Policy starts for £24.37/month.
3.  **The Event**: Bobby develops a sniffle and a lump (Health Event).
4.  **Care**: Jane visits Francis Bacon Pet Health (Vet Practice) in Wossit (Location). Diagnosis is made using standard codes.
5.  **Claim Initiation**: Jane sends an incomplete Claim Form.
6.  **Data Enrichment**: Insurance Factory (Broker) contacts Vet via email. Vet calls back; Call Agent records info.
7.  **Assessment**: Anne Farraday (Assessor) reviews the claim.
8.  **Decision**: "Willow" (AI) researches the diagnosis. Claim is passed.
9.  **Settlement**: Letter sent to Jane.

## Conceptual Model

### Key Entities (Nodes)

- **Person**: (e.g., Jane Winterbottom, Anne Farraday, Call Agent)
- **Address**: (e.g., 76 Acaicia Drive)
- **Pet**: (e.g., Bobby)
- **Breed**: (e.g., Cocker Spaniel)
- **Policy**: (e.g., The contract)
- **Insurer**: (e.g., Affinity)
- **Underwriter**: (e.g., The Underwriter entity)
- **Claim**: (e.g., The request for indemnity)
- **VetPractice**: (e.g., Francis Bacon Pet Health)
- **Diagnosis**: (e.g., Sniffle, Lump - Standard Code)
- **Document**: (e.g., Claim Form, Letter, Email)
- **Interaction**: (e.g., Call, Email sent, Research task)
- **Agent**: (e.g., Willow Research Agent)

### Relationships (Edges)

- `(:Person)-[:LIVES_AT]->(:Address)`
- `(:Person)-[:OWNS]->(:Pet)`
- `(:Pet)-[:IS_BREED]->(:Breed)`
- `(:Policy)-[:COVERS]->(:Pet)`
- `(:Policy)-[:OWNED_BY]->(:Person)`
- `(:Policy)-[:UNDERWRITTEN_BY]->(:Underwriter)`
- `(:Claim)-[:FILED_AGAINST]->(:Policy)`
- `(:Claim)-[:INVOLVES]->(:Pet)`
- `(:Pet)-[:VISITED]->(:VetPractice)`
- `(:VetPractice)-[:DIAGNOSED]->(:Diagnosis)-[:FOR]->(:Pet)`
- `(:Person)-[:SUBMITTED]->(:Document)`
- `(:Broker)-[:CONTACTED]->(:VetPractice)`
- `(:Assessor)-[:ASSESSED]->(:Claim)`
- `(:Agent)-[:RESEARCHED]->(:Diagnosis)`

## Data Capture Points

The ontology must support partial data capture at various stages:

1.  **Quote**: Customer, Pet, Address.
2.  **Inception**: Policy details, Premium.
3.  **Claim**: Vet details, Event details.
4.  **Enrichment**: Missing info gathered via interactions.

## Technical Implementation Strategy

We will implement this using Neo4j (Cypher) as the primary store for the "Business Graph".
The schema will be defined in `schemas/business_ontology.cypher`.
