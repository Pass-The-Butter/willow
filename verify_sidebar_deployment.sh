#!/bin/bash

# Willow Sidebar Deployment Verification Script
# Usage: ./verify_sidebar_deployment.sh

set -e

echo "🧠 Willow Sidebar Mission Control - Deployment Verification"
echo "============================================================"
echo ""

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if docker is running
echo "1. Checking Docker..."
if ! docker info > /dev/null 2>&1; then
    echo -e "${RED}✗ Docker is not running${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Docker is running${NC}"
echo ""

# Check if sidebar container exists
echo "2. Checking sidebar container..."
if docker ps -a | grep -q willow-sidebar; then
    echo -e "${GREEN}✓ Sidebar container exists${NC}"

    # Check if it's running
    if docker ps | grep -q willow-sidebar; then
        echo -e "${GREEN}✓ Sidebar container is running${NC}"
    else
        echo -e "${YELLOW}⚠ Sidebar container exists but is not running${NC}"
        echo "  Run: docker-compose up -d sidebar"
    fi
else
    echo -e "${RED}✗ Sidebar container not found${NC}"
    echo "  Run: docker-compose build sidebar && docker-compose up -d sidebar"
    exit 1
fi
echo ""

# Check if proxy container exists and is running
echo "3. Checking proxy container..."
if docker ps | grep -q willow-proxy; then
    echo -e "${GREEN}✓ Proxy container is running${NC}"
else
    echo -e "${YELLOW}⚠ Proxy container not running${NC}"
    echo "  Run: docker-compose up -d proxy"
fi
echo ""

# Test direct sidebar access (port 3000)
echo "4. Testing direct sidebar access (port 3000)..."
if curl -s -o /dev/null -w "%{http_code}" http://localhost:3000 | grep -q "200"; then
    echo -e "${GREEN}✓ Sidebar accessible on port 3000${NC}"
else
    echo -e "${RED}✗ Sidebar not accessible on port 3000${NC}"
    echo "  Check logs: docker logs willow-sidebar"
fi
echo ""

# Test proxy routing (port 80)
echo "5. Testing proxy routing (port 80)..."
HTTP_CODE=$(curl -s -o /dev/null -w "%{http_code}" http://localhost/ 2>/dev/null || echo "000")
if [ "$HTTP_CODE" = "200" ]; then
    echo -e "${GREEN}✓ Proxy routing works (HTTP 200)${NC}"

    # Check if it's actually the sidebar
    if curl -s http://localhost/ | grep -q "Willow Mission Control"; then
        echo -e "${GREEN}✓ Serving Willow Sidebar content${NC}"
    else
        echo -e "${YELLOW}⚠ Port 80 accessible but not serving sidebar${NC}"
    fi
else
    echo -e "${RED}✗ Proxy not accessible (HTTP $HTTP_CODE)${NC}"
    echo "  Check: docker logs willow-proxy"
fi
echo ""

# Check sidebar logs for errors
echo "6. Checking sidebar logs for errors..."
ERROR_COUNT=$(docker logs willow-sidebar 2>&1 | grep -i error | wc -l | tr -d ' ')
if [ "$ERROR_COUNT" -eq "0" ]; then
    echo -e "${GREEN}✓ No errors in sidebar logs${NC}"
else
    echo -e "${YELLOW}⚠ Found $ERROR_COUNT error(s) in logs${NC}"
    echo "  View logs: docker logs willow-sidebar"
fi
echo ""

# Check content structure
echo "7. Checking content structure..."
if [ -d "domains/sidebar/src/content/docs/knowledge" ]; then
    echo -e "${GREEN}✓ Knowledge section exists${NC}"
else
    echo -e "${RED}✗ Knowledge section missing${NC}"
fi

if [ -d "domains/sidebar/src/content/docs/operations" ]; then
    echo -e "${GREEN}✓ Operations section exists${NC}"
else
    echo -e "${RED}✗ Operations section missing${NC}"
fi

if [ -d "domains/sidebar/src/content/docs/reports" ]; then
    REPORT_COUNT=$(find domains/sidebar/src/content/docs/reports -name "*.mdx" | wc -l | tr -d ' ')
    echo -e "${GREEN}✓ Reports section exists ($REPORT_COUNT reports)${NC}"
else
    echo -e "${RED}✗ Reports section missing${NC}"
fi
echo ""

# Check if post_status.py skill exists
echo "8. Checking reporting skill..."
if [ -f "core/skills/post_status.py" ]; then
    echo -e "${GREEN}✓ post_status.py skill exists${NC}"
else
    echo -e "${RED}✗ post_status.py skill not found${NC}"
fi
echo ""

# Summary
echo "============================================================"
echo "Deployment Verification Summary"
echo "============================================================"
echo ""
echo "Container Status:"
docker ps --filter "name=willow-sidebar" --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" || true
echo ""
echo "Network Connectivity:"
echo "  Direct: http://localhost:3000"
echo "  Proxy:  http://localhost/ (or http://bunny/)"
echo ""
echo "Next Steps:"
echo "  1. Open http://bunny/ in a browser"
echo "  2. Navigate through Knowledge, Operations, and Reports sections"
echo "  3. Generate a flight report:"
echo "     python -c \"from core.skills import post_status; print(post_status.execute('Test Report'))\""
echo ""
echo "For detailed deployment guide, see: domains/sidebar/DEPLOYMENT.md"
echo ""
