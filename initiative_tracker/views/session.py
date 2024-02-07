import uuid

from fastapi import APIRouter
from initiative_tracker.models.common import Status
from starlette.exceptions import HTTPException

from initiative_tracker.models.session import (
    Session,
    Event,
    SessionReadSchema,
    SessionWriteSchema,
    EventReadSchema,
    EventWriteSchema,
)

session_router = APIRouter(
    prefix="/sessions",
    tags=["sessions"],
)


# these are drafts

@session_router.get("/sessions", response_model=list[SessionReadSchema])
async def get_sessions():
    return await SessionReadSchema.from_queryset(Session.all())


@session_router.get("/sessions/{session_id}", response_model=SessionReadSchema)
async def get_session(session_id: uuid.UUID):
    return await SessionReadSchema.from_queryset_single(Session.get(id=session_id))


@session_router.post("/sessions", response_model=SessionReadSchema)
async def create_session(session: SessionWriteSchema):
    session_obj = await Session.create(**session.model_dump(exclude_unset=True))
    return await SessionReadSchema.from_tortoise_orm(session_obj)


@session_router.put("/session/{session_id}", response_model=SessionReadSchema)
async def update_session(session_id: uuid.UUID, session: SessionWriteSchema):
    await Session.filter(id=session_id).update(**session.model_dump(exclude_unset=True))
    return await SessionReadSchema.from_queryset_single(Session.get(id=session_id))


@session_router.delete("/session/{session_id}", response_model=Status)
async def delete_session(session_id: uuid.UUID):
    deleted_count = await Session.filter(id=session_id).delete()
    if not deleted_count:
        raise HTTPException(status_code=404, detail=f"Session {session_id} not found")
    return Status(code=201, message=f"Deleted session {session_id}")


@session_router.get("/session/{session_id}/events", response_model=list[EventReadSchema])
async def get_events(session_id: uuid.UUID):
    return await EventReadSchema.from_queryset(Event.filter(session_id=session_id))


@session_router.post("/session/{session_id}/events", response_model=EventReadSchema)
async def create_event(session_id: uuid.UUID, event: EventWriteSchema):
    event_obj = await Event.create(
        **event.model_dump(exclude_unset=True), session_id=session_id
    )
    return await EventReadSchema.from_tortoise_orm(event_obj)


@session_router.delete("/session/{session_id}/events/{event_id}", response_model=Status)
async def delete_event(session_id: uuid.UUID, event_id: uuid.UUID):
    session = await Session.get_or_none(id=session_id)
    event = await Event.get_or_none(session_id=session_id, id=event_id)
    if not event or not session:
        raise HTTPException(status_code=404, detail=f"Event {event_id} not found")
    latest_event = (
        await Event.filter(session_id=session_id).order_by("-order_index").first()
    )
    if latest_event is not None and event.order_index < latest_event.order_index:
        raise HTTPException(
            status_code=400,
            detail=f"Event {event_id} is in the past and cannot be deleted",
        )
    await Event.filter(session_id=session_id, id=event_id).delete()
    return Status(code=201, message=f"Deleted event {event_id}")
