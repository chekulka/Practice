# AI/ML Job Hunter

A job hunting application for finding AI/ML startup jobs in the US.

## Features

- Search multiple job boards (Remotive, The Muse, Adzuna)
- Filter by AI/ML job categories:
  - **Data Analytics**: Data Analyst, Analytics Engineer, BI roles
  - **A/B Experimentation**: A/B Testing, Growth, Experimentation roles
  - **Causal Inference**: Econometrics, Applied Scientist roles
  - **Data Science**: Data Scientist, ML Engineer, AI Engineer roles
  - **Product Management**: AI/ML Product Manager roles
- Focus on startup companies
- Remote job filtering
- Salary filtering
- Relevance scoring

## Quick Start

```bash
# Interactive mode
python main.py

# Quick search
python main.py --search "data scientist"

# CLI mode with options
python -m job_hunter --help
```

## CLI Examples

```bash
# Search all AI/ML categories
python -m job_hunter

# Search specific categories
python -m job_hunter -c data_science ab_experimentation

# Remote only, startups
python -m job_hunter -c data_analytics -r

# With salary filter
python -m job_hunter --min-salary 150000

# Save results to JSON
python -m job_hunter -o json --save jobs.json
```

## Configuration

Set environment variables for additional job sources:

```bash
export ADZUNA_APP_ID="your_app_id"
export ADZUNA_API_KEY="your_api_key"
```

## Job Categories

| Category | Roles |
|----------|-------|
| `data_analytics` | Data Analyst, Analytics Engineer, BI Analyst |
| `ab_experimentation` | A/B Testing, Experimentation, Growth Analyst |
| `causal_inference` | Causal Inference, Econometrics, Applied Scientist |
| `data_science` | Data Scientist, ML Engineer, AI Engineer |
| `product_management` | AI/ML Product Manager, Data PM |

## Project Structure

```
job_hunter/
├── __init__.py      # Package initialization
├── __main__.py      # Module entry point
├── config.py        # Configuration and job categories
├── models.py        # Data models (Job, Company, Salary)
├── job_sources.py   # Job board API integrations
├── filters.py       # Filtering and scoring logic
└── cli.py           # Command-line interface
main.py              # Main entry point
```

## Requirements

- Python 3.7+
- No external dependencies (uses standard library only)
