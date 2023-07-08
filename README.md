# service.markets
Software-as-a-Service (SaaS) Marketplace with cryptocurrency payments

Service.markets runs on [FastAPI](https://fastapi.tiangolo.com/) and uses [Aleph.im](https://aleph.im/) for decentralized hosting. 
## Initial setup
Install the FastAPI library and Uvicorn:
```shell
poetry install
```
Activate the virtual environment, if not already done:
```shell
poetry shell
```

## Run on local

### Running the API
Uvicorn is used to run ASGI compatible web applications, such as the `app`
web application from the example above. You need to specify it the name of the
Python module to use and the name of the app:
```shell
python -m uvicorn src.service_markets.api.main:app --reload
```

Then open the app in a web browser on http://localhost:8000

> Tip: With `--reload`, Uvicorn will automatically reload your code upon changes  

## Testing
To run the tests, you need to [install the dev dependencies](#installing-dev-dependencies).

In order to avoid indexing all the messages and starting out with an empty database, you need to set the `TEST_CHANNEL` environment variable to `true`:
```shell
export TEST_CHANNEL=true
```

Then, you can run the API tests with:
```shell
poetry run pytest src/service_markets/api/test.py
```

**Note**: The tests run sequentially and if one fails, the following ones will also fail due to the event loop being closed.

## Environment variables

| Name            | Description                                               | Type     | Default |
|-----------------|-----------------------------------------------------------|----------|---------|
| `TEST_CACHE`    | Whether to use the test cache                             | `bool`   | `true`  |
| `TEST_CHANNEL`  | Whether to use a fresh test channel                       | `bool`   | `false` |
| `ALEPH_CHANNEL` | The Aleph channel to use, is superseded by `TEST_CHANNEL` | `string` | `None`  |