"""
Data models for job listings.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from enum import Enum


class JobSource(Enum):
    """Enumeration of job sources."""
    ADZUNA = "adzuna"
    REMOTIVE = "remotive"
    THE_MUSE = "the_muse"
    GITHUB_JOBS = "github_jobs"
    MANUAL = "manual"


class ExperienceLevel(Enum):
    """Job experience levels."""
    ENTRY = "entry"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    EXECUTIVE = "executive"
    UNKNOWN = "unknown"


class JobType(Enum):
    """Employment types."""
    FULL_TIME = "full_time"
    PART_TIME = "part_time"
    CONTRACT = "contract"
    INTERNSHIP = "internship"
    UNKNOWN = "unknown"


@dataclass
class Company:
    """Represents a company."""
    name: str
    description: Optional[str] = None
    website: Optional[str] = None
    size: Optional[str] = None
    industry: Optional[str] = None
    is_startup: bool = False
    funding_stage: Optional[str] = None
    location: Optional[str] = None


@dataclass
class Salary:
    """Represents salary information."""
    min_amount: Optional[float] = None
    max_amount: Optional[float] = None
    currency: str = "USD"
    period: str = "yearly"  # yearly, monthly, hourly

    def __str__(self) -> str:
        if self.min_amount and self.max_amount:
            return f"${self.min_amount:,.0f} - ${self.max_amount:,.0f} {self.period}"
        elif self.min_amount:
            return f"${self.min_amount:,.0f}+ {self.period}"
        elif self.max_amount:
            return f"Up to ${self.max_amount:,.0f} {self.period}"
        return "Not specified"


@dataclass
class Job:
    """Represents a job listing."""
    id: str
    title: str
    company: Company
    description: str
    url: str
    source: JobSource

    # Location
    location: str = "Unknown"
    is_remote: bool = False

    # Categorization
    categories: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)

    # Details
    salary: Optional[Salary] = None
    experience_level: ExperienceLevel = ExperienceLevel.UNKNOWN
    job_type: JobType = JobType.UNKNOWN

    # Requirements
    required_skills: List[str] = field(default_factory=list)
    preferred_skills: List[str] = field(default_factory=list)

    # Metadata
    posted_date: Optional[datetime] = None
    expires_date: Optional[datetime] = None
    fetched_at: datetime = field(default_factory=datetime.now)

    # Scoring
    relevance_score: float = 0.0

    def __str__(self) -> str:
        remote_tag = " [Remote]" if self.is_remote else ""
        startup_tag = " [Startup]" if self.company.is_startup else ""
        return (
            f"{self.title} at {self.company.name}{remote_tag}{startup_tag}\n"
            f"  Location: {self.location}\n"
            f"  Salary: {self.salary or 'Not specified'}\n"
            f"  Categories: {', '.join(self.categories) if self.categories else 'N/A'}\n"
            f"  URL: {self.url}"
        )

    def to_dict(self) -> dict:
        """Convert job to dictionary for serialization."""
        return {
            "id": self.id,
            "title": self.title,
            "company": {
                "name": self.company.name,
                "description": self.company.description,
                "website": self.company.website,
                "is_startup": self.company.is_startup,
                "funding_stage": self.company.funding_stage,
            },
            "description": self.description,
            "url": self.url,
            "source": self.source.value,
            "location": self.location,
            "is_remote": self.is_remote,
            "categories": self.categories,
            "tags": self.tags,
            "salary": {
                "min": self.salary.min_amount if self.salary else None,
                "max": self.salary.max_amount if self.salary else None,
                "currency": self.salary.currency if self.salary else "USD",
            } if self.salary else None,
            "experience_level": self.experience_level.value,
            "job_type": self.job_type.value,
            "required_skills": self.required_skills,
            "posted_date": self.posted_date.isoformat() if self.posted_date else None,
            "relevance_score": self.relevance_score,
        }


@dataclass
class SearchResults:
    """Container for search results."""
    jobs: List[Job]
    total_count: int
    query: str
    categories: List[str]
    fetched_at: datetime = field(default_factory=datetime.now)

    def filter_by_category(self, category: str) -> List[Job]:
        """Filter jobs by category."""
        return [job for job in self.jobs if category in job.categories]

    def filter_startups(self) -> List[Job]:
        """Filter to only startup jobs."""
        return [job for job in self.jobs if job.company.is_startup]

    def filter_remote(self) -> List[Job]:
        """Filter to only remote jobs."""
        return [job for job in self.jobs if job.is_remote]

    def sort_by_relevance(self) -> List[Job]:
        """Sort jobs by relevance score."""
        return sorted(self.jobs, key=lambda j: j.relevance_score, reverse=True)

    def sort_by_date(self) -> List[Job]:
        """Sort jobs by posted date (newest first)."""
        return sorted(
            self.jobs,
            key=lambda j: j.posted_date or datetime.min,
            reverse=True
        )
