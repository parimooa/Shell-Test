import sqlalchemy.exc
from fastapi import FastAPI, HTTPException, status
from pydantic.error_wrappers import ValidationError
from sqlalchemy.orm import Session

import models

import schema
from db import SessionLocal, engine
from market_data import MarketOptionData

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

db_session: Session = SessionLocal()
option = MarketOptionData(db_session)


@app.post(
    "/market_data",
    status_code=status.HTTP_201_CREATED,
)
async def market_data(m_data: schema.Payload):
    """
    Upload the market data to data store,
    validate the payload and send error if validation fails
    :param m_data: json data e.g. {"data":"BRN Jan24 Call Strike 100 USD/BBL"}
    :return:
    """
    try:
        option.market_data = m_data.data
        if m_data.data:
            identifier = option.upload_market_data()
        else:
            raise HTTPException(status_code=400, detail="Empty payload")
        if identifier:
            return {
                "identifier": identifier,
                "message": f"Market data uploaded successfully",
            }
        else:
            raise HTTPException(
                status_code=400, detail="Market data failed to upload !!"
            )

    except sqlalchemy.exc.IntegrityError as e:
        raise HTTPException(status_code=400, detail="Market Data already exists !!")
    except (AttributeError, ValidationError, ValueError) as e:
        raise HTTPException(
            status_code=500, detail=f"Error in parsing market data '{str(e)}'"
        )


@app.get("/market_data/{identifier}")
async def get_data(identifier: str):
    """
    Get market data for previously inserted identifier
    If identifier is not in data store, send invalid identifier message
    :param identifier: unique identifier (UUID)
    :return:
    """
    try:
        result = option.get_market_data(identifier)
        if result:
            return result
        else:
            raise HTTPException(
                status_code=404, detail=f"Given'{identifier}' is an invalid identifier"
            )
    except sqlalchemy.exc.DataError as e:
        raise HTTPException(
            status_code=404, detail=f"Given'{identifier}' is an invalid identifier"
        )


@app.get("/calculate_pv/{identifier}", response_model=schema.PriceValue)
async def calculate_price_value(identifier: str):
    """
    Get price value of previously uploaded market data,
    Return error for non existing identifier
    :param identifier:
    :return:
    """
    try:
        result = option.calculate_pv(identifier)
        if result:
            return result
        else:
            raise HTTPException(
                status_code=404, detail=f"{identifier} market data not found"
            )
    except sqlalchemy.exc.DataError as e:
        raise HTTPException(
            status_code=404, detail=f"Given'{identifier}' is an invalid identifier"
        )
