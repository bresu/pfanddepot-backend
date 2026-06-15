from pydantic import BaseModel

class StatsRead(BaseModel):
    total_items: int
    total_cents: int
    total_euros: float