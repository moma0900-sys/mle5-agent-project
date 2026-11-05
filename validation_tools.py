import re

from models import(
    Ticket, Customer,
    Availability,
    Policy,
    TicketUpdateDraft,
    EscalationDraft
)


# trace -> Dict mit Schlüssel und Wert als String. Wie viele Schlüssel-Wert-Paare das Dictionary enthält, ist offen.
def get_ticket(ticket_id: str, trace: list[dict[str, str]], tickets: list[Ticket]) -> Ticket:
    for ticket in tickets:
        if ticket.ticket_id == ticket_id:
            trace.append({"tool": "get_ticket", "ticket_id": ticket_id, "status": "found"})
            return ticket

    trace.append({"tool": "get_ticket", "ticket_id": ticket_id, "status": "not_found"})
    raise ValueError(f"No ticket found with Ticket-ID {ticket_id} in 'tickets.json'.")



def get_customer_context(customer_id: str, trace: list[dict[str, str]], customers: list[Customer]) -> Customer:
    for customer in customers:
        if customer.customer_id == customer_id:
            trace.append({"tool": "get_customer_context", "customer_id": customer_id, "status": "found"})
            return customer

    trace.append({"tool": "get_customer_context", "customer_id": customer_id, "status": "not_found"})
    raise ValueError(f"Customer-ID {customer_id} not found in 'customers.json'.")



def check_availability(queue: str, trace: list[dict[str, str]], contacts: list[Availability]) -> Availability:
    for contact in contacts:
        if contact.queue == queue:
            trace.append({"tool": "check_availability", "queue": queue, "status": "found"})
            return contact

    trace.append({"tool": "check_availability", "queue": queue, "status": "not_found"})
    raise ValueError(f"Queue {queue} not found in 'availability.json'.")



def search_policy(query: str, trace: list[dict[str, str]], policies: list[Policy]) -> list[Policy]:
    matches = []
    for policy in policies:
        if query.casefold() in policy.title.casefold() or query.casefold() in policy.text.casefold():
            matches.append(policy)

    if matches:
        trace.append({"tool": "search_policy", "query": query, "status": "found"})
    else:
        trace.append({"tool": "search_policy", "query": query, "status": "not_found"})
    return matches



def is_citation_supported(source_id: str, evidence: list[Policy]) -> bool:
    for policy in evidence:
        if policy.source_id == source_id:
            return True
    return False



def extract_citations(answer: str) -> list[str]:
    # \[ und \] erkennen die eckigen Klammern
    # ([a-z0-9-]+) erfasst die ID dazwischen
    return re.findall(r"\[([a-z0-9-]+)\]", answer)



def validate_citations(answer: str, evidence: list[Policy]) -> bool:
    extract = extract_citations(answer)
    if not extract:
        return False
    for source_id in extract:
        if not is_citation_supported(source_id, evidence):
            return False
    return  True



def draft_ticket_update(ticket_id: str, text: str,trace: list[dict[str, str]]) -> TicketUpdateDraft:
    draft = TicketUpdateDraft(ticket_id=ticket_id, text=text)
    trace.append({"tool": "draft_ticket_update", "ticket_id": ticket_id, "status": "drafted"})
    return draft



def draft_escalation(ticket_id: str, queue: str, reason: str, trace: list[dict[str, str]]) -> EscalationDraft:
    draft = EscalationDraft(ticket_id=ticket_id, queue=queue, reason=reason)
    trace.append({"tool": "draft_escalation", "ticket_id": ticket_id, "queue": queue, "status": "drafted"})
    return draft