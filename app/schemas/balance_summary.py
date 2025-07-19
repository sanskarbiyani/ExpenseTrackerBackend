from pydantic import BaseModel

class BalanceSummary(BaseModel):
    today_balance: float
    week_balance: float
    month_balance: float

    model_config = {
        "from_attributes": True,
    }