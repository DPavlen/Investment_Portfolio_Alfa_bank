from datetime import datetime

from pydantic import BaseModel


class OperationCreate(BaseModel):
    """BaseModel импортируем из Pydantic.
    Это схема необходима для @router.post."""
    id: int
    quantity: str
    figi: str
    instrument_type: str
    date: datetime
    type: str