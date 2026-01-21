# Frappe CRM MCP Server

An [MCP](https://modelcontextprotocol.io/) server that lets AI assistants interact with [Frappe CRM](https://frappe.io/crm).

## Why?

Frappe CRM is a powerful open-source CRM. This MCP server gives AI assistants (like Claude) direct access to your CRM data, enabling natural language interactions:

- "Show me all open deals"
- "Create a lead for John at Acme Corp"
- "What's happening with the Tesla deal?"
- "Add a note to the Stripe deal about our call today"

## Installation

Requires Python 3.11+.

### From PyPI (recommended)

```bash
# Using uvx (no install needed)
uvx frappe-crm-mcp

# Or install with pip
pip install frappe-crm-mcp
```

### From source

```bash
git clone https://github.com/joehaddad2000/frappe-crm-mcp.git
cd frappe-crm-mcp
uv sync
```

## Configuration

### 1. Generate Frappe API Keys

1. Log into your Frappe CRM instance
2. Go to **User** → your user → **API Access**
3. Click **Generate Keys**
4. Save the API Key and API Secret

### 2. Add to Claude Code

```bash
claude mcp add frappe-crm \
  -s user \
  -e FRAPPE_URL=https://your-site.frappe.cloud \
  -e FRAPPE_API_KEY=your_api_key \
  -e FRAPPE_API_SECRET=your_api_secret \
  -- uvx frappe-crm-mcp
```

### 3. Add to Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "frappe-crm": {
      "command": "uvx",
      "args": ["frappe-crm-mcp"],
      "env": {
        "FRAPPE_URL": "https://your-site.frappe.cloud",
        "FRAPPE_API_KEY": "your_api_key",
        "FRAPPE_API_SECRET": "your_api_secret"
      }
    }
  }
}
```

## Available Tools

### Deals
- `deals_list` - List deals with optional filters
- `deals_get` - Get a single deal
- `deals_create` - Create a new deal
- `deals_update` - Update deal fields

### Leads
- `leads_list` - List leads with optional filters
- `leads_get` - Get a single lead
- `leads_update` - Update lead fields
- `leads_convert` - Convert a lead to a deal

### Contacts
- `contacts_search` - Search contacts by name/email
- `contacts_get` - Get a single contact
- `contacts_get_deals` - Get deals linked to a contact

### Organizations
- `organizations_list` - List organizations
- `organizations_get` - Get a single organization

### Notes
- `notes_list` - List notes on a deal or lead
- `notes_add` - Add a note to a deal or lead

### Tasks
- `tasks_list` - List tasks with optional filters
- `tasks_get` - Get a single task
- `tasks_add` - Create a new task
- `tasks_update` - Update task fields

### Activities
- `activities_get` - Get activity timeline for a deal or lead

## Development

```bash
# Install dependencies
uv sync

# Run the server (for testing)
FRAPPE_URL=... FRAPPE_API_KEY=... FRAPPE_API_SECRET=... uv run python -m frappe_crm_mcp.server

# Test with FastMCP dev tools
FRAPPE_URL=... FRAPPE_API_KEY=... FRAPPE_API_SECRET=... uv run fastmcp dev src/frappe_crm_mcp/server.py
```

## License

MIT
