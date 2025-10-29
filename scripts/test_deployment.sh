#!/bin/bash
# Test deployment script
# Usage: ./scripts/test_deployment.sh https://your-app.vercel.app YOUR_API_KEY

set -e

BASE_URL="${1:-http://localhost:8000}"
API_KEY="${2:-}"

echo "Testing deployment at: $BASE_URL"
echo ""

# Test health endpoint
echo "1. Testing health endpoint..."
curl -s "$BASE_URL/health" | jq .
echo ""

# Test root endpoint
echo "2. Testing root endpoint..."
curl -s "$BASE_URL/" | jq .
echo ""

# Test metrics endpoint (if enabled)
echo "3. Testing metrics endpoint..."
curl -s "$BASE_URL/metrics" | head -n 20
echo ""

if [ -n "$API_KEY" ]; then
    # Test authenticated endpoint
    echo "4. Testing authenticated status endpoint..."
    curl -s -H "Authorization: Bearer $API_KEY" "$BASE_URL/status" | jq .
    echo ""
    
    # Test MCP endpoint
    echo "5. Testing MCP endpoint..."
    curl -s -X POST -H "Authorization: Bearer $API_KEY" \
        -H "Content-Type: application/json" \
        -d '{"tool": "get_pokemon_info", "params": {"pokemon_name": "pikachu"}}' \
        "$BASE_URL/mcp" | jq .
    echo ""
else
    echo "⚠️  No API key provided, skipping authenticated tests"
    echo "Usage: $0 <base_url> <api_key>"
fi

echo "✅ Deployment test completed!"
