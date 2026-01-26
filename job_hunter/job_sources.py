"""
Job source integrations for fetching jobs from various APIs.
"""

import hashlib
import json
import os
import urllib.request
import urllib.parse
import urllib.error
from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional, Dict, Any

from .models import Job, Company, Salary, JobSource, ExperienceLevel, JobType
from .config import APIConfig, STARTUP_INDICATORS, US_LOCATIONS


class JobSourceBase(ABC):
    """Base class for job sources."""

    def __init__(self, config: APIConfig):
        self.config = config

    @abstractmethod
    def search(self, query: str, location: str = "us", **kwargs) -> List[Job]:
        """Search for jobs matching the query."""
        pass

    @abstractmethod
    def get_source_name(self) -> str:
        """Get the name of this job source."""
        pass

    def _make_request(self, url: str, headers: Optional[Dict] = None) -> Optional[Dict]:
        """Make an HTTP GET request and return JSON response."""
        try:
            req = urllib.request.Request(url)
            if headers:
                for key, value in headers.items():
                    req.add_header(key, value)

            with urllib.request.urlopen(req, timeout=self.config.request_timeout) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.URLError as e:
            print(f"Error fetching from {self.get_source_name()}: {e}")
            return None
        except json.JSONDecodeError as e:
            print(f"Error parsing response from {self.get_source_name()}: {e}")
            return None

    def _is_startup(self, company_name: str, description: str = "", tags: List[str] = None) -> bool:
        """Check if a company appears to be a startup."""
        text = f"{company_name} {description} {' '.join(tags or [])}".lower()
        return any(indicator in text for indicator in STARTUP_INDICATORS)

    def _is_us_location(self, location: str) -> bool:
        """Check if location is in the US."""
        location_lower = location.lower()
        return any(us_loc in location_lower for us_loc in US_LOCATIONS)

    def _generate_job_id(self, source: str, identifier: str) -> str:
        """Generate a unique job ID."""
        return hashlib.md5(f"{source}:{identifier}".encode()).hexdigest()[:12]


class AdzunaSource(JobSourceBase):
    """Adzuna job board integration."""

    BASE_URL = "https://api.adzuna.com/v1/api/jobs"

    def get_source_name(self) -> str:
        return "Adzuna"

    def search(self, query: str, location: str = "us", **kwargs) -> List[Job]:
        """Search Adzuna for jobs."""
        if not self.config.adzuna_app_id or not self.config.adzuna_api_key:
            print("Adzuna API credentials not configured. Skipping Adzuna search.")
            return []

        jobs = []
        page = 1
        max_pages = kwargs.get("max_pages", 2)

        while page <= max_pages:
            params = {
                "app_id": self.config.adzuna_app_id,
                "app_key": self.config.adzuna_api_key,
                "results_per_page": self.config.results_per_page,
                "what": query,
                "where": kwargs.get("city", ""),
                "page": page,
                "sort_by": "date",
            }

            url = f"{self.BASE_URL}/{location}/search/{page}?{urllib.parse.urlencode(params)}"
            response = self._make_request(url)

            if not response or "results" not in response:
                break

            for item in response["results"]:
                job = self._parse_job(item)
                if job:
                    jobs.append(job)

            if len(response["results"]) < self.config.results_per_page:
                break

            page += 1

        return jobs

    def _parse_job(self, data: Dict[str, Any]) -> Optional[Job]:
        """Parse Adzuna job data into Job model."""
        try:
            company = Company(
                name=data.get("company", {}).get("display_name", "Unknown"),
                is_startup=self._is_startup(
                    data.get("company", {}).get("display_name", ""),
                    data.get("description", "")
                )
            )

            salary = None
            if data.get("salary_min") or data.get("salary_max"):
                salary = Salary(
                    min_amount=data.get("salary_min"),
                    max_amount=data.get("salary_max"),
                    currency="USD"
                )

            location = data.get("location", {}).get("display_name", "Unknown")
            is_remote = "remote" in location.lower() or "remote" in data.get("title", "").lower()

            return Job(
                id=self._generate_job_id("adzuna", data.get("id", "")),
                title=data.get("title", "Unknown"),
                company=company,
                description=data.get("description", ""),
                url=data.get("redirect_url", ""),
                source=JobSource.ADZUNA,
                location=location,
                is_remote=is_remote,
                salary=salary,
                posted_date=datetime.fromisoformat(data["created"].replace("Z", "+00:00"))
                if data.get("created") else None,
                tags=data.get("category", {}).get("tag", "").split(",") if data.get("category") else []
            )
        except Exception as e:
            print(f"Error parsing Adzuna job: {e}")
            return None


