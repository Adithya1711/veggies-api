# Veggies API

A lightweight, memory-efficient FastAPI backend that serves the daily market data collected by the scraper module.

## Architecture

This API is completely decoupled from the scraping logic. It acts strictly as a data consumer. By reading from a structured file system (`data/DD-MM-YYYY/place.json`), it functions as a highly scalable read-only database without the overhead of maintaining an SQL server.

## Endpoints

### `GET /api/v1/{place}/today`

Returns the daily wholesale and retail vegetable prices for the specified region.

**Example Request:**

```bash
curl http://localhost:8000/api/v1/chennai/today
```

**Successful Response:**

```json
{
  "status": "success",
  "region": "chennai",
  "date": "23-08-2026",
  "data": [
    {
      "price": 35,
      "vegetale_name": "Onion Big (பெரிய வெங்காயம்)",
      "minRetail": 39,
      "maxRetail": 46
    }
  ]
}
```

## Running Locally

This project exclusively uses `uv` for dependency management and execution. For `uv` setup instructions, refer to the official documentation at [docs.astral.sh](https://docs.astral.sh/uv/).

To start the API in development mode with hot-reloading, navigate to the `veggies-api` directory and run the server using `uv`:

```bash
cd veggies-api
uv run uvicorn main:app --reload
```

Once the server is running, navigate to `[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)` in your browser to view the interactive Swagger documentation and test the endpoints directly.
