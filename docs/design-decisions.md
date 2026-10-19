# Design Decisions

## Ownership
- Engineer A (Ochulu Agbenu): errors.py, tickets.py, storage.py, and their tests
- Engineer B (Raymond Nicholas): workflow.py, reports.py, and their tests
- Both: main.py, README, docs

## Agreed decisions
1. **Ticket storage:** a list of dicts, passed as the first argument to every function.
2. **Errors:** functions raise exceptions from errors.py; main.py catches CampusFlowError and prints the message.
3. **Return values:** mutating functions return the affected ticket dict.
4. **JSON:** only storage.py reads and writes files; the path is a parameter.
5. **Testability:** no input() or print() outside main.py.
6. **affected_users input:** create_ticket accepts an int or a digit-only string; bools, zero, negatives and decimals are rejected.
7. **Work queue:** includes only tickets with status "open". The queue is for work nobody has started; an in_progress ticket already has an owner.
8. **Reopen:** keeps assigned_to. Reopening only changes the status, and the previous assignee already knows the problem, so we keep them.
9. **Resolved tickets:** cannot be assigned or changed until explicitly reopened.
10. **IDs:** T001 format, highest existing number + 1, compared numerically, never as text.

## Function contracts
- tickets.py: calculate_priority(urgency, affected_users) -> str
- tickets.py: create_ticket(tickets, title, category, urgency, affected_users) -> dict
- tickets.py: find_ticket(tickets, ticket_id) -> dict  (raises TicketNotFoundError)
- tickets.py: ticket_number(ticket_id) -> int
- workflow.py: assign_ticket(tickets, ticket_id, staff_name) -> dict
- workflow.py: change_status(tickets, ticket_id, new_status) -> dict
- reports.py: get_work_queue(tickets) -> list[dict]
- reports.py: build_report(tickets) -> dict
- storage.py: load_tickets(path) -> list[dict]
- storage.py: save_tickets(path, tickets) -> None

## Failure rule
Every function validates first and mutates last, so a rejected call leaves the ticket list unchanged.