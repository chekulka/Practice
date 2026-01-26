"""
Filtering and scoring system for AI/ML job listings.
"""

import re
from datetime import datetime, timedelta
from typing import List, Optional, Callable

from .models import Job, SearchResults, ExperienceLevel
from .config import JOB_CATEGORIES, STARTUP_INDICATORS, US_LOCATIONS, SearchConfig


class JobFilter:
    """Filter jobs based on various criteria."""

    def __init__(self, config: Optional[SearchConfig] = None):
        self.config = config or SearchConfig()

    def filter_jobs(self, jobs: List[Job]) -> List[Job]:
        """Apply all configured filters to job list."""
        filtered = jobs

        # Filter by categories
        if self.config.categories:
            filtered = self.filter_by_categories(filtered, self.config.categories)

        # Filter by location (US only)
        filtered = self.filter_by_us_location(filtered)

        # Filter remote only if specified
        if self.config.remote_only:
            filtered = [job for job in filtered if job.is_remote]

        # Filter startups only if specified
        if self.config.startup_only:
            filtered = [job for job in filtered if job.company.is_startup]

        # Filter by days old
        if self.config.days_old:
            filtered = self.filter_by_date(filtered, self.config.days_old)

        # Filter by minimum salary
        if self.config.min_salary:
            filtered = self.filter_by_salary(filtered, self.config.min_salary)

        # Limit results
        if self.config.max_results:
            filtered = filtered[:self.config.max_results]

        return filtered

    def filter_by_categories(self, jobs: List[Job], categories: List[str]) -> List[Job]:
        """Filter jobs that match specified AI/ML categories."""
        filtered = []

        for job in jobs:
            job_text = f"{job.title} {job.description}".lower()
            matched_categories = []

            for cat_key in categories:
                if cat_key not in JOB_CATEGORIES:
                    continue

                category = JOB_CATEGORIES[cat_key]

                # Check if job matches this category
                title_match = any(
                    pattern in job.title.lower()
                    for pattern in category.title_patterns
                )

                keyword_match = any(
                    keyword in job_text
                    for keyword in category.keywords
                )

                if title_match or keyword_match:
                    matched_categories.append(category.name)

            if matched_categories:
                job.categories = matched_categories
                filtered.append(job)

        return filtered

    def filter_by_us_location(self, jobs: List[Job]) -> List[Job]:
        """Filter jobs to US locations only."""
        filtered = []

        for job in jobs:
            location_lower = job.location.lower()

            # Check if location is in the US or remote
            is_us = any(us_loc in location_lower for us_loc in US_LOCATIONS)
            is_remote = job.is_remote or "remote" in location_lower

            if is_us or is_remote:
                filtered.append(job)

        return filtered

    def filter_by_date(self, jobs: List[Job], days: int) -> List[Job]:
        """Filter jobs posted within the last N days."""
        cutoff_date = datetime.now() - timedelta(days=days)
        return [
            job for job in jobs
            if job.posted_date is None or job.posted_date.replace(tzinfo=None) >= cutoff_date
        ]

    def filter_by_salary(self, jobs: List[Job], min_salary: int) -> List[Job]:
        """Filter jobs with salary above minimum."""
        filtered = []
        for job in jobs:
            if job.salary is None:
                # Include jobs without salary info
                filtered.append(job)
            elif job.salary.min_amount and job.salary.min_amount >= min_salary:
                filtered.append(job)
            elif job.salary.max_amount and job.salary.max_amount >= min_salary:
                filtered.append(job)
        return filtered

    def filter_by_experience(self, jobs: List[Job], levels: List[ExperienceLevel]) -> List[Job]:
        """Filter jobs by experience level."""
        return [
            job for job in jobs
            if job.experience_level in levels or job.experience_level == ExperienceLevel.UNKNOWN
        ]


class JobScorer:
    """Score jobs based on relevance and preferences."""

    def __init__(self, preferences: Optional[dict] = None):
        self.preferences = preferences or {}

        # Default scoring weights
        self.weights = {
            "title_match": 30,
            "category_match": 25,
            "startup_bonus": 15,
            "remote_bonus": 10,
            "salary_info": 10,
            "recent_posting": 10,
        }

    def score_jobs(self, jobs: List[Job], query: str) -> List[Job]:
        """Score all jobs and sort by relevance."""
        for job in jobs:
            job.relevance_score = self._calculate_score(job, query)

        return sorted(jobs, key=lambda j: j.relevance_score, reverse=True)

    def _calculate_score(self, job: Job, query: str) -> float:
        """Calculate relevance score for a job."""
        score = 0.0
        query_terms = query.lower().split()

        # Title match scoring
        title_lower = job.title.lower()
        title_matches = sum(1 for term in query_terms if term in title_lower)
        score += (title_matches / len(query_terms)) * self.weights["title_match"]

        # Category match scoring
        if job.categories:
            score += self.weights["category_match"]

        # Startup bonus
        if job.company.is_startup:
            score += self.weights["startup_bonus"]

        # Remote bonus (if preferred)
        if job.is_remote and self.preferences.get("prefer_remote", True):
            score += self.weights["remote_bonus"]

        # Salary info bonus
        if job.salary:
            score += self.weights["salary_info"]

        # Recent posting bonus
        if job.posted_date:
            days_old = (datetime.now() - job.posted_date.replace(tzinfo=None)).days
            if days_old <= 7:
                score += self.weights["recent_posting"]
            elif days_old <= 14:
                score += self.weights["recent_posting"] * 0.5

        # Preferred skills match
        preferred_skills = self.preferences.get("skills", [])
        if preferred_skills:
            description_lower = job.description.lower()
            skill_matches = sum(
                1 for skill in preferred_skills
                if skill.lower() in description_lower
            )
            if preferred_skills:
                score += (skill_matches / len(preferred_skills)) * 15

        return round(score, 2)


class JobSearchEngine:
    """Main search engine combining aggregation, filtering, and scoring."""

    def __init__(self, config: Optional[SearchConfig] = None, preferences: Optional[dict] = None):
        self.filter = JobFilter(config)
        self.scorer = JobScorer(preferences)

    def search(self, jobs: List[Job], query: str) -> SearchResults:
        """Search, filter, and score jobs."""
        # Filter jobs
        filtered_jobs = self.filter.filter_jobs(jobs)

        # Score and sort jobs
        scored_jobs = self.scorer.score_jobs(filtered_jobs, query)

        return SearchResults(
            jobs=scored_jobs,
            total_count=len(scored_jobs),
            query=query,
            categories=self.filter.config.categories
        )


def detect_startup(company_name: str, description: str, tags: List[str] = None) -> bool:
    """
    Detect if a company is likely a startup based on various signals.
    """
    text = f"{company_name} {description} {' '.join(tags or [])}".lower()

    # Check for startup indicators
    if any(indicator in text for indicator in STARTUP_INDICATORS):
        return True

    # Check for small company signals
    small_company_signals = [
        "small team", "growing team", "join our team",
        "founding", "co-founder", "employee #", "early employee"
    ]
    if any(signal in text for signal in small_company_signals):
        return True

    # Check for NOT startup signals (large companies)
    large_company_signals = [
        "fortune 500", "fortune500", "global leader",
        "100,000+ employees", "established in 19"
    ]
    if any(signal in text for signal in large_company_signals):
        return False

    return False
