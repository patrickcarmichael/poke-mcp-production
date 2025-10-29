# Poke MCP Production Server

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/patrickcarmichael/poke-mcp-production)

A production-ready Pokémon MCP (Model Context Protocol) server with enterprise features:

- ✅ **FastMCP with HTTP Transport** - RESTful API access to MCP tools
- 🔒 **Authentication** - API key-based security
- 📈 **Monitoring** - Prometheus metrics and health checks
- 📝 **Structured Logging** - JSON-formatted logs with structlog
- ⚡ **Rate Limiting** - Protect against abuse
- 🚀 **Vercel Deployment** - Serverless deployment with continuous integration
- 🔐 **SSH Tunneling** - Secure remote access configuration

## Features

### MCP Tools

1. **get_pokemon_info** - Comprehensive Pokémon information
   - Base stats, types, abilities (with descriptions)
   - Moves with effects (first 10)
   - Full evolution chain

2. **simulate_battle** - Realistic Pokémon battle simulation
   - Core battle mechanics (type effectiveness, status effects)
   - Turn-based combat with detailed battle log
   - Winner determination

### Production Features

- **Authentication**: Bearer token API key authentication
- **Rate Limiting**: Configurable request limits per time window
- **Monitoring**: Prometheus metrics for requests, latency, and tool calls
- **Logging**: Structured JSON logs with request tracing
- **CORS**: Configurable cross-origin resource sharing
- **Health Checks**: `/health` endpoint for monitoring
- **Environment Configuration**: Flexible environment-based settings

## Quick Start

### Prerequisites

