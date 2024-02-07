from enum import StrEnum
from uuid import UUID
from pydantic import BaseModel


class CharacterClassFeatureChoice(BaseModel):
    id: UUID
    name: str
    description: str


class CharacterClassFeatureType(StrEnum):
    NO_CHOICE = "no_choice"
    SINGULAR_CHOICE = "choice"
    MULTIPLE_CHOICE = "choices"


class CharacterClassFeature(BaseModel):
    id: UUID
    name: str
    description: str
    level: int = 1
    optional: bool = False
    type_: CharacterClassFeatureType
    choices: list[CharacterClassFeatureChoice]


class CharacterClass(BaseModel):
    id: UUID
    name: str
    description: str
    owner: UUID
    features: list[CharacterClassFeature]


class CharacterClassRecord(BaseModel):
    class_id: UUID
    level: int = 1


class Character(BaseModel):
    id: UUID
    name: str
    classes: list[CharacterClass]
    owner: UUID
