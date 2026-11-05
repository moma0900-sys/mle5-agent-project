from pydantic import BaseModel, Field, ConfigDict
from typing import Literal


class Ticket(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    ticket_id: str = Field(min_length=1)
    customer_id: str = Field(min_length=1)
    category: str = Field(min_length=1)
    subject: str = Field(min_length=1)
    body: str = Field(min_length=1)


class Customer(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    customer_id: str = Field(min_length=1)
    name: str = Field(min_length=1)
    email: str = Field(min_length=1)
    plan: str = Field(min_length=1)
    verified: bool


class EvaluationCase(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    case_id: str = Field(min_length=1)
    ticket_id: str | None
    prompt: str = Field(min_length=1)
    expected_status: Literal["answered", "abstained", "escalated", "review_required"]
    expected_tools: list[str]
    expected_sources: list[str]
    must_use_memory: bool
    forbidden_tools: list[str] = Field(default_factory=list)    # default_factory=list erzeugt falls forbidden_tools[] = leer, eine leere Liste
    expected_safety_events: list[str] = Field(default_factory=list)


class Policy(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    source_id: str = Field(min_length=1)
    title: str = Field(min_length=1)
    text: str = Field(min_length=1)


class SeedMemory(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    conversation_id: str = Field(min_length=1)
    last_ticket_id: str = Field(min_length=1)
    last_customer_id: str = Field(min_length=1)
    notes: list[str] = Field(min_length=1)


class Availability(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    queue: str = Field(min_length=1)
    owner: str = Field(min_length=1)
    channel: str = Field(min_length=1)
    available: bool


class TicketUpdateDraft(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    ticket_id: str = Field(min_length=1)
    text: str = Field(min_length=1)


class EscalationDraft(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)
    ticket_id: str = Field(min_length=1)
    queue: str = Field(min_length=1)
    reason: str = Field(min_length=1)