- Python 3.11+
- [uv](https://github.com/astral-sh/uv) (recommended) or pip
- Vercel account (for deployment)

### Local Development

1. **Clone the repository**

```bash
git clone https://github.com/patrickcarmichael/poke-mcp-production.git
cd poke-mcp-production
```

2. **Install dependencies**

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -r requirements.txt
```

3. **Configure environment**

```bash
cp .env.example .env
# Edit .env with your settings
```

4. **Run the server**

```bash
# For MCP stdio mode (local testing)
python server.py

# For HTTP mode (production)
uvicorn api.index:app --reload --host 0.0.0.0 --port 8000
```

5. **Test the server**

```bash
# Health check
curl http://localhost:8000/health

# Protected endpoint (requires API key)
curl -H "Authorization: Bearer your-api-key" http://localhost:8000/status
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive deployment instructions including:

- Vercel deployment
- Environment variable configuration
- SSH tunnel setup for remote access
- Continuous deployment setup
- Production monitoring

## Configuration

All configuration is managed through environment variables. See `.env.example` for all available options.

### Key Configuration Options

| Variable | Description | Default |
|----------|-------------|----------|
| `API_KEY` | Authentication key | (required) |
| `ALLOWED_ORIGINS` | CORS allowed origins | `http://localhost:*` |
| `LOG_LEVEL` | Logging level | `INFO` |
| `RATE_LIMIT_REQUESTS` | Max requests per window | `100` |
| `RATE_LIMIT_WINDOW` | Time window in seconds | `60` |
| `ENABLE_METRICS` | Enable Prometheus metrics | `true` |

## API Endpoints

### Public Endpoints

- `GET /` - Server information
- `GET /health` - Health check
- `GET /metrics` - Prometheus metrics (if enabled)

### Protected Endpoints (Require API Key)

- `POST /mcp` - MCP tool execution endpoint
- `GET /status` - Detailed server status

### Authentication

All protected endpoints require a Bearer token:

```bash
curl -H "Authorization: Bearer YOUR_API_KEY" https://your-server.vercel.app/status
```

## Monitoring

### Prometheus Metrics

The server exposes Prometheus-compatible metrics at `/metrics`:

- `http_requests_total` - Total HTTP requests by method, endpoint, and status
- `http_request_duration_seconds` - Request latency histogram
- `mcp_tool_calls_total` - MCP tool invocations by tool name and status
- `mcp_tool_duration_seconds` - Tool execution duration
- `pokeapi_requests_total` - PokeAPI requests by endpoint and status
- `active_connections` - Current active connections

### Logging

Structured JSON logs include:

- Request/response details
- Tool execution tracking
- Error tracking with stack traces
- Performance metrics

## SSH Tunneling for Remote Access

See [SSH_TUNNELING.md](SSH_TUNNELING.md) for detailed instructions on:

- Setting up SSH tunnels to access your deployed server
- Configuring Claude Desktop and other MCP clients
- Security best practices
- Troubleshooting

## Architecture

```
poke-mcp-production/
├── api/
│   └── index.py          # Vercel serverless handler
├── src/
│   ├── __init__.py
│   ├── auth.py           # Authentication logic
│   ├── battle_utils.py   # Battle simulation utilities
│   ├── config.py         # Configuration management
│   ├── constants.py      # Type effectiveness, constants
│   ├── logger.py         # Structured logging setup
│   ├── middleware.py     # CORS, rate limiting, logging
│   ├── monitoring.py     # Prometheus metrics
│   └── pokeapi_client.py # PokeAPI integration
├── server.py            # Main MCP server (stdio mode)
├── vercel.json          # Vercel configuration
├── pyproject.toml       # Project metadata
├── requirements.txt     # Python dependencies
└── .env.example         # Environment template
```

## Development

### Testing

```bash
# Install dev dependencies
uv sync --extra dev

# Run tests (when implemented)
pytest

# Code formatting
black .

# Linting
ruff check .

# Type checking
mypy src/
```

### Adding New Tools

1. Add tool function to `server.py`:

```python
@mcp.tool()
async def my_new_tool(param: str) -> Dict[str, Any]:
    """Tool description."""
    # Implementation
    return {"result": "data"}
```

2. Add monitoring and logging as needed
3. Update documentation

## Security Considerations

1. **API Keys**: Always use strong, randomly generated API keys
2. **CORS**: Configure `ALLOWED_ORIGINS` for production
3. **Rate Limiting**: Adjust limits based on expected usage
4. **HTTPS**: Always use HTTPS in production (Vercel provides this)
5. **SSH Tunnels**: Use key-based authentication, not passwords
6. **Secrets**: Never commit `.env` files or secrets to git

## Troubleshooting

### Server Won't Start

- Check Python version: `python --version` (must be 3.11+)
- Verify all dependencies are installed
- Check `.env` file configuration

### Authentication Failures

- Verify API key is set in environment
- Check Authorization header format: `Bearer YOUR_KEY`
- Ensure CORS settings allow your origin

### Rate Limiting Issues

- Adjust `RATE_LIMIT_REQUESTS` and `RATE_LIMIT_WINDOW`
- Check client IP address handling
- Review logs for rate limit events

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

MIT License - see LICENSE file for details

## Acknowledgments

- [PokeAPI](https://pokeapi.co/) - Pokémon data source
- [FastMCP](https://github.com/jlowin/fastmcp) - MCP server framework
- [Model Context Protocol](https://modelcontextprotocol.io/) - MCP specification
- Original poke-mcp implementations by [NaveenBandarage](https://github.com/NaveenBandarage) and [ChiragAgg5k](https://github.com/ChiragAgg5k)

## Support

For issues, questions, or contributions:

- Open an issue on GitHub
- Check [DEPLOYMENT.md](DEPLOYMENT.md) for deployment help
- Review [SSH_TUNNELING.md](SSH_TUNNELING.md) for remote access setup

## Roadmap

- [ ] Full MCP protocol integration in Vercel endpoint
- [ ] WebSocket support for real-time updates
- [ ] Caching layer for PokeAPI responses
- [ ] Additional battle mechanics
- [ ] Team management tools
- [ ] Database integration for persistent data
- [ ] GraphQL API option
- [ ] Docker deployment option