class RemotiveSource(JobSourceBase):
    """Remotive.io job board integration (free API)."""

    BASE_URL = "https://remotive.com/api/remote-jobs"

    def get_source_name(self) -> str:
        return "Remotive"

    def search(self, query: str, location: str = "us", **kwargs) -> List[Job]:
        """Search Remotive for remote jobs."""
        jobs = []

        # Remotive categories relevant to AI/ML
        categories = ["data", "software-dev", "product", "all-others"]

        for category in categories:
            params = {
                "category": category,
                "search": query,
            }

            url = f"{self.BASE_URL}?{urllib.parse.urlencode(params)}"
            response = self._make_request(url)

            if not response or "jobs" not in response:
                continue

            for item in response["jobs"]:
                # Filter for US or remote positions
                candidate_location = item.get("candidate_required_location", "")
                if "worldwide" in candidate_location.lower() or self._is_us_location(candidate_location):
                    job = self._parse_job(item)
                    if job:
                        jobs.append(job)

        return jobs

    def _parse_job(self, data: Dict[str, Any]) -> Optional[Job]:
        """Parse Remotive job data into Job model."""
        try:
            company = Company(
                name=data.get("company_name", "Unknown"),
                website=data.get("company_logo_url", ""),
                is_startup=self._is_startup(
                    data.get("company_name", ""),
                    data.get("description", ""),
                    data.get("tags", [])
                )
            )

            # Parse salary if available
            salary = None
            salary_text = data.get("salary", "")
            if salary_text and "$" in salary_text:
                salary = self._parse_salary_text(salary_text)

            return Job(
                id=self._generate_job_id("remotive", str(data.get("id", ""))),
                title=data.get("title", "Unknown"),
                company=company,
                description=data.get("description", ""),
                url=data.get("url", ""),
                source=JobSource.REMOTIVE,
                location=data.get("candidate_required_location", "Remote"),
                is_remote=True,  # Remotive is all remote jobs
                salary=salary,
                posted_date=datetime.fromisoformat(data["publication_date"].replace("Z", "+00:00"))
                if data.get("publication_date") else None,
                tags=data.get("tags", []),
                job_type=self._parse_job_type(data.get("job_type", ""))
            )
        except Exception as e:
            print(f"Error parsing Remotive job: {e}")
            return None

    def _parse_salary_text(self, text: str) -> Optional[Salary]:
        """Parse salary from text format."""
        import re
        # Try to extract numbers from salary text
        numbers = re.findall(r'[\d,]+', text.replace(",", ""))
        if len(numbers) >= 2:
            return Salary(min_amount=float(numbers[0]), max_amount=float(numbers[1]))
        elif len(numbers) == 1:
            return Salary(min_amount=float(numbers[0]))
        return None

    def _parse_job_type(self, job_type: str) -> JobType:
        """Parse job type string."""
        job_type_lower = job_type.lower()
        if "full" in job_type_lower:
            return JobType.FULL_TIME
        elif "part" in job_type_lower:
            return JobType.PART_TIME
        elif "contract" in job_type_lower:
            return JobType.CONTRACT
        return JobType.UNKNOWN


