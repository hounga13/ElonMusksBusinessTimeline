# Elon Musk's Business Timeline Cache

This repository stores cached data for the "Elon Musk's Business Timeline" web application.

## Directory Structure
- `data/`: Contains JSON files with cached content (e.g., `elon-musk.json`, `tesla.json`).
- `scripts/`: Python scripts for crawling data.
- `.github/workflows/`: GitHub Actions workflow for periodic updates.

## Setup
1. Clone the repository: `git clone <repository-url>`
2. Configure API tokens in `scripts/crawl.py` (e.g., Twitter API token).
3. Enable GitHub Actions in the repository settings.

## Usage
- The workflow `update-cache.yml` runs daily to update cached data.
- Manually trigger the workflow via the GitHub Actions tab if needed.
