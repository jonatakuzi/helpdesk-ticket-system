# Helpdesk CLI

A lightweight command-line IT support ticket tracker built with Python and SQLite. Designed for small teams or personal use to log, track, and resolve technical support issues without needing a full-blown helpdesk platform.

## Features

- Create tickets with priority levels (low / medium / high / critical)
- List all tickets or filter by status
- Update ticket status and add resolution notes
- View full ticket history with timestamped notes
- Persistent local storage via SQLite (no server required)

## Requirements

- Python 3.7+
- No external dependencies — uses only the standard library

## Installation

```bash
git clone https://github.com/jonatakuzi/helpdesk-ticket-system.git
cd helpdesk-ticket-system
```

## Usage

### Open a new ticket
```bash
python helpdesk.py new "Outlook not loading after Windows update"
python helpdesk.py new "VPN drops connection every 30 minutes" --priority high
```

### List all tickets
```bash
python helpdesk.py list
python helpdesk.py list --status open
```

### Update a ticket
```bash
python helpdesk.py update 2 --status in-progress --note "Checking logs"
python helpdesk.py update 2 --status resolved --note "Updated network driver, fixed"
```

### View ticket details
```bash
python helpdesk.py show 2
```

### Close a ticket
```bash
python helpdesk.py close 2 --note "User confirmed fix worked"
```

## Project Structure

```
helpdesk-ticket-system/
├── helpdesk.py   # CLI entry point and command handlers
├── db.py         # SQLite database layer
└── README.md
```

## Why I Built This

I wanted a no-frills way to track support issues locally without spinning up a web server or signing up for a SaaS tool. This covers the core workflow: log it, work it, close it.
