#!/usr/bin/env python3
"""
AI/ML Job Hunter - Main Entry Point

A job hunting application for finding AI/ML startup jobs in the US.

Supported job categories:
- Data Analytics
- A/B Experimentation
- Causal Inference
- Data Science
- AI/ML Product Management

Usage:
    python main.py                              # Interactive mode
    python main.py --search "data scientist"    # Quick search
    python -m job_hunter                        # CLI mode

For CLI options, run: python -m job_hunter --help
"""

import sys
import os

# Add the project root to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from job_hunter.config import JOB_CATEGORIES, SearchConfig, APIConfig
from job_hunter.job_sources import JobAggregator
from job_hunter.filters import JobSearchEngine
from job_hunter.models import SearchResults


def print_banner():
    """Print the application banner."""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║          AI/ML Job Hunter - Startup Edition              ║
    ║     Find your next AI/ML role at innovative startups     ║
    ╚══════════════════════════════════════════════════════════╝
    """)


def print_categories():
    """Print available job categories."""
    print("\nAvailable Job Categories:")
    print("-" * 40)
    for key, category in JOB_CATEGORIES.items():
        print(f"  [{key}]")
        print(f"    {category.name}")
        print(f"    Keywords: {', '.join(category.keywords[:3])}...")
    print()


def get_user_selection() -> list:
    """Get category selection from user."""
    print("\nSelect categories (comma-separated numbers, or 'all'):")
    categories = list(JOB_CATEGORIES.keys())
    for i, key in enumerate(categories, 1):
        print(f"  {i}. {JOB_CATEGORIES[key].name}")

    selection = input("\nYour selection: ").strip().lower()

    if selection == "all" or selection == "":
        return categories

    try:
        indices = [int(x.strip()) - 1 for x in selection.split(",")]
        return [categories[i] for i in indices if 0 <= i < len(categories)]
    except (ValueError, IndexError):
        print("Invalid selection. Using all categories.")
        return categories


def get_search_preferences() -> dict:
    """Get search preferences from user."""
    print("\nSearch Preferences:")

    remote_only = input("  Remote only? (y/n) [n]: ").strip().lower() == "y"
    startup_only = input("  Startups only? (y/n) [y]: ").strip().lower() != "n"

    min_salary = input("  Minimum salary (press Enter to skip): ").strip()
    min_salary = int(min_salary) if min_salary.isdigit() else None

    return {
        "remote_only": remote_only,
        "startup_only": startup_only,
        "min_salary": min_salary,
    }


def display_results(results: SearchResults):
    """Display search results."""
    if not results.jobs:
        print("\n No jobs found matching your criteria.")
        print("  Try adjusting your filters or searching different categories.")
        return

    print(f"\n Found {results.total_count} matching jobs:\n")
    print("=" * 70)

    for i, job in enumerate(results.jobs[:20], 1):  # Show top 20
        print(f"\n[{i}] {job.title}")
        print(f"    Company: {job.company.name}", end="")
        if job.company.is_startup:
            print(" ⭐ STARTUP", end="")
        print()

        print(f"    Location: {job.location}", end="")
        if job.is_remote:
            print(" 🏠 REMOTE", end="")
        print()

        if job.salary:
            print(f"    💰 Salary: {job.salary}")

        if job.categories:
            print(f"    📂 Categories: {', '.join(job.categories)}")

        print(f"    🔗 Apply: {job.url}")
        print(f"    📊 Relevance Score: {job.relevance_score}")

    if results.total_count > 20:
        print(f"\n... and {results.total_count - 20} more jobs.")
        print("Use CLI mode for full results: python -m job_hunter --help")

    print("\n" + "=" * 70)


def interactive_mode():
    """Run in interactive mode."""
    print_banner()
    print_categories()

    # Get user selections
    selected_categories = get_user_selection()
    preferences = get_search_preferences()

    # Build configuration
    api_config = APIConfig(
        adzuna_app_id=os.environ.get("ADZUNA_APP_ID"),
        adzuna_api_key=os.environ.get("ADZUNA_API_KEY"),
    )

    search_config = SearchConfig(
        categories=selected_categories,
        remote_only=preferences["remote_only"],
        startup_only=preferences["startup_only"],
        min_salary=preferences["min_salary"],
    )

    # Build search query from categories
    keywords = []
    for cat_key in selected_categories:
        if cat_key in JOB_CATEGORIES:
            keywords.extend(JOB_CATEGORIES[cat_key].keywords[:2])
    query = " ".join(set(keywords[:5]))

    print(f"\n🔍 Searching for: {query}")
    print("-" * 50)

    # Search jobs
    aggregator = JobAggregator(api_config)
    all_jobs = aggregator.search_all(query, location="us")

    print(f"\n📥 Fetched {len(all_jobs)} jobs from all sources")

    # Filter and score
    search_engine = JobSearchEngine(search_config, {"prefer_remote": preferences["remote_only"]})
    results = search_engine.search(all_jobs, query)

    # Display results
    display_results(results)

    # Offer to save
    save = input("\nSave results to file? (y/n) [n]: ").strip().lower()
    if save == "y":
        filename = input("Filename [jobs.json]: ").strip() or "jobs.json"
        import json
        with open(filename, "w") as f:
            json.dump({
                "query": results.query,
                "total_count": results.total_count,
                "jobs": [job.to_dict() for job in results.jobs]
            }, f, indent=2, default=str)
        print(f"✅ Results saved to {filename}")


def quick_search(query: str):
    """Run a quick search with default settings."""
    print_banner()
    print(f"🔍 Quick search: {query}\n")

    api_config = APIConfig(
        adzuna_app_id=os.environ.get("ADZUNA_APP_ID"),
        adzuna_api_key=os.environ.get("ADZUNA_API_KEY"),
    )

    search_config = SearchConfig(
        categories=list(JOB_CATEGORIES.keys()),
        startup_only=True,
    )

    aggregator = JobAggregator(api_config)
    all_jobs = aggregator.search_all(query, location="us")

    search_engine = JobSearchEngine(search_config)
    results = search_engine.search(all_jobs, query)

    display_results(results)


def main():
    """Main entry point."""
    if len(sys.argv) > 1:
        if sys.argv[1] == "--help" or sys.argv[1] == "-h":
            print(__doc__)
            print("\nFor CLI mode with more options: python -m job_hunter --help")
            sys.exit(0)
        elif sys.argv[1] == "--search" and len(sys.argv) > 2:
            quick_search(" ".join(sys.argv[2:]))
        else:
            # Pass to CLI
            from job_hunter.cli import main as cli_main
            cli_main()
    else:
        interactive_mode()


if __name__ == "__main__":
    main()
