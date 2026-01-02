# Session Handoff: 2025-12-28

## "The Bunny Migration & Population Reset"

### 1. Executive Summary

- **Runtime Migrated**: All services (Dashboard, N8N, Graphiti, Neo4j-MCP) are now running on **Bunny (Xeon Server)** and exposed via Tailscale Funnel. The Mac is now strictly a client.
- **Data Loss Incident**: The previous 100k population records were confirmed lost (0 rows in all checked DBs).
- **Directive Change**: **STOP** random generation. The next data generation run must strictly align with the **Purely Pets Insurance** quote form.
- **Current Status**: System is operational but empty. Population schema is being refactored.

### 2. Infrastructure State

- **Server**: Bunny (Xeon/Ubuntu)
- **Access**: `ssh bunny` (Configured in `~/.ssh/config` or via key)
- **Services (Docker)**:
  - `willow-dashboard`: Port 5001 (Mapped to `https://bunny.clouded-newton.ts.net`)
  - `willow-n8n`: Port 5678 (Mapped to `/n8n`)
  - `willow-api`: Port 8000 (Mapped to `/api`)
  - `willow-graphiti`: Port 8002 (Mapped to `/graphiti`)
  - `willow-population-db`: Port 5432 (Currently `postgres:15-alpine` - **NEEDS UPDATE**)

### 3. The "Purely Pets" Plan (Next Steps)

The user has mandated strict alignment with `https://quote.purelypetsinsurance.co.uk/`.

#### A. Database Upgrade

The current `postgres:15-alpine` image lacks the `pgvector` extension required by the new spec.

- [ ] **ACTION**: Update `docker-compose.yml` service `population-db` to use image `pgvector/pgvector:pg15`.
- [ ] **ACTION**: Redeploy container: `docker-compose up -d population-db`.

#### B. Schema Application

A new schema matching the Purely Pets form has been drafted but **NOT applied**.

- [ ] **Source**: `domains/population/correct_schema.sql`
- [ ] **Action**: Run this SQL against the new `pgvector` container.
- [ ] **Note**: Drops existing `people` table in favor of `customers` and `pets`.

#### C. Generator Rewrite

The current `remote_generator.py` targets the old `people` table.

- [ ] **ACTION**: Refactor `remote_generator.py` to:
  - Import `Faker` (en_GB locale).
  - Generate strictly `customers` (Name, Email, Phone, Address, DOB).
  - Generate `pets` (Name, Species, Breed, DOB, Gender, Microchipped).
  - Insert into the new tables.
  - **Audit**: Use the Neo4j audit logging block drafted in the previous attempt.

#### D. Housekeeping

- [ ] **Backup**: `bootstrap/backup_population.sh` is installed on Bunny. Configure a cron job or N8N workflow to run this nightly.

### 4. Critical Files

- `docs/POPULATION_SCHEMA_SPEC.md`: **The Source of Truth**.
- `domains/population/correct_schema.sql`: The database definition.
- `BIOS.md`: Updated with new Tailscale URLs.

### 5. Known Issues

- `people.html` template currently tries to view the old `people` table. Needs update to view `customers`/`pets` JOIN after schema change.
- `remote_generator.py`: Currently broken/in-between states. Needs full rewrite.

_Signed, Antigravity (Session 2025-12-28)_
