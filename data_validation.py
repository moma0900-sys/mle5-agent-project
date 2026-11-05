import json
from models import (
    Ticket,
    Customer,
    EvaluationCase,
    Policy,
    SeedMemory,
    Availability,
)


def load_tickets(tickets_path) -> list[Ticket]:
    tickets_text = tickets_path.read_text(encoding="utf-8")

    tickets = json.loads(tickets_text)
    if not isinstance(tickets, list):
        raise TypeError(f"Must contain a list: {tickets_path}")

    validated_tickets = []

    for ticket in tickets:
        if not isinstance(ticket, dict):
            raise TypeError("Each ticket must be a Dictionary.")

        validated_tickets.append(Ticket.model_validate(ticket))

    ticket_ids=[]
    for ticket in validated_tickets:
        ticket_ids.append(ticket.ticket_id)

    # Anzahl Ticket_IDs = Anzahl unterschiedlicher Ticket_IDs?
    if len(ticket_ids) != len(set(ticket_ids)):
        raise ValueError(f"Duplicate Ticket-IDs found in {tickets_path}.")

    return validated_tickets



def load_customers(customer_path) -> list[Customer]:
    customers_text = customer_path.read_text(encoding="utf-8")

    customers = json.loads(customers_text)

    if not isinstance(customers, list):
            raise TypeError(f"Must contain a list: {customer_path}")

    validated_customers = []

    for customer in customers:
        if not isinstance(customer, dict):
            raise TypeError("Each ticket must be a Dictionary.")

        validated_customers.append(Customer.model_validate(customer))

    customer_ids=[]
    for customer in validated_customers:
        customer_ids.append(customer.customer_id)

    # Keine doppelte Cusomer-ID?
    if len(customer_ids) != len(set(customer_ids)):
        raise ValueError(f"Duplicate Ticket-IDs found in {customer_path}.")

    return validated_customers



# Check if each ticket ID from tickets.json has a valid customer ID from customer.json
def validate_ticket_customers(tickets: list[Ticket], customers: list[Customer]) -> None:
    customer_ids = set()

    for customer in customers:
        customer_ids.add(customer.customer_id)

    for ticket in tickets:
        if ticket.customer_id not in customer_ids:
            raise ValueError(f"Customer-ID '{ticket.customer_id}' from Ticket '{ticket.ticket_id}' not found in Customer-List.")
        else:
            print(f"No violation, customer {ticket.customer_id} in {ticket.ticket_id} is valid.")
    print("="*60)



def load_evaluation_cases(evaluation_path) -> list[EvaluationCase]:
    evaluation_text = evaluation_path.read_text(encoding="utf-8")

    evaluation = json.loads(evaluation_text)

    if not isinstance(evaluation, list):
        raise TypeError(f"Must contain a list: {evaluation_path}")
    
    validated_evaluation = []
    
    for case in evaluation:
        if not isinstance(case, dict):
            raise TypeError("Each case must be a Dictionary.")
    
        validated_evaluation.append(EvaluationCase.model_validate(case))

    case_ids=[]
    for case in validated_evaluation:
        case_ids.append(case.case_id)
    
    # Keine doppelte Cusomer-ID?
    if len(case_ids) != len(set(case_ids)):
        raise ValueError(f"Duplicate Case-IDs found in {evaluation_path}.")

    return validated_evaluation



# Check if each ticket ID from tickets.json has a valid ID from agent_cases.json
def validate_evaluation_cases(cases: list[EvaluationCase], tickets:list[Ticket]) -> None:
    ticket_ids = set()
    for ticket in tickets:
        ticket_ids.add(ticket.ticket_id)

    for case in cases:
        if case.ticket_id is not None and case.ticket_id not in ticket_ids:
                raise ValueError(f"Case-ID '{case.case_id}' has unknown Ticket-ID '{case.ticket_id}'.")



def load_mds(policies_path) -> list[Policy]:
    policies = []

    for policy in policies_path.glob("*.md"):
        raw_text = policy.read_text(encoding="utf-8").strip()
        if not raw_text:
            raise ValueError(f"Document {policy.name} is empty.")

        # get MD-Title
        lines = raw_text.splitlines()
        if not lines[0].startswith("# "):
            raise ValueError(f"No Title found in {policy.name}")

        title = lines[0].removeprefix("# ").strip()

        # get Source ID
        # List to check if there are several Source-IDs in a MD-file
        source_ids = []
        for line in lines:
            if line.startswith("Source ID:"):
                source_ids.append(line.removeprefix("Source ID:").strip())
        if len(source_ids) != 1:
            raise ValueError(f"Expected exactly one source ID in {policy.name}")

        source_id = source_ids[0]

        # get Text
        body = []

        for line in lines[1:]:
            if not line.startswith("Source ID:"):
                body.append(line)

        text = "\n".join(body).strip()

        policies.append(Policy(source_id=source_id, title=title, text=text))


    loaded_source_ids = []
    for policy in policies:
        loaded_source_ids.append(policy.source_id)

    # Keine doppelte Source-ID?
    if len(loaded_source_ids) != len(set(loaded_source_ids)):
        raise ValueError(f"Duplicate Source-IDs found in {policies_path}.")

    return policies



def validate_evaluation_sources(cases: list[EvaluationCase], policies: list[Policy]) -> None:
    source_ids = set()

    for policy in policies:
        source_ids.add(policy.source_id)

    for case in cases:
        for source_id in case.expected_sources:
            if source_id not in source_ids:
                raise ValueError(f"{source_id} not found in {case.case_id}")



def load_seed_memory(seed_path) -> SeedMemory:
    raw = seed_path.read_text(encoding="utf-8")
    
    data = json.loads(raw)

    if not isinstance(data, dict):
        raise ValueError (f"Expected a JSON object in {seed_path}.")

    return SeedMemory.model_validate(data)



def validate_seed_memory(seed_memory: SeedMemory, tickets: list[Ticket]) -> None:
    for ticket in tickets:
        if ticket.ticket_id == seed_memory.last_ticket_id and ticket.customer_id != seed_memory.last_customer_id:
                raise ValueError (f"Wrong Customer-ID {seed_memory.last_customer_id} in Memory {seed_memory.conversation_id}. Expected: {ticket.customer_id}")

        elif ticket.ticket_id == seed_memory.last_ticket_id and ticket.customer_id == seed_memory.last_customer_id:
            return

    raise ValueError(f"No Ticket found with {seed_memory.last_ticket_id}.")



def load_availability(availability_path) -> list[Availability]:
    raw = availability_path.read_text(encoding="utf-8")

    entries = json.loads(raw)

    if not isinstance(entries, list):
            raise TypeError(f"Must contain a list: {availability_path}")

    validated_entries = []

    for entry in entries:
        if not isinstance(entry, dict):
            raise TypeError("Each entry must be a Dictionary.")

        validated_entries.append(Availability.model_validate(entry))

    return validated_entries