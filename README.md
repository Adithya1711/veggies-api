# Veggies API

A zero-maintenance data pipeline and REST API that tracks daily local vegetable market prices (Chennai).

This project bridges the gap between fragile public municipal websites and production-ready software by leveraging Bright Data to extract data and an AI-powered GitHub Actions pipeline to automatically heal the scraper when the target website's UI changes.

## The Problem It Solves

Vital local market data is trapped in municipal websites lacking official APIs. Traditional scrapers break whenever these sites update their UI, causing downstream applications to crash. This project solves that by creating a self-repairing bridge that requires zero manual human intervention.

## Who is it For?

- **Software Developers:** Provides a structured, resilient REST API to build market-tracking applications without worrying about broken data pipelines.
- **Local Food Businesses:** Serves the caterers, restaurants, and cloud kitchens who rely on downstream applications to monitor volatile ingredient costs and protect profit margins.

## Repository Structure

This repository is split into two completely decoupled microservices:

- `/scraper` (The Producer): A Python script that triggers a Bright Data extraction job, polls for the result, and saves the cleaned JSON array.
- `/veggies-api` (The Consumer): A lightweight FastAPI server that reads the local JSON files and serves them via RESTful endpoints.
- `.github/workflows/scraper.yml`: The CI/CD pipeline that automates the daily run, validates the data, and triggers the AI self-healing mechanism if the target layout changes.

## The Self-Healing CI/CD Loop

This project runs entirely autonomously via GitHub Actions:

1. **Cron Job:** Runs daily at 5:00 AM UTC.
2. **Validate:** Checks if the extracted JSON array is empty or missing fields (indicating a broken website layout).
3. **Heal:** If broken, it triggers the Bright Data CLI to let the AI dynamically patch the CSS selectors.
4. **Commit:** Pushes the fresh `chennai.json` file straight to the repository, automatically updating the data source for the live API.

## Running Locally

### Prerequisites

This project exclusively uses `uv` for dependency management and execution. For `uv` installation instructions, please refer to the official documentation at [docs.astral.sh](https://docs.astral.sh/uv/getting-started/installation/).

Create a `.env` file in the root directory:

```env
BRIGHT_DATA_API_TOKEN=your_token_here
COLLECTOR_ID=c_your_collector_id
```

### Execution

Run the modules directly from the root directory using `uv`.

**1. Run the Scraper**

```bash
uv run scraper/main.py
```

**2. Start the API Server**

```bash
cd veggies-api
uv run uvicorn main:app --reload
```

The API will be available at [http://127.0.0.1:8000](http://127.0.0.1:8000). Navigate to [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to view the interactive Swagger documentation and test the endpoints.
