# 🎫 Meeseeks Ticket: ARCHITECT-q2ff47hf

**GUID**: `q2ff47hf`
**TITLE**: Initialize & Port Knowledge to Sidebar
**ROLE**: Mr. Meeseeks (Architect)
**CONTEXT**: Sidebar service is running but empty. `RESOURCES.md` and `BIOS.md` need to be ingested.

## 📋 Directives

1. **Source Ingestion**: Port `/Volumes/Delila/dev/Willow/RESOURCES.md` and `/BIOS.md` into `domains/sidebar/src/content/docs/`.
2. **Taxonomy Update**: Edit `astro.config.mjs` to reflect the sidebar heirarchy (Knowledge, Operations, Reports).
3. **Organogram Node**: Add this ticket GUID to the Neo4j graph as a Task node under the "Interface" domain.
4. **Deploy**: Rebuild the `sidebar` container on `bunny` to show the new content.

## 🏁 Exit Criteria

- `http://bunny` contains the system resources and BIOS text.
- Task `q2ff47hf` is visible in the D3 Organogram.

---

# 🎫 Meeseeks Ticket: GOPHER-rtb1tkjq

**GUID**: `rtb1tkjq`
**TITLE**: Connect Mission Log to MongoDB
**ROLE**: Mr. Meeseeks (Gopher)
**CONTEXT**: Verification results are currently transient. Long-term storage is required.

## 📋 Directives

1. **Skill Upgrade**: Edit `core/skills/land_the_plane.py` to push results to MongoDB Atlas (URI in `.env`).
2. **Collection**: Use database `willow-mission-control`, collection `flight_logs`.
3. **Organogram Node**: Add this ticket GUID to the Neo4j graph as a Task node under the "Core" domain.
4. **Evidence**: Store the JSON of the first successful Mongo push in the repository at `artifacts/evidence/mongo_push_rtb1tkjq.json`.

## 🏁 Exit Criteria

- One entry from `land_the_plane` exists in MongoDB Atlas.
- Task `rtb1tkjq` is visible in the D3 Organogram.
