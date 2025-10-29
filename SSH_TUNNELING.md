# SSH Tunneling Setup for Remote Access

This guide explains how to set up SSH tunnels to securely access your deployed Poke MCP server from remote clients like Claude Desktop.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [SSH Server Setup](#ssh-server-setup)
4. [Local SSH Tunnel](#local-ssh-tunnel)
5. [Reverse SSH Tunnel](#reverse-ssh-tunnel)
6. [MCP Client Configuration](#mcp-client-configuration)
7. [Persistent Tunnels](#persistent-tunnels)
8. [Security Best Practices](#security-best-practices)
9. [Troubleshooting](#troubleshooting)

## Overview

SSH tunneling allows you to:

- Access your Vercel-deployed MCP server from local applications
- Secure communication through encrypted SSH connections
- Bypass firewall restrictions
- Test remote deployments locally

### Architecture

```
Claude Desktop (localhost:8000)
    ↓ (SSH tunnel)
SSH Server (your machine or VPS)
    ↓ (HTTPS)
Vercel Deployment (your-app.vercel.app)
    ↓
PokeAPI
```

## Prerequisites

- SSH access to a server (your machine, VPS, or cloud instance)
- SSH client installed (comes with macOS/Linux, use PuTTY for Windows)
- Your deployed Vercel app URL
- API key for authentication

## SSH Server Setup

### Option 1: Use Your Local Machine

**macOS/Linux**:

1. **Enable SSH**:

   ```bash
   # macOS
   sudo systemsetup -setremotelogin on
   
   # Linux (Ubuntu/Debian)
   sudo apt-get install openssh-server
   sudo systemctl enable ssh
   sudo systemctl start ssh
   ```

2. **Configure SSH** (optional):

   Edit `/etc/ssh/sshd_config`:
   ```
   PasswordAuthentication no  # Use keys only
   PubkeyAuthentication yes
   PermitRootLogin no
   ```

3. **Restart SSH**:

   ```bash
   # macOS
   sudo launchctl stop com.openssh.sshd
   sudo launchctl start com.openssh.sshd
   
   # Linux
   sudo systemctl restart ssh
   ```

**Windows**:

1. Install [OpenSSH Server](https://learn.microsoft.com/en-us/windows-server/administration/openssh/openssh_install_firstuse)
2. Or use WSL2 with Linux instructions above

### Option 2: Use a VPS

Providers:
- **DigitalOcean**: $4-6/month droplet
- **Linode**: $5/month instance
- **AWS EC2**: Free tier available
- **Hetzner**: €4/month

**Setup**:

```bash
# Connect to your VPS
ssh user@your-vps-ip

# Update and secure
sudo apt-get update
sudo apt-get upgrade
sudo ufw allow 22
sudo ufw enable

# Install required tools
sudo apt-get install openssh-server curl
```

### SSH Key Setup

1. **Generate SSH key** (if you don't have one):

   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. **Copy public key to server**:

   ```bash
   # Local machine
   ssh-copy-id user@server-ip
   
   # Or manually
   cat ~/.ssh/id_ed25519.pub | ssh user@server-ip "mkdir -p ~/.ssh && cat >> ~/.ssh/authorized_keys"
   ```

3. **Test connection**:

   ```bash
   ssh user@server-ip
   ```

## Local SSH Tunnel

### Basic Local Port Forwarding

Forward local port to your Vercel deployment:

```bash
ssh -L 8000:your-app.vercel.app:443 user@server-ip -N
```

**Explanation**:
- `-L 8000`: Local port to listen on
- `your-app.vercel.app:443`: Remote host and port
- `user@server-ip`: SSH server
- `-N`: No remote command (just tunnel)

### With Custom Configuration

Create `~/.ssh/config`:

```bash
Host poke-mcp-tunnel
    HostName server-ip
    User your-username
    LocalForward 8000 your-app.vercel.app:443
    ServerAliveInterval 60
    ServerAliveCountMax 3
    IdentityFile ~/.ssh/id_ed25519
```

**Connect**:

```bash
ssh -N poke-mcp-tunnel
```

### Test the Tunnel

```bash
# Health check (note: using http for local, not https)
curl http://localhost:8000/health

# With API key
curl -H "Authorization: Bearer YOUR_API_KEY" http://localhost:8000/status
```

## Reverse SSH Tunnel

For accessing a local server from remote:

```bash
# On your local machine
ssh -R 8000:localhost:8000 user@server-ip -N
```

**Use case**: Testing local development server from remote client

## MCP Client Configuration

### Claude Desktop

1. **Open Claude configuration**:

   ```bash
   # macOS
   code ~/Library/Application\ Support/Claude/claude_desktop_config.json
   
   # Linux
   code ~/.config/Claude/claude_desktop_config.json
   
   # Windows
   code %APPDATA%\Claude\claude_desktop_config.json
   ```

2. **Add MCP server configuration**:

   ```json
   {
     "mcpServers": {
       "poke-mcp-production": {
         "transport": {
           "type": "http",
           "url": "http://localhost:8000/mcp",
           "headers": {
             "Authorization": "Bearer YOUR_API_KEY"
           }
         }
       }
     }
   }
   ```

3. **Restart Claude Desktop**

4. **Start SSH tunnel** before using Claude

### Cursor

1. **Open Cursor settings**: Settings → MCP

2. **Add server**:

   ```json
   {
     "name": "poke-mcp-production",
     "type": "http",
     "url": "http://localhost:8000/mcp",
     "headers": {
       "Authorization": "Bearer YOUR_API_KEY"
     }
   }
   ```

### Generic MCP Client

```python
from mcp import MCPClient

client = MCPClient(
    transport="http",
    url="http://localhost:8000/mcp",
    headers={"Authorization": "Bearer YOUR_API_KEY"},
)
```

## Persistent Tunnels

### Using systemd (Linux)

1. **Create service file**: `/etc/systemd/system/poke-mcp-tunnel.service`

   ```ini
   [Unit]
   Description=Poke MCP SSH Tunnel
   After=network.target

   [Service]
   User=your-username
   ExecStart=/usr/bin/ssh -N -L 8000:your-app.vercel.app:443 user@server-ip -o ServerAliveInterval=60 -o ExitOnForwardFailure=yes
   Restart=always
   RestartSec=10

   [Install]
   WantedBy=multi-user.target
   ```

2. **Enable and start**:

   ```bash
   sudo systemctl daemon-reload
   sudo systemctl enable poke-mcp-tunnel
   sudo systemctl start poke-mcp-tunnel
   ```

3. **Check status**:

   ```bash
   sudo systemctl status poke-mcp-tunnel
   ```

### Using autossh

**Install**:

```bash
# macOS
brew install autossh

# Linux
sudo apt-get install autossh
```

**Run**:

```bash
autossh -M 0 -N -L 8000:your-app.vercel.app:443 user@server-ip \
  -o ServerAliveInterval=60 \
  -o ServerAliveCountMax=3 \
  -o ExitOnForwardFailure=yes
```

**Background daemon**:

```bash
autossh -M 0 -f -N -L 8000:your-app.vercel.app:443 user@server-ip
```

### Using launchd (macOS)

1. **Create plist**: `~/Library/LaunchAgents/com.pokemcp.tunnel.plist`

   ```xml
   <?xml version="1.0" encoding="UTF-8"?>
   <!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
   <plist version="1.0">
   <dict>
       <key>Label</key>
       <string>com.pokemcp.tunnel</string>
       <key>ProgramArguments</key>
       <array>
           <string>/usr/bin/ssh</string>
           <string>-N</string>
           <string>-L</string>
           <string>8000:your-app.vercel.app:443</string>
           <string>user@server-ip</string>
       </array>
       <key>RunAtLoad</key>
       <true/>
       <key>KeepAlive</key>
       <true/>
   </dict>
   </plist>
   ```

2. **Load and start**:

   ```bash
   launchctl load ~/Library/LaunchAgents/com.pokemcp.tunnel.plist
   launchctl start com.pokemcp.tunnel
   ```

## Security Best Practices

### SSH Security

1. **Use SSH keys, not passwords**
2. **Disable root login**
3. **Use strong key encryption**: Ed25519 or RSA 4096
4. **Enable firewall**: Only allow necessary ports
5. **Regular updates**: Keep SSH server updated
6. **Monitor logs**: Watch for unauthorized access attempts

### API Security

1. **Strong API keys**: Use cryptographically random keys
2. **Rotate keys regularly**: Every 90 days minimum
3. **Different keys per environment**: dev/staging/production
4. **Monitor usage**: Track API calls for anomalies

### Network Security

1. **Use VPN** when possible for additional security
2. **Restrict SSH access** by IP if possible
3. **Use fail2ban**: Protect against brute force
4. **Enable 2FA**: For SSH if supported

### SSH Hardening

Edit `/etc/ssh/sshd_config`:

```bash
# Disable password authentication
PasswordAuthentication no
PermitEmptyPasswords no

# Disable root login
PermitRootLogin no

# Use strong ciphers only
Ciphers chacha20-poly1305@openssh.com,aes256-gcm@openssh.com

# Use strong key exchange
KexAlgorithms curve25519-sha256,curve25519-sha256@libssh.org

# Use strong MACs
MACs hmac-sha2-512-etm@openssh.com,hmac-sha2-256-etm@openssh.com

# Limit login attempts
MaxAuthTries 3
MaxSessions 2

# Set timeouts
ClientAliveInterval 300
ClientAliveCountMax 2
```

## Troubleshooting

### Tunnel Won't Establish

1. **Test SSH connection**:
   ```bash
   ssh -v user@server-ip
   ```

2. **Check firewall**:
   ```bash
   # Server side
   sudo ufw status
   ```

3. **Verify port availability**:
   ```bash
   # Local machine
   lsof -i :8000
   ```

4. **Try different port**:
   ```bash
   ssh -L 8001:your-app.vercel.app:443 user@server-ip -N
   ```

### Connection Drops

1. **Use autossh** for automatic reconnection
2. **Increase keepalive**:
   ```bash
   ssh -o ServerAliveInterval=30 -o ServerAliveCountMax=5 ...
   ```
3. **Check network stability**

### Permission Denied

1. **Check SSH key permissions**:
   ```bash
   chmod 600 ~/.ssh/id_ed25519
   chmod 644 ~/.ssh/id_ed25519.pub
   chmod 700 ~/.ssh
   ```

2. **Verify key is added**:
   ```bash
   ssh-add -l
   ssh-add ~/.ssh/id_ed25519
   ```

### MCP Client Can't Connect

1. **Verify tunnel is running**:
   ```bash
   ps aux | grep ssh
   ```

2. **Test endpoint directly**:
   ```bash
   curl http://localhost:8000/health
   ```

3. **Check API key**: Ensure it's correct in client config

4. **Review logs**: Check Claude/Cursor logs for errors

### Port Already in Use

```bash
# Find process using port
lsof -i :8000

# Kill process
kill -9 PID

# Or use different port
ssh -L 8001:your-app.vercel.app:443 user@server-ip -N
```

## Alternative Solutions

### ngrok

For quick testing without SSH setup:

```bash
# Install
brew install ngrok  # macOS

# Run
ngrok http https://your-app.vercel.app

# Use provided URL in client
```

**Note**: Free tier has limitations

### Cloudflare Tunnel

For production alternative:

```bash
# Install
brew install cloudflare/cloudflare/cloudflared

# Setup
cloudflared tunnel login
cloudflared tunnel create poke-mcp
cloudflared tunnel route dns poke-mcp mcp.yourdomain.com
```

### Tailscale

For private network access:

1. Install Tailscale on all devices
2. Access server via Tailscale IP
3. No port forwarding needed

## Best Practices

1. **Use automation** (autossh, systemd) for reliability
2. **Monitor tunnel health**: Set up alerts
3. **Document configuration**: Keep notes of your setup
4. **Regular security audits**: Review SSH logs
5. **Backup configurations**: Save SSH configs
6. **Test failover**: Ensure tunnel recovery works
7. **Use connection multiplexing**: For better performance
8. **Implement logging**: Track tunnel usage

## Getting Help

- **SSH Issues**: Check `/var/log/auth.log` (Linux) or system logs
- **Network Issues**: Use `tcpdump` or Wireshark
- **MCP Issues**: Enable debug logging in client
- **Community**: Ask in MCP Discord or GitHub discussions

## Next Steps

1. Set up persistent tunnel
2. Configure your MCP client
3. Test connection thoroughly
4. Monitor and maintain
5. Consider production-grade solutions (Tailscale, Cloudflare Tunnel)
