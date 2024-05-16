from enum import Enum
from typing import Annotated, Any

from fastapi import APIRouter, Body, File, HTTPException
from sqlmodel import func, select

from app import config
from app.deps import SessionDep
from app.models import Lead, LeadBase, LeadPublic, LeadsPublic
from app.utils import generate_new_lead_email, send_email


class StateName(str, Enum):
    pending = "pending"
    reached_out = "reached_out"


router = APIRouter()


@router.get("/", response_model=LeadsPublic)
def get_leads(
    session: SessionDep, skip: int = 0, limit: int = 100
) -> Any:
    """
    Retrieve leads. Can use query parameter to limit output.
    """

    count_statement = select(func.count()).select_from(Lead)
    count = session.exec(count_statement).one()
    statement = select(Lead).offset(skip).limit(limit)
    leads = session.exec(statement).all()

    return LeadsPublic(data=leads, count=count)


@router.post("/", response_model=LeadPublic)
def create_lead(*, session: SessionDep, lead_in: LeadBase, resume: Annotated[bytes, File()]) -> Any:
    """
    Create new lead.
    """
    lead = Lead.model_validate(
        lead_in,
        update={"resume": resume, "state": StateName.pending}
    )
    session.add(lead)
    session.commit()
    session.refresh(lead)

    # TODO replace with BackgroundTasks
    email_data = generate_new_lead_email(
        first_name=lead_in.first_name, last_name=lead_in.last_name
    )
    send_email(
        email_to=[lead_in.email, config.LAWYER_EMAIL],
        subject=email_data.subject,
        html_content=email_data.html_content,
    )
    return lead


@router.put("/{id}", response_model=LeadPublic)
def update_lead(
    *, session: SessionDep, id: int, new_state: Annotated[StateName, Body()]
) -> Any:
    """
    Update a lead (e.g. change state to "reached_out").
    """
    lead = session.get(Lead, id)
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    update_dict = lead.model_dump(exclude_unset=True)
    update_dict["state"] = new_state
    lead.sqlmodel_update(update_dict)
    session.add(lead)
    session.commit()
    session.refresh(lead)
    return lead
