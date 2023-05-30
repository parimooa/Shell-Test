import math

from scipy.stats import norm

from option_db import OptionDB
from schema import MarketDataCreate, PriceValue

OPTION_TYPES = ["call", "put"]


class MarketOptionData(OptionDB):
    """Base class for market option data"""

    def __init__(self, db):
        OptionDB.__init__(self, db)

    @property
    def market_data(self):
        return self._parsed_market_data

    @market_data.setter
    def market_data(self, value):
        if value:
            (
                symbol,
                expiry_date,
                call_type,
                strike,
                strike_price,
                currency,
            ) = value.split(" ")

            if call_type.lower() in OPTION_TYPES:
                self._parsed_market_data = MarketDataCreate(
                    symbol=symbol,
                    expiry_date=expiry_date,
                    option_type=call_type,
                    strike_price=strike_price,
                )
            else:
                raise ValueError(f"'{call_type}' is not valid option type")

    def calculate_pv(self, symbol: str) -> PriceValue:
        """
        Use black 76 formula to calculate pricing option
        :param symbol:
        :return:
        """
        result: MarketDataCreate = self.get_market_data(symbol)
        d1 = (
            math.log(result.spot_price / result.strike_price)
            + (0.5 * result.volatility**2 * result.time_to_expiry)
        ) / (result.volatility * math.sqrt(result.time_to_expiry))
        d2 = d1 - (result.volatility * math.sqrt(result.time_to_expiry))

        if result.option_type.lower() == "call":
            option_pv = math.exp(-result.risk_free_rate * result.time_to_expiry) * (
                result.spot_price
                * math.exp((0.5 * result.volatility**2) * result.time_to_expiry)
                * norm.cdf(d1)
                - result.strike_price * norm.cdf(d2)
            )
        elif result.option_type.lower() == "put":
            option_pv = math.exp(-result.risk_free_rate * result.time_to_expiry) * (
                result.strike_price * norm.cdf(-d2)
                - result.spot_price
                * math.exp((0.5 * result.volatility**2) * result.time_to_expiry)
                * norm.cdf(-d1)
            )
        else:
            raise ValueError(
                "Invalid option type. Please specify either 'call' or 'put'."
            )

        return PriceValue(
            symbol=result.symbol, price_value=option_pv, identifier=result.identifier
        )
