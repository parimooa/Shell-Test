from datetime import date, datetime
from typing import Optional
from uuid import UUID, uuid4

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, validator, UUID4, Field

option_expiry_months = {"hh": 1, "brn": 2}


class MarketData(BaseModel):
    strike_price: float
    expiry_date: str
    symbol: str
    option_type: str


class MarketDataCreate(MarketData):
    """
    Assumptions made for spot,risk_Rate and volatility
    """

    identifier: UUID = Field(default_factory=uuid4)
    spot_price: float = 70
    risk_free_rate: float = 0.05
    time_to_expiry: Optional[float]
    volatility: float = 0.02

    class Config:
        orm_mode = True

    @validator("time_to_expiry", pre=True, always=True)
    def calculate_time_to_expiry(cls, v, values):
        if "expiry_date" in values and "symbol" in values and not v:
            expiry_month_year = datetime.strptime(values["expiry_date"], "%b%y")
            expiry_month = expiry_month_year.month
            expiry_year = expiry_month_year.year
            try:
                relative_month = option_expiry_months[values["symbol"].lower()]
                expiration_date = date(expiry_year, expiry_month, 1) - relativedelta(
                    months=relative_month, days=1
                )
                while (
                    expiration_date.weekday() >= 5
                ):  # Adjust if the expiration date falls on a weekend
                    expiration_date -= relativedelta(days=1)
                    # Calculate the time to expiration in years
                expiration_time_years = (expiration_date - date.today()).days / 365.0
                return round(expiration_time_years, 2)
            except KeyError as e:
                raise ValueError(f"{values['symbol']} is not a valid symbol")

        else:
            raise ValueError("Either Option expiry date or symbol not provided")


class PriceValue(BaseModel):
    identifier: UUID4
    symbol: str
    price_value: float


class Payload(BaseModel):
    data: str
