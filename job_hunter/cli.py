"""
Command-line interface for the AI/ML Job Hunter.
"""

import argparse
import json
import os
from datetime import datetime
from typing import List, Optional

from .models import Job, SearchResults
from .config import JOB_CATEGORIES, SearchConfig, APIConfig
from .job_sources import JobAggregator
from .filters import JobSearchEngine


class JobHunterCLI:
    """Command-line interface for job hunting."""

    def __init__(self):
        self.api_config = self._load_api_config()
        self.aggregator = JobAggregator(self.api_config)

    def _load_api_config(self) -> APIConfig:
        """Load API configuration from environment variables."""
        return APIConfig(
            adzuna_app_id=os.environ.get("ADZUNA_APP_ID"),
            adzuna_api_key=os.environ.get("ADZUNA_API_KEY"),
            muse_api_key=os.environ.get("MUSE_API_KEY"),
        )

    def run(self, args: argparse.Namespace):
        """Run the job search based on CLI arguments."""
        print("\n" + "=" * 60)
        print("   AI/ML Job Hunter - Startup Jobs in the US")
        print("=" * 60)

        # Build search configuration
        search_config = SearchConfig(
            categories=args.categories if args.categories else list(JOB_CATEGORIES.keys()),
            remote_only=args.remote,
            startup_only=not args.include_all,
            days_old=args.days,
            min_salary=args.min_salary,
            max_results=args.limit,
        )

        preferences = {
            "prefer_remote": args.remote,
            "skills": args.skills.split(",") if args.skills else [],
        }

        # Build search query
        query = self._build_query(args)
        print(f"\nSearching for: {query}")
        print(f"Categories: {', '.join(search_config.categories)}")
        print(f"Filters: Remote only={args.remote}, Startups only={not args.include_all}")
        print("-" * 60)

        # Fetch jobs from all sources
        all_jobs = self.aggregator.search_all(query, location="us")
        print(f"\nTotal jobs fetched: {len(all_jobs)}")

        # Apply filtering and scoring
        search_engine = JobSearchEngine(search_config, preferences)
        results = search_engine.search(all_jobs, query)

        print(f"Jobs after filtering: {results.total_count}")
        print("-" * 60)

        # Display results
        if args.output == "json":
            self._output_json(results, args.output_file)
        else:
            self._output_text(results, args.verbose)

        # Save results if requested
        if args.save:
            self._save_results(results, args.save)

    def _build_query(self, args: argparse.Namespace) -> str:
        """Build search query from arguments."""
        if args.query:
            return args.query

        # Build query from categories
        queries = []
        for cat_key in args.categories or list(JOB_CATEGORIES.keys()):
            if cat_key in JOB_CATEGORIES:
                queries.extend(JOB_CATEGORIES[cat_key].keywords[:2])

        return " OR ".join(set(queries[:5]))  # Limit query length

    def _output_text(self, results: SearchResults, verbose: bool = False):
        """Output results as formatted text."""
        if not results.jobs:
            print("\nNo jobs found matching your criteria.")
            return

        print(f"\n Found {results.total_count} matching jobs:\n")

        for i, job in enumerate(results.jobs, 1):
            print(f"\n[{i}] {job.title}")
            print(f"    Company: {job.company.name}", end="")
            if job.company.is_startup:
                print(" [STARTUP]", end="")
            print()
            print(f"    Location: {job.location}", end="")
            if job.is_remote:
                print(" [REMOTE]", end="")
            print()

            if job.salary:
                print(f"    Salary: {job.salary}")

            if job.categories:
                print(f"    Categories: {', '.join(job.categories)}")

            print(f"    Score: {job.relevance_score}")
            print(f"    URL: {job.url}")

            if verbose and job.posted_date:
                print(f"    Posted: {job.posted_date.strftime('%Y-%m-%d')}")

            if verbose and job.description:
                # Show truncated description
                desc = job.description[:200].replace("\n", " ")
                print(f"    Description: {desc}...")

        print("\n" + "=" * 60)
        print(f"Total: {results.total_count} jobs found")

    def _output_json(self, results: SearchResults, output_file: Optional[str] = None):
        """Output results as JSON."""
        data = {
            "query": results.query,
            "total_count": results.total_count,
            "categories": results.categories,
            "fetched_at": results.fetched_at.isoformat(),
            "jobs": [job.to_dict() for job in results.jobs]
        }

        json_output = json.dumps(data, indent=2, default=str)

        if output_file:
            with open(output_file, "w") as f:
                f.write(json_output)
            print(f"Results saved to {output_file}")
        else:
            print(json_output)

    def _save_results(self, results: SearchResults, filename: str):
        """Save results to a file."""
        data = {
            "query": results.query,
            "total_count": results.total_count,
            "categories": results.categories,
            "fetched_at": results.fetched_at.isoformat(),
            "jobs": [job.to_dict() for job in results.jobs]
        }

        with open(filename, "w") as f:
            json.dump(data, f, indent=2, default=str)

        print(f"\nResults saved to {filename}")


def create_parser() -> argparse.ArgumentParser:
    """Create the argument parser."""
    parser = argparse.ArgumentParser(
        prog="job_hunter",
        description="AI/ML Job Hunter - Find startup jobs in AI/ML fields across the US",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python -m job_hunter                           # Search all AI/ML categories
  python -m job_hunter -c data_science           # Search only data science roles
  python -m job_hunter -c ab_experimentation -r  # A/B testing, remote only
  python -m job_hunter -q "machine learning"     # Custom search query
  python -m job_hunter --min-salary 120000       # Filter by minimum salary
  python -m job_hunter -o json --save jobs.json  # Save results as JSON

Categories:
  - data_analytics     : Data Analyst, Analytics Engineer, BI roles
  - ab_experimentation : A/B Testing, Experimentation, Growth roles
  - causal_inference   : Causal Inference, Econometrics, Applied Scientist
  - data_science       : Data Scientist, ML Engineer, AI roles
  - product_management : AI/ML Product Manager roles
        """
    )

    parser.add_argument(
        "-q", "--query",
        type=str,
        help="Custom search query (overrides categories)"
    )

    parser.add_argument(
        "-c", "--categories",
        nargs="+",
        choices=list(JOB_CATEGORIES.keys()),
        help="Job categories to search (default: all)"
    )

    parser.add_argument(
        "-r", "--remote",
        action="store_true",
        help="Show only remote positions"
    )

    parser.add_argument(
        "--include-all",
        action="store_true",
        help="Include non-startup companies"
    )

    parser.add_argument(
        "-d", "--days",
        type=int,
        default=30,
        help="Only show jobs posted within N days (default: 30)"
    )

    parser.add_argument(
        "--min-salary",
        type=int,
        help="Minimum salary filter"
    )

    parser.add_argument(
        "-l", "--limit",
        type=int,
        default=50,
        help="Maximum number of results (default: 50)"
    )

    parser.add_argument(
        "-s", "--skills",
        type=str,
        help="Comma-separated preferred skills for scoring"
    )

    parser.add_argument(
        "-o", "--output",
        choices=["text", "json"],
        default="text",
        help="Output format (default: text)"
    )

    parser.add_argument(
        "--output-file",
        type=str,
        help="Output file for JSON format"
    )

    parser.add_argument(
        "--save",
        type=str,
        help="Save results to JSON file"
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show detailed job information"
    )

    return parser


def main():
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()

    cli = JobHunterCLI()
    cli.run(args)


if __name__ == "__main__":
    main()
