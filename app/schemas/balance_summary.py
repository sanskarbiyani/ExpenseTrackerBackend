from pydantic import BaseModel

class BalanceSummary(BaseModel):
    today_balance: float
    week_balance: float
    month_balance: float

    class Config:
        orm_mode = True