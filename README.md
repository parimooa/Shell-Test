# Shell-Test

## Database

#### Start Postgres Database and pgadmin (Docker)

`make compose-up`

#### Stop Postgres Database and pgadmin (Docker)

`make compose-down`

## Development

#### Format code 

`make format`

#### Run test 

`make test`

#### Start app 

`make start-app`

##### API docs

`http://localhost:8000/docs`

## API routes

##### To upload market data

`/market_data`. 

##### To Retrieve market data

`/market_data/{identifier}`

##### To Retrieve price value for previous market data

`/calculate_pv/{identifier}`
