from pydantic import BaseModel, condecimal, field_validator
from enum import Enum
from datetime import datetime

class EventStatus(str, Enum):
    uncompleted = "незавершённое"
    team1_won = "завершено выигрышем первой команды"
    team2_won = "завершено выигрышем второй команды"

class EventCreate(BaseModel):
    name: str
    odds: condecimal(gt=0, max_digits=5, decimal_places=2)
    deadline: datetime

    @field_validator('deadline', mode='before')
    @classmethod
    def parse_deadline(cls, value):
        if isinstance(value, str):
            return datetime.strptime(value, '%Y-%m-%d %H:%M')
        return value

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Example Event",
                "odds": 1.25,
                "deadline": "2024-07-25 08:10"
            }
        }

class EventUpdate(BaseModel):
    status: EventStatus

class EventResponse(BaseModel):
    id: int
    name: str
    odds: condecimal(max_digits=5, decimal_places=2)
    deadline: datetime
    status: EventStatus

    @field_validator('deadline', mode='before')
    @classmethod
    def format_deadline(cls, value):
        if isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M')
        return value

    class Config:
        use_enum_values = True
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Example Event",
                "odds": 1.25,
                "deadline": "2024-07-25 08:10",
                "status": "незавершённое"
            }
        }
