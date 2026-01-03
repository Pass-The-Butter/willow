## Plan: Unified Command Center Protocol

We will evolve the existing "Sidebar" (currently serving documentation on `bunny`) into a master application shell. This shell will provide the requested persistent left-hand navigation, embedding or linking to the various subsystems (Metrics, Grapevine, Brain) so they are accessible from a single pane of glass.

### Steps
1. **Audit Sidebar Architecture**: Inspect the `bunny` web root (likely Astro/Starlight) to confirm it can host dynamic components or iframes.
2. **Construct the Shell**: Modify the Sidebar layout to support a persistent "Global Navigation" menu on the left.
3. **Integrate Metrics**: Embed the Python-based Metrics Dashboard (currently port 5001) into a dedicated view within the Shell.
4. **Connect the Grapevine**: Add a status view that subscribes to N8N (Grapevine) webhooks for live system health monitoring.
5. **Deploy & Verify**: Push the updated Shell to `bunny` and verify all internal links (Neo4j, Jira) function correctly.

### Further Considerations
1. **Integration Depth**: Should we simply `iframe` the existing Python dashboard, or rewrite its visualizations natively into the Sidebar for better performance?
2. **Security**: Does this unified view require a login layer, or is the local network security sufficient?
