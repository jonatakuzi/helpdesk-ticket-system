#!/usr/bin/env python3
"""
helpdesk.py - Command-line IT support ticket tracker
Usage:
  python helpdesk.py new "Laptop won't connect to VPN"
  python helpdesk.py list
  python helpdesk.py update 3 --status resolved --note "Reinstalled VPN client"
  python helpdesk.py show 3
"""

import argparse
import sys
from db import TicketDB

def cmd_new(db, args):
    ticket_id = db.create_ticket(args.title, priority=args.priority)
    print(f"[+] Ticket #{ticket_id} created: {args.title} (Priority: {args.priority})")

def cmd_list(db, args):
    tickets = db.list_tickets(status=args.status)
    if not tickets:
        print("No tickets found.")
        return
    print(f"\n{'ID':<5} {'Status':<12} {'Priority':<10} {'Title':<40} {'Created'}")
    print("-" * 85)
    for t in tickets:
        print(f"{t['id']:<5} {t['status']:<12} {t['priority']:<10} {t['title'][:38]:<40} {t['created_at'][:16]}")
    print()

def cmd_update(db, args):
    db.update_ticket(args.id, status=args.status, note=args.note)
    print(f"[v] Ticket #{args.id} updated.")
    if args.status:
        print(f"    Status  -> {args.status}")
    if args.note:
        print(f"    Note    -> {args.note}")

def cmd_show(db, args):
    ticket = db.get_ticket(args.id)
    if not ticket:
        print(f"Ticket #{args.id} not found.")
        return
    print(f"\n{'='*50}")
    print(f"Ticket #{ticket['id']}: {ticket['title']}")
    print(f"{'='*50}")
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
    p_new.add_argument("--priority", choices=["low","medium","high","critical"],
                       default="medium")

    p_list = sub.add_parser("list", help="List tickets")
    p_list.add_argument("--status", choices=["open","in-progress","resolved","closed"])

    p_update = sub.add_parser("update", help="Update a ticket")
    p_update.add_argument("id", type=int)
    p_update.add_argument("--status", choices=["open","in-progress","resolved","closed"])
    p_update.add_argument("--note")

    p_show = sub.add_parser("show", help="Show ticket details")
    p_show.add_argument("id", type=int)

    p_close = sub.add_parser("close", help="Close a ticket")
    p_close.add_argument("id", type=int)
    p_close.add_argument("--note")

    args = parser.parse_args()
    db = TicketDB()
    dispatch = {"new": cmd_new, "list": cmd_list, "update": cmd_update, "show": cmd_show, "close": cmd_close}
    dispatch[args.command](db, args)

if __name__ == "__main__":
    main()
