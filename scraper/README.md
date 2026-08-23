# Data Extraction Module

This module acts as the data producer. It is responsible for triggering the Bright Data extraction job, polling for completion, and securely routing the structured data into the API module's storage directory.

## Core Flow

Rather than forcing a persistent connection, this script uses an asynchronous polling mechanism to remain highly time-efficient:

1. **Trigger:** Sends a POST request to the Bright Data API to start the data collection process for the target URL.
2. **Poll:** Polls the dataset endpoint at regular intervals until a `200 OK` is returned, indicating the job is complete.
3. **Route:** Automatically calculates the current date and dynamically saves the extracted JSON array into the API's file structure (`../veggies-api/data/DD-MM-YYYY/chennai.json`).

## Environment Setup

The script requires access to your Bright Data credentials. Ensure a `.env` file exists in the **root directory** of the project with the following keys:

```env
BRIGHT_DATA_API_TOKEN=your_token_here
COLLECTOR_ID=c_your_collector_id
```

## Execution

This project exclusively uses `uv` as the package manager and test runner. For setup and usage instructions regarding `uv`, refer to [docs.astral.sh](https://docs.astral.sh/uv/).

**Important Pathing Note:** You must execute this script from the main project root, not from inside the `scraper/` directory. This ensures the relative pathing correctly deposits the generated JSON file into the `veggies-api` folder.

```bash
uv run scraper/main.py
```