class TheMuseSource(JobSourceBase):
    """The Muse job board integration."""

    BASE_URL = "https://www.themuse.com/api/public/jobs"

    def get_source_name(self) -> str:
        return "The Muse"

    def search(self, query: str, location: str = "us", **kwargs) -> List[Job]:
        """Search The Muse for jobs."""
        jobs = []

        # The Muse categories
        categories = ["Data Science", "Data Analytics", "Product"]

        for category in categories:
            params = {
                "category": category,
                "location": "United States",
                "page": 1,
            }

            url = f"{self.BASE_URL}?{urllib.parse.urlencode(params)}"
            response = self._make_request(url)

            if not response or "results" not in response:
                continue

            for item in response["results"]:
                job = self._parse_job(item, query)
                if job:
                    jobs.append(job)

        return jobs

    def _parse_job(self, data: Dict[str, Any], query: str) -> Optional[Job]:
        """Parse The Muse job data into Job model."""
        try:
            # Check if job matches query
            title = data.get("name", "")
            if query.lower() not in title.lower():
                return None

            company_data = data.get("company", {})
            company = Company(
                name=company_data.get("name", "Unknown"),
                description=company_data.get("short_name", ""),
                size=company_data.get("size", {}).get("name", ""),
                industry=", ".join([ind.get("name", "") for ind in company_data.get("industries", [])]),
                is_startup=self._is_startup(
                    company_data.get("name", ""),
                    company_data.get("description", "")
                )
            )

            locations = data.get("locations", [])
            location_str = ", ".join([loc.get("name", "") for loc in locations]) or "Unknown"

            return Job(
                id=self._generate_job_id("themuse", str(data.get("id", ""))),
                title=title,
                company=company,
                description=data.get("contents", ""),
                url=data.get("refs", {}).get("landing_page", ""),
                source=JobSource.THE_MUSE,
                location=location_str,
                is_remote="remote" in location_str.lower(),
                posted_date=datetime.fromisoformat(data["publication_date"].replace("Z", "+00:00"))
                if data.get("publication_date") else None,
                experience_level=self._parse_experience_level(data.get("levels", []))
            )
        except Exception as e:
            print(f"Error parsing The Muse job: {e}")
            return None

    def _parse_experience_level(self, levels: List[Dict]) -> ExperienceLevel:
        """Parse experience level from The Muse data."""
        if not levels:
            return ExperienceLevel.UNKNOWN

        level_name = levels[0].get("name", "").lower()
        if "entry" in level_name or "junior" in level_name:
            return ExperienceLevel.ENTRY
        elif "mid" in level_name:
            return ExperienceLevel.MID
        elif "senior" in level_name:
            return ExperienceLevel.SENIOR
        elif "lead" in level_name or "manager" in level_name:
            return ExperienceLevel.LEAD
        elif "executive" in level_name or "director" in level_name:
            return ExperienceLevel.EXECUTIVE

        return ExperienceLevel.UNKNOWN


class JobAggregator:
    """Aggregates jobs from multiple sources."""

    def __init__(self, config: Optional[APIConfig] = None):
        self.config = config or APIConfig()
        self.sources: List[JobSourceBase] = [
            RemotiveSource(self.config),  # Free API, no key needed
            TheMuseSource(self.config),   # Free API, no key needed
        ]

        # Add Adzuna if configured
        if self.config.adzuna_app_id and self.config.adzuna_api_key:
            self.sources.append(AdzunaSource(self.config))

    def search_all(self, query: str, location: str = "us", **kwargs) -> List[Job]:
        """Search all configured job sources."""
        all_jobs = []
        seen_ids = set()

        for source in self.sources:
            print(f"Searching {source.get_source_name()}...")
            try:
                jobs = source.search(query, location, **kwargs)
                for job in jobs:
                    if job.id not in seen_ids:
                        seen_ids.add(job.id)
                        all_jobs.append(job)
                print(f"  Found {len(jobs)} jobs from {source.get_source_name()}")
            except Exception as e:
                print(f"  Error searching {source.get_source_name()}: {e}")

        return all_jobs

    def add_source(self, source: JobSourceBase):
        """Add a new job source."""
        self.sources.append(source)
