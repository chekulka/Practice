"""
Configuration for AI/ML Job Hunter.

Defines job categories, search keywords, and API configurations.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class JobCategory:
    """Represents a job category with associated search terms."""
    name: str
    keywords: List[str]
    title_patterns: List[str]


# Define AI/ML job categories
JOB_CATEGORIES: Dict[str, JobCategory] = {
    "data_analytics": JobCategory(
        name="Data Analytics",
        keywords=[
            "data analyst", "analytics engineer", "business analyst",
            "data analytics", "analytics", "BI analyst", "business intelligence"
        ],
        title_patterns=[
            "data analyst", "analytics", "bi analyst", "business intelligence"
        ]
    ),
    "ab_experimentation": JobCategory(
        name="A/B Experimentation",
        keywords=[
            "a/b testing", "experimentation", "experiment analyst",
            "growth analyst", "experimentation platform", "ab testing",
            "experiment", "testing analyst", "optimization"
        ],
        title_patterns=[
            "experimentation", "experiment", "a/b", "ab test", "growth"
        ]
    ),
    "causal_inference": JobCategory(
        name="Causal Inference",
        keywords=[
            "causal inference", "econometrics", "causal ml",
            "applied scientist", "research scientist", "economist",
            "quantitative researcher", "causal", "inference"
        ],
        title_patterns=[
            "causal", "economist", "applied scientist", "research scientist"
        ]
    ),
    "data_science": JobCategory(
        name="Data Science",
        keywords=[
            "data scientist", "data science", "machine learning",
            "ml engineer", "ai engineer", "deep learning",
            "nlp", "computer vision", "predictive modeling"
        ],
        title_patterns=[
            "data scientist", "machine learning", "ml engineer",
            "ai engineer", "data science"
        ]
    ),
    "product_management": JobCategory(
        name="AI/ML Product Management",
        keywords=[
            "product manager ai", "product manager ml", "product manager data",
            "technical product manager", "ai product", "ml product",
            "data product manager", "platform product manager"
        ],
        title_patterns=[
            "product manager", "product lead", "product owner"
        ]
    )
}

# Startup indicators in company descriptions or tags
STARTUP_INDICATORS = [
    "startup", "series a", "series b", "series c", "seed",
    "early stage", "fast-growing", "rapidly growing", "venture-backed",
    "funded", "pre-ipo", "scale-up", "scaleup", "growth stage",
    "emerging", "disruptive", "innovative"
]

# US location filters
US_LOCATIONS = [
    "united states", "usa", "us", "remote", "san francisco",
    "new york", "seattle", "austin", "boston", "los angeles",
    "chicago", "denver", "miami", "atlanta", "california",
    "texas", "washington", "massachusetts", "colorado", "georgia",
    "florida", "illinois", "ny", "sf", "la", "nyc", "bay area"
]

# API Configuration
@dataclass
class APIConfig:
    """Configuration for job board APIs."""
    # Adzuna API (free tier available)
    adzuna_app_id: Optional[str] = None
    adzuna_api_key: Optional[str] = None

    # The Muse API (free)
    muse_api_key: Optional[str] = None

    # Request settings
    request_timeout: int = 30
    max_retries: int = 3
    results_per_page: int = 50


# Default configuration
DEFAULT_CONFIG = APIConfig()


# Search configuration
@dataclass
class SearchConfig:
    """Configuration for job searches."""
    categories: List[str] = field(default_factory=lambda: list(JOB_CATEGORIES.keys()))
    location: str = "us"
    remote_only: bool = False
    startup_only: bool = True
    days_old: int = 30
    min_salary: Optional[int] = None
    max_results: int = 100
