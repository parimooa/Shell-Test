import json
from uuid import uuid4

import pytest

from main import option

uid = str(uuid4())


@pytest.mark.parametrize(
    "input,expected,expected_status_code",
    [
        (
            "BRN Jan24 Call Strike 100 USD/BBL",
            {"identifier": "some-uuid", "message": "Market data uploaded successfully"},
            201,
        ),
        ("", {"detail": "Empty payload"}, 400),
        (
            "BRN Call Strike 100 USD/BBL",
            {
                "detail": "Error in parsing market data 'not enough values to unpack "
                "(expected 6, got 5)'"
            },
            500,
        ),
    ],
    ids=["correct-payload", "empty-payload", "wrong-payload"],
)
def test_upload_data(test_app, monkeypatch, input, expected, expected_status_code):
    monkeypatch.setattr(option, "upload_market_data", lambda: "some-uuid")
    payload = {"data": input}
    response = test_app.post("/market_data", content=json.dumps(payload))
    assert response.json() == expected
    assert response.status_code == expected_status_code


@pytest.mark.parametrize(
    "uid,expected",
    [(uid, {"identifier": uid, "symbol": "RNM", "price_value": 4.5})],
    ids=["correct-id"],
)
def test_calculate_price_value(test_app, monkeypatch, uid, expected):
    monkeypatch.setattr(option, "calculate_pv", lambda uid: expected)
    response = test_app.get(f"/calculate_pv/{uid}")
    assert response.json() == expected


@pytest.mark.parametrize(
    "uid,mock_return,expected",
    [
        (
            123,
            None,
            {"detail": "Given'123' is an invalid identifier"},
        ),
        (
            123,
            {
                "spot_price": 70,
                "risk_free_rate": 0.05,
                "volatility": 0.02,
                "symbol": "BRN",
                "strike_price": 100,
                "identifier": "4c27880c-5018-4e7a-a297-e80741f425c4",
                "time_to_expiry": 0.43,
                "expiry_date": "Jan24",
                "option_type": "Call",
            },
            {
                "spot_price": 70,
                "risk_free_rate": 0.05,
                "volatility": 0.02,
                "symbol": "BRN",
                "strike_price": 100,
                "identifier": "4c27880c-5018-4e7a-a297-e80741f425c4",
                "time_to_expiry": 0.43,
                "expiry_date": "Jan24",
                "option_type": "Call",
            },
        ),
    ],
    ids=["invalid-id", "correct-id"],
)
def test_retrieve_market_data(test_app, monkeypatch, uid, mock_return, expected):
    monkeypatch.setattr(option, "get_market_data", lambda uid: expected)
    response = test_app.get(f"/market_data/123")
    assert response.json() == expected
