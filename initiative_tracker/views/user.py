from uuid import uuid4
from fastapi import APIRouter
from pydantic import BaseModel

from initiative_tracker.models.character import (
    Character,
    CharacterClass,
    CharacterClassFeature,
    CharacterClassFeatureType,
)
from initiative_tracker.models.user import User

user_router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@user_router.get("/me")
async def get_self() -> User:
    return User(id=uuid4(), username="mercer", email="matthew@merc.er")


class CharacterResponse(BaseModel):
    characters: list[Character]


@user_router.get("/me/characters")
async def get_characters() -> CharacterResponse:
    return CharacterResponse(
        characters=[
            Character(
                id=uuid4(),
                name="Percival",
                classes=[
                    CharacterClass(
                        id=uuid4(),
                        name="Gunslinger",
                        description="A fighter that uses guns",
                        owner=uuid4(),
                        features=[
                            CharacterClassFeature(
                                id=uuid4(),
                                name="Firearm Proficiency",
                                description="You gain proficiency with firearms",
                                level=1,
                                optional=False,
                                type_=CharacterClassFeatureType.NO_CHOICE,
                                choices=[],
                            ),
                        ],
                    ),
                ],
                owner=uuid4(),
            ),
            Character(
                id=uuid4(),
                name="Keyleth",
                classes=[
                    CharacterClass(
                        id=uuid4(),
                        name="Druid",
                        description="A spellcaster that uses nature magic",
                        owner=uuid4(),
                        features=[
                            CharacterClassFeature(
                                id=uuid4(),
                                name="Wild Shape",
                                description="You can transform into animals",
                                level=2,
                                optional=False,
                                type_=CharacterClassFeatureType.NO_CHOICE,
                                choices=[],
                            ),
                        ],
                    ),
                ],
                owner=uuid4(),
            ),
            Character(
                id=uuid4(),
                name="Grog",
                classes=[
                    CharacterClass(
                        id=uuid4(),
                        name="Barbarian",
                        description="A fighter that uses rage",
                        owner=uuid4(),
                        features=[
                            CharacterClassFeature(
                                id=uuid4(),
                                name="Rage",
                                description="You can enter a rage",
                                level=1,
                                optional=False,
                                type_=CharacterClassFeatureType.NO_CHOICE,
                                choices=[],
                            ),
                        ],
                    ),
                ],
                owner=uuid4(),
            ),
        ]
    )
