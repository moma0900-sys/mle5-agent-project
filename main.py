from pathlib import Path
from pprint import pprint
from data_validation import (
    load_tickets,
    load_customers,
    validate_ticket_customers,
    load_evaluation_cases,
    validate_evaluation_cases,
    load_mds,
    validate_evaluation_sources,
    load_seed_memory,
    validate_seed_memory,
    load_availability,
)

from validation_tools import (
    get_ticket,
    get_customer_context,
    check_availability,
    search_policy,
    draft_ticket_update,
    draft_escalation,
    is_citation_supported,
    extract_citations,
    validate_citations,
)



ROOT = Path(__file__).resolve().parent

def main():
    validated_tickets = load_tickets(Path(ROOT/"data/operations/tickets.json"))

    for ticket in validated_tickets:
        print(type(ticket))
        print("Ticket-ID:", ticket.ticket_id)
        print("Customer-ID:", ticket.customer_id)
        print("Category:", ticket.category)
        print(f"### {ticket.subject} ###")
        pprint(ticket.body)
        print("="*60)


    validated_customers = load_customers(Path(ROOT/"data/operations/customers.json"))

    for customer in validated_customers:
        print(type(customer))
        print("Customer-ID:", customer.customer_id)
        print("Name:", customer.name)
        print(customer.email)
        print("Business plan:", customer.plan)
        print("Verified =", customer.verified)
        print("="*60)


    validate_ticket_customers(validated_tickets, validated_customers)


    validated_evaluation = load_evaluation_cases(Path(ROOT/"data/evaluation/agent_cases.json"))

    for case in validated_evaluation:
        print(type(case))
        print("Case-ID:", case.case_id)
        print("Ticket-ID:", case.ticket_id)
        pprint(case.prompt)
        print("Expected Status:", case.expected_status)
        print("Expected Tools:", case.expected_tools)
        print("Expected Sources:", case.expected_sources)
        print("Use of Memory =", case.must_use_memory)
        print("Forbidden Tools =", case.forbidden_tools)
        print("Expected safety events =", case.expected_safety_events)
        print("="*60)


    validate_evaluation_cases(validated_evaluation, validated_tickets)


    validated_policies = load_mds(Path(ROOT/"data/knowledge_base"))
    for policie in validated_policies:
        pprint(policie)
        print("="*60)


    validate_evaluation_sources(validated_evaluation, validated_policies)


    seed_memory = load_seed_memory(Path(ROOT/"data/operations/seed_memory.json"))
    pprint(seed_memory)
    print("="*60)
    validate_seed_memory(seed_memory, validated_tickets)


    contact_persons = load_availability(Path(ROOT/"data/operations/availability.json"))
    pprint(contact_persons)
    print("="*60)

    trace = []
    ticket = get_ticket("T-1002", trace ,validated_tickets)
    pprint(ticket)
    print(trace)
    print("="*60)

    customer = get_customer_context(ticket.customer_id, trace, validated_customers)
    pprint(customer)
    print(trace)
    print("="*60)

    contact = check_availability("identity-review", trace, contact_persons)
    pprint(contact)
    print(trace)
    print("="*60)

    hit = search_policy("MFA",  trace, validated_policies)
    print(validate_citations("Prüfe die Backup-Codes. [account-access]", hit))
    print(validate_citations("Siehe [account-access] und [refunds].", hit))
    print(validate_citations("Prüfe die Backup-Codes.", hit))
    pprint(hit)
    print(trace)
    print("="*60)

    print(is_citation_supported("account-access", hit))

    print(extract_citations("Prüfe die Backup-Codes. [account-access]"))
    print(extract_citations("Siehe [account-access] und [escalation-rules]."))
    print(extract_citations("Keine passenden Belege gefunden."))
    print("="*60)

    draft = draft_ticket_update(ticket.ticket_id, "MFA-restored", trace)
    pprint(draft)
    print(trace[-1])
    print("="*60)

    escalation = draft_escalation("T-1003", "incident-response", "Several customers report a checkout failure.", trace)
    pprint(escalation)
    print(trace[-1])
    print("="*60)



if __name__ == "__main__":
    main()