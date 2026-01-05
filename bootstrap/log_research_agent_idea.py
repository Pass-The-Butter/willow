import os
import certifi
from neo4j import GraphDatabase
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# AuraDB connection details
URI = os.getenv("NEO4J_URI")
USER = os.getenv("NEO4J_USER")
PASSWORD = os.getenv("NEO4J_PASSWORD")

if not all([URI, USER, PASSWORD]):
    raise ValueError("Neo4j credentials not found in .env")

def log_research_agent_idea():
    """
    Log the Deep Research Agent idea to AuraDB.
    Based on n8n template: https://n8n.io/workflows/2878-host-your-own-ai-deep-research-agent-with-n8n-apify-and-openai-o3/
    """
    print("Connecting to AuraDB to log Deep Research Agent idea...")
    os.environ['SSL_CERT_FILE'] = certifi.where()
    os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
    
    driver = GraphDatabase.driver(URI, auth=(USER, PASSWORD))
    
    try:
        with driver.session() as session:
            print("Logging idea: Deep Research Agent for N8N...")
            
            session.run("""
                MERGE (i:Idea {title: 'Deep Research Agent for N8N'})
                SET i.id = 'idea-research-agent-001',
                    i.description = 'Deploy AI Deep Research Agent on local N8N server (Bunny). Replicates OpenAI DeepResearch feature - uses reasoning to synthesize web information and complete multi-step research tasks. Based on n8n template by Jimleuk.',
                    i.source = 'Captain request 2026-01-05',
                    i.source_url = 'https://n8n.io/workflows/2878-host-your-own-ai-deep-research-agent-with-n8n-apify-and-openai-o3/',
                    i.status = 'To Do',
                    i.priority = 'High',
                    i.domain = 'Research',
                    i.category = 'N8N Workflow',
                    i.complexity = 'Medium',
                    i.created = datetime(),
                    i.implementation = 'Form captures research query + depth/breadth → Creates Notion placeholder → Recursive web search + scrape via Apify → Generate partial learnings → Reasoning LLM synthesizes report → Write to Notion',
                    i.value = 'Self-hosted deep research capability at fraction of OpenAI Pro cost. Learn and customize for business needs.',
                    i.dependencies = ['Apify API Key', 'OpenAI o3-mini or o1 access', 'Notion database template', 'N8N workflow import', 'Public webhook URL'],
                    i.requirements = [
                        'APIFY.com API Key for web search and scraping',
                        'OpenAI o3-mini access (or o1 series alternative)',
                        'Notion database from template: https://jimleuk.notion.site/19486dd60c0c80da9cb7eb1468ea9afd',
                        'N8N workflow must be published with public form URL',
                        'Local N8N on Bunny already running'
                    ],
                    i.workflow_nodes = ['HTTP Request', 'If', 'Merge', 'Form', 'Notion', 'OpenAI', '+21 more'],
                    i.config_notes = 'Depth=1 & Breadth=2 takes 5-10min. Depth=3 & Breadth=5 takes 2+ hours. Can swap Apify for other scrapers. Can use Deepseek or Gemini 2.0 instead.',
                    i.credits = 'Template by David Zhang (dzhng) - https://github.com/dzhng/deep-research'

                WITH i
                MATCH (p:Project {name: 'Willow'})
                MERGE (p)-[:HAS_IDEA]->(i)
                
                WITH i
                MERGE (n8n:Technology {name: 'N8N'})
                MERGE (i)-[:USES]->(n8n)
                
                WITH i
                MERGE (infra:Infrastructure {name: 'Bunny'})
                MERGE (i)-[:DEPLOYS_TO]->(infra)
            """)
            
            print("✓ Logged: Deep Research Agent for N8N")
            print("")
            print("=" * 60)
            print("📋 REQUIREMENTS BEFORE IMPLEMENTING:")
            print("=" * 60)
            print("")
            print("1. ✅ N8N Server - Already running on Bunny (port 5678)")
            print("")
            print("2. ❓ APIFY API Key")
            print("   → Sign up at https://www.apify.com/")
            print("   → Get API key for web search and scraping services")
            print("   → Add to N8N credentials")
            print("")
            print("3. ❓ OpenAI API Access")
            print("   → Need access to o3-mini model (or o1 series)")
            print("   → Current OPENAI_API_KEY in compose - verify o3/o1 access")
            print("   → Alternative: Use Deepseek or Gemini 2.0")
            print("")
            print("4. ❓ Notion Setup")
            print("   → Duplicate template: https://jimleuk.notion.site/19486dd60c0c80da9cb7eb1468ea9afd")
            print("   → Create Notion integration/API key")
            print("   → Configure Notion nodes in workflow")
            print("")
            print("5. ❓ Public Webhook URL")
            print("   → Current: https://bunny.clouded-newton.ts.net/")
            print("   → Form must be publicly accessible")
            print("   → May need Tailscale Funnel or Cloudflare Tunnel")
            print("")
            print("6. 📥 Import Workflow")
            print("   → Download workflow JSON from n8n template page")
            print("   → Import into local N8N instance")
            print("   → Configure credentials (Apify, OpenAI, Notion)")
            print("")
            print("=" * 60)
            print("💡 ALTERNATIVE OPTIONS:")
            print("=" * 60)
            print("• Replace Apify with: Firecrawl (costly), SerpAPI, or custom scraper")
            print("• Replace OpenAI o3 with: Deepseek, Gemini 2.0 Thinking")
            print("• Replace Notion with: AuraDB direct storage, Markdown files")
            print("• Replace web data with: Internal document search")
            print("")
            
    except Exception as e:
        print(f"Error logging idea: {e}")
    finally:
        driver.close()

if __name__ == "__main__":
    log_research_agent_idea()
