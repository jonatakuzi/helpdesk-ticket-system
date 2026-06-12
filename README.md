# Helpdesk CLI

A lightweight command-line IT support ticket tracker built with Python and SQLite. Log, prioritize, track, and resolve technical support issues without needing a full helpdesk platform — runs entirely locally with no server required.

![Python](https://img.shields.io/badge/Python-3.7%2B-blue?logo=python&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-lightblue?logo=sqlite)
![Dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)
![License](https://img.shields.io/badge/license-MIT-green)

## Features

- Create tickets with four priority levels: `low`, `medium`, `high`, `critical`
- List all tickets or filter by status (`open`, `in-progress`, `resolved`)
- Update ticket status and append timestamped resolution notes
- View full ticket history with all notes
- Persistent local storage via SQLite — no setup, no config
- No external dependencies — standard library only

## Requirements

- Python 3.7+
- No `pip install` needed

## Installation

```bash
git clone https://github.com/jonatakuzi/helpdesk-ticket-system.git
cd helpdesk-ticket-system
```

## Usage

### Open a new ticket
```bash
python helpdesk.py new "Outlook not loading after Windows update"
python helpdesk.py new "VPN drops every 30 minutes" --priority high
python helpdesk.py new "Server CPU at 98%" --priority critical
```

### List all open tickets
```bash
python helpdesk.py list
python helpdesk.py list --status in-progress
python helpdesk.py list --status resolved
```
```
ID  Priority   Status      Title
──────────────────────────────────────────────────────
1   critical   open        Server CPU at 98%
2   high       in-progress VPN drops every 30 minutes
3   low        open        Outlook not loading
```

### Update a ticket
```bash
python helpdesk.py update 2 --status resolved --note "Reinstalled VPN client v4.2, issue resolved"
```

### View ticket details and history
```bash
python helpdesk.py view 2
```

### Close a ticket
```bash
python helpdesk.py close 1
```

## Tech Stack

- Python 3.7+
- SQLite3 (built into Python stdlib)
- Standard library: `sqlite3`, `argparse`, `datetime`
