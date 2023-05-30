from sqlalchemy import Column, Float, String, UUID

from db import Base


class OptionData(Base):
    __tablename__ = "option_data"
    identifier = Column(
        UUID(as_uuid=True),
        primary_key=True,
    )
    spot_price = Column(Float)
    risk_free_rate = Column(Float)
    time_to_expiry = Column(Float)
    volatility = Column(Float)
    expiry_date = Column(String)
    symbol = Column(String)
    option_type = Column(String)
    strike_price = Column(Float)
