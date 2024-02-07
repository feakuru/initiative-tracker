from typing import TypeAlias
from tortoise import fields, models
from tortoise.contrib.postgres import fields as pg_fields
from tortoise.contrib.pydantic import pydantic_model_creator


class Session(models.Model):
    """
    A play session.
    """

    id = fields.UUIDField(pk=True)
    campaign_id = fields.UUIDField()
    host_id = fields.UUIDField()
    players = pg_fields.ArrayField(element_type="jsonb")
    title = fields.TextField()
    created_at = fields.DatetimeField(auto_now_add=True)
    modified_at = fields.DatetimeField(auto_now=True)
    events = fields.ReverseRelation["Event"]


class Event(models.Model):
    """
    An event that occurs in a session.
    This is any action - by the player, DM, NPC, world, etc.
    """

    session: fields.ForeignKeyRelation[Session] = fields.ForeignKeyField("models.Session", related_name="events")
    order_index = fields.IntField()
    created_at = fields.DatetimeField(auto_now_add=True)
    notes = fields.TextField()
    type = fields.TextField()
    data = fields.JSONField()
    actor_id = fields.UUIDField(null=True)
    actor_type = fields.TextField()
    object_id = fields.UUIDField(null=True)
    object_type = fields.TextField()  # TODO: change to enum


# TODO implement wrappers to have this done automatically
SessionReadSchema: TypeAlias = pydantic_model_creator(  # type: ignore[valid-type]
    Session, name="SessionReadSchema",
)
SessionWriteSchema: TypeAlias = pydantic_model_creator(  # type: ignore[valid-type]
    Session, name="SessionWriteSchema", exclude_readonly=True,
)
EventReadSchema: TypeAlias = pydantic_model_creator(  # type: ignore[valid-type]
    Event, name="EventReadSchema",
)
EventWriteSchema: TypeAlias = pydantic_model_creator(  # type: ignore[valid-type]
    Event, name="EventWriteSchema", exclude_readonly=True,
)
