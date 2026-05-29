#!/usr/bin/env python3
"""
helpdesk.py - Command-line IT support ticket tracker.
Stores all tickets in a local SQLite database via the TicketDB class in db.py.
Data persists between runs, so closing the terminal does not lose your tickets.

Usage:
  python helpdesk.py new "Laptop won't connect to VPN"
  python helpdesk.py new "Monitor flickering" --priority high
  python helpdesk.py list
  python helpdesk.py list --status open
  python helpdesk.py search "VPN"
  python helpdesk.py update 3 --status resolved --note "Reinstalled VPN client"
  python helpdesk.py show 3
  python helpdesk.py close 3
"""

import argparse
import sys
from db import TicketDB


def cmd_new(db, args):
    """
    Create a new ticket and save it to the SQLite database.
    Priority defaults to 'medium' if not specified.
    Prints the assigned ticket ID so the user can reference it later.
    """
    ticket_id = db.create_ticket(args.title, priority=args.priority)
    print(f"[+] Ticket #{ticket_id} created: {args.title} (Priority: {args.priority})")


def cmd_list(db, args):
    """
    List all tickets, optionally filtered by status (open, resolved, closed).
    Formats output as a fixed-width table for readability in the terminal.
    If no tickets match the filter, prints a friendly message instead of crashing.
    """
    tickets = db.list_tickets(status=args.status)
    if not tickets:
        print("No tickets found.")
        return
    print(f"\n{'ID':<5} {'Status':<12} {'Priority':<10} {'Title':<40} {'Created'}")
    print("-" * 85)
    for t in tickets:
        print(f"{t['id']:<5} {t['status']:<12} {t['priority']:<10} {t['title'][:38]:<40} {t['created_at'][:16]}")
    print()


def cmd_search(db, args):
    """
    Search tickets by keyword in the title.
    Performs a case-insensitive match, useful when you remember part of an issue
    but not the exact ticket number.
    """
    tickets = db.list_tickets()
    keyword = args.keyword.lower()
    matches = [t for t in tickets if keyword in t['title'].lower()]
    if not matches:
        print(f"No tickets matching '{args.keyword}'.")
        return
    print(f"\nSearch results for '{args.keyword}':")
    print(f"\n{'ID':<5} {'Status':<12} {'Priority':<10} {'Title':<40} {'Created'}")
    print("-" * 85)
    for t in matches:
        print(f"{t['id']:<5} {t['status']:<12} {t['priority']:<10} {t['title'][:38]:<40} {t['created_at'][:16]}")
    print()


def cmd_update(db, args):
    """
    Update a ticket status and optionally append a note explaining what was done.
    Notes are timestamped and stored separately for a full audit trail.
    """
    db.update_ticket(args.id, status=args.status, note=args.note)
    print(f"[~] Ticket #{args.id} updated.")


def cmd_show(db, args):
    """
    Show full details for a single ticket, including all notes in chronological order.
    """
    ticket = db.get_ticket(args.id)
    if not ticket:
        print(f"Ticket #{args.id} not found.")
        return
    print(f"\n  Ticket #{ticket['id']}")
    print(f"  Title    : {ticket['title']}")
    print(f"  Status   : {ticket['status']}")
    print(f"  Priority : {ticket['priority']}")
    print(f"  Created  : {ticket['created_at']}")
    print(f"  Updated  : {ticket['updated_at']}")
    notes = db.get_notes(args.id)
    if notes:
        print(f"\n  Notes:")
        for n in notes:
            print(f"    [{n['created_at'][:16]}] {n['note']}")
    print()


def cmd_close(db, args):
    """
    Shortcut to mark a ticket as closed with an optional note.
    Equivalent to running: update --status closed
    """
    db.update_ticket(args.id, status="closed", note=args.note)
    print(f"[v] Ticket #{args.id} closed.")


def main():
    parser = argparse.ArgumentParser(
        description="Helpdesk CLI - lightweight IT support ticket tracker",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    sub = parser.add_subparsers(dest="command", required=True)

    p_new = sub.add_parser("new", help="Open a new ticket")
    p_new.add_argument("title", help="Short description of the issue")
    p_new.add_argument("--priority", choices=["low", "medium", "high", "critical"], default="medium")

    p_list = sub.add_parser("list", help="List all tickets")
    p_list.add_argument("--status", choices=["open", "in_progress", "resolved", "closed"])

    p_search = sub.add_parser("search", help="Search tickets by keyword in title")
    p_search.add_argument("keyword", help="Keyword to search for")

    p_update = sub.add_parser("update", help="Update a ticket status or add a note")
    p_update.add_argument("id", type=int)
    p_update.add_argument("--status", choices=["open", "in_progress", "resolved", "closed"])
    p_update.add_argument("--note")

    p_show = sub.add_parser("show", help="Show full details for a ticket")
    p_show.add_argument("id", type=int)

    p_close = sub.add_parser("close", help="Close a ticket")
    p_close.add_argument("id", type=int)
    p_close.add_argument("--note")

    args = parser.parse_args()
    db = TicketDB()

    commands = {
        "new": cmd_new,
        "list": cmd_list,
        "search": cmd_search,
        "update": cmd_update,
        "show": cmd_show,
        "close": cmd_close,
    }
    commands[args.command](db, args)


if __name__ == "__main__":
    main()
