from uuid import uuid4

from sqlalchemy.orm import Session

import models


class OptionDB:
    """Base class for db operations"""

    def __init__(self, db):
        self.db: Session = db
        self._parsed_market_data = None

    def upload_market_data(self) -> str:
        """
        upload the market data in database
        generate unique uuid
        :return:
        """

        market_data = models.OptionData(
            identifier=self._parsed_market_data.identifier,
            spot_price=self._parsed_market_data.spot_price,
            risk_free_rate=self._parsed_market_data.risk_free_rate,
            time_to_expiry=self._parsed_market_data.time_to_expiry,
            volatility=self._parsed_market_data.volatility,
            expiry_date=self._parsed_market_data.expiry_date,
            option_type=self._parsed_market_data.option_type,
            symbol=self._parsed_market_data.symbol,
            strike_price=self._parsed_market_data.strike_price,
        )
        self.db.add(market_data)
        self.db.commit()
        self.db.refresh(market_data)
        return market_data.identifier

    def get_market_data(self, identifier: str):
        return (
            self.db.query(models.OptionData)
            .filter(models.OptionData.identifier == identifier)
            .first()
        )
