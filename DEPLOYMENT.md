# Deployment Guide - Poke MCP Production

This guide covers deploying your Poke MCP server to Vercel with continuous deployment.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Vercel Deployment](#vercel-deployment)
3. [Environment Variables](#environment-variables)
4. [Continuous Deployment](#continuous-deployment)
5. [Custom Domain Setup](#custom-domain-setup)
6. [Monitoring Setup](#monitoring-setup)
7. [Troubleshooting](#troubleshooting)

## Prerequisites

- GitHub account with this repository
- [Vercel account](https://vercel.com/signup) (free tier works)
- Generated API key (strong random string)

## Vercel Deployment

### Option 1: Deploy Button (Quickest)

1. Click the "Deploy with Vercel" button in the README
2. Connect your GitHub account if not already connected
3. Configure environment variables (see below)
4. Click "Deploy"

### Option 2: Vercel CLI

1. **Install Vercel CLI**

```bash
npm install -g vercel
```

2. **Login to Vercel**

```bash
vercel login
```

3. **Deploy from project directory**

```bash
cd poke-mcp-production
vercel
```

4. **Follow the prompts**:
   - Link to existing project or create new
   - Set up environment variables
   - Deploy

### Option 3: Vercel Dashboard

1. **Go to [Vercel Dashboard](https://vercel.com/dashboard)**

2. **Click "New Project"**

3. **Import from Git**:
   - Select your GitHub repository
   - Click "Import"

4. **Configure Project**:
   - Framework Preset: Other
   - Root Directory: `./`
   - Build Command: (leave empty, uses vercel.json)
   - Output Directory: (leave empty)

5. **Add Environment Variables** (see next section)

6. **Click "Deploy"**

## Environment Variables

### Required Variables

Add these in Vercel Dashboard → Settings → Environment Variables:

```bash
# Authentication - CRITICAL
API_KEY=your-super-secure-random-api-key-here

# Server Configuration
SERVER_NAME=poke-mcp-production
SERVER_VERSION=1.0.0

# CORS - Update with your domains
ALLOWED_ORIGINS=http://localhost:*,https://yourdomain.com,https://your-vercel-app.vercel.app

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=json

# Monitoring
ENABLE_METRICS=true

# Rate Limiting
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_WINDOW=60

# PokeAPI
POKEAPI_BASE_URL=https://pokeapi.co/api/v2
POKEAPI_TIMEOUT=30

# Production
ENVIRONMENT=production
DEBUG=false
```

### Generating a Secure API Key

```bash
# Using Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Using OpenSSL
openssl rand -base64 32

# Using Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('base64'))"
```

### Environment Variable Scopes

In Vercel, you can set variables for:

- **Production**: Used for production deployments
- **Preview**: Used for preview deployments (PRs)
- **Development**: Used for local development

Recommend setting all variables for **Production** and **Preview**.

## Continuous Deployment

### Automatic Deployment

Vercel automatically deploys:

1. **Production Deployments**: Every push to `main` branch
2. **Preview Deployments**: Every pull request

### Deployment Workflow

```bash
# Make changes
git add .
git commit -m "Update feature"
git push origin main

# Vercel automatically:
# 1. Detects the push
# 2. Builds the project
# 3. Deploys to production
# 4. Sends notification
```

### Manual Deployment

```bash
# Deploy to preview
vercel

# Deploy to production
vercel --prod
```

### Deployment Hooks

For advanced workflows, use Vercel Deploy Hooks:

1. Go to Project Settings → Git → Deploy Hooks
2. Create a new hook
3. Use the webhook URL in your CI/CD pipeline

```bash
# Trigger deployment via webhook
curl -X POST https://api.vercel.com/v1/integrations/deploy/...
```

## Custom Domain Setup

### Add Custom Domain

1. **Go to Project Settings → Domains**

2. **Add your domain**: `api.yourdomain.com`

3. **Configure DNS**:

   For apex domain (`yourdomain.com`):
   ```
   Type: A
   Name: @
   Value: 76.76.21.21
   ```

   For subdomain (`api.yourdomain.com`):
   ```
   Type: CNAME
   Name: api
   Value: cname.vercel-dns.com
   ```

4. **Wait for verification** (can take a few minutes to hours)

5. **Update `ALLOWED_ORIGINS`** in environment variables

### SSL/TLS

Vercel automatically provisions SSL certificates. No additional configuration needed.

## Monitoring Setup

### Vercel Analytics

1. Enable in Project Settings → Analytics
2. View traffic, performance metrics in dashboard

### Prometheus Monitoring

Your server exposes metrics at `/metrics`:

```bash
curl https://your-app.vercel.app/metrics
```

**Setup Prometheus Scraper**:

```yaml
# prometheus.yml
scrape_configs:
  - job_name: 'poke-mcp'
    metrics_path: '/metrics'
    static_configs:
      - targets: ['your-app.vercel.app']
```

### Health Check Monitoring

Use a service like:

- **UptimeRobot**: Free health check monitoring
- **Pingdom**: Advanced monitoring
- **Datadog**: Full observability

Monitor endpoint: `https://your-app.vercel.app/health`

### Log Aggregation

**Vercel Logs**:
- View in Vercel Dashboard → Deployments → Functions Logs
- Real-time streaming available

**External Log Services**:
- **Logtail**: Structured log aggregation
- **Datadog**: Full logging and APM
- **Elasticsearch**: Self-hosted solution

## Post-Deployment Checklist

- [ ] Verify deployment URL works
- [ ] Test health endpoint: `GET /health`
- [ ] Test authenticated endpoint: `GET /status` (with API key)
- [ ] Verify CORS settings
- [ ] Check metrics endpoint: `GET /metrics`
- [ ] Test MCP tools work correctly
- [ ] Set up health check monitoring
- [ ] Configure custom domain (if applicable)
- [ ] Update client configurations with new URL
- [ ] Test SSH tunnel connection (see SSH_TUNNELING.md)
- [ ] Document API key securely
- [ ] Set up alerting for errors

## Troubleshooting

### Deployment Fails

**Check build logs**:
1. Go to Vercel Dashboard → Deployments
2. Click on failed deployment
3. View build logs

**Common issues**:

- **Missing dependencies**: Check `requirements.txt`
- **Python version**: Ensure 3.11+ in `vercel.json`
- **Import errors**: Verify all imports are correct
- **Environment variables**: Ensure all required vars are set

### 500 Internal Server Error

1. **Check Function Logs**:
   - Vercel Dashboard → Deployments → Function Logs

2. **Common causes**:
   - Missing environment variables
   - Runtime errors in code
   - Dependency issues

3. **Debug locally**:
   ```bash
   vercel env pull .env.local
   uvicorn api.index:app --reload
   ```

### Authentication Not Working

1. **Verify API key is set**: Check environment variables
2. **Check Authorization header format**: `Bearer YOUR_KEY`
3. **Verify CORS settings**: Check `ALLOWED_ORIGINS`
4. **Check logs**: Look for authentication errors

### Rate Limiting Too Aggressive

1. Update environment variables:
   ```bash
   RATE_LIMIT_REQUESTS=500
   RATE_LIMIT_WINDOW=60
   ```

2. Or disable temporarily:
   ```bash
   RATE_LIMIT_ENABLED=false
   ```

3. Redeploy for changes to take effect

### Timeout Issues

**Vercel Function Timeouts**:

- Free tier: 10 seconds
- Pro tier: 60 seconds

**Solutions**:

1. Optimize PokeAPI calls (reduce requests)
2. Implement caching
3. Upgrade to Pro plan if needed
4. Adjust `POKEAPI_TIMEOUT` setting

### CORS Errors

1. **Check `ALLOWED_ORIGINS`**: Must include requesting origin
2. **Format**: Comma-separated, no spaces
   ```
   https://example.com,https://api.example.com
   ```
3. **Wildcards**: Use `*` for port: `http://localhost:*`
4. **Redeploy** after changes

## Performance Optimization

### Caching

Implement caching for PokeAPI responses:

```python
# Add to src/pokeapi_client.py
from functools import lru_cache

@lru_cache(maxsize=1000)
def cache_pokemon_data(name: str):
    # Cached lookup
    pass
```

### Database Integration

For persistent caching, consider:

- **Vercel KV** (Redis)
- **Supabase** (PostgreSQL)
- **PlanetScale** (MySQL)

### Edge Functions

For lower latency, consider Vercel Edge Functions:

```json
// vercel.json
{
  "functions": {
    "api/index.py": {
      "runtime": "edge"
    }
  }
}
```

## Security Best Practices

1. **Rotate API keys regularly**
2. **Use different keys for production/preview**
3. **Enable rate limiting**
4. **Monitor for unusual activity**
5. **Keep dependencies updated**
6. **Use HTTPS only**
7. **Implement request signing for critical operations**
8. **Regular security audits**

## Scaling Considerations

### Vercel Limits (Free Tier)

- 100 GB bandwidth/month
- 100 hours serverless function execution
- 12 deployments/day

### When to Upgrade

- High traffic volume
- Need longer function timeouts
- Require more bandwidth
- Need team collaboration features

### Alternative Hosting

If you outgrow Vercel:

- **AWS Lambda** + API Gateway
- **Google Cloud Functions**
- **Azure Functions**
- **Railway** (simpler alternative)
- **Fly.io** (persistent instances)
- **Self-hosted** with Docker

## Getting Help

- **Vercel Documentation**: https://vercel.com/docs
- **Vercel Support**: support@vercel.com
- **Community Discord**: Join Vercel Discord
- **GitHub Issues**: Open issue in repository

## Next Steps

After successful deployment:

1. Read [SSH_TUNNELING.md](SSH_TUNNELING.md) for remote access setup
2. Configure MCP clients to use your server
3. Set up monitoring and alerting
4. Plan for scaling and optimization
