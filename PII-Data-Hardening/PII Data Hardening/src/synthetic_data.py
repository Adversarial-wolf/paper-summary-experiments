"""
Synthetic Data Generation for PII Detection
"""

import pandas as pd
import random
from typing import List, Dict
import json

# Define PII types for synthetic data
PII_TYPES = ["email", "phone", "ssn", "credit_card", "url", "name", "address"]

# Define categories for metadata
CATEGORIES = [
    "cloud_storage",
    "database_access",
    "api_call",
    "file_transfer",
    "payment_processing",
    "user_authentication",
    "data_analytics",
]

# Sample templates for different metadata fields
URL_TEMPLATES = [
    "https://api.example.com/{category}/{resource}",
    "https://storage.example.com/{category}/{resource}",
    "https://app.example.com/{category}/{resource}",
]

DESCRIPTION_TEMPLATES = [
    "Access to {category} resources for user {user}",
    "Processing payment for {category} service",
    "Querying {category} database for user {user}",
    "Downloading {category} data for analysis",
    "Creating {category} resource for {user}",
]

REASON_TEMPLATES = [
    "User {user} requested {category} access",
    "Billing for {category} service usage",
    "Processing {category} transaction",
    "Analyzing {category} data for {user}",
    "Accessing {category} resources for {user}",
]


def generate_sample_pii() -> Dict:
    """Generate a sample PII entry."""
    piis = []

    # Generate different types of PII
    if random.random() > 0.7:
        piis.append(
            {"type": "email", "value": f"user{random.randint(1000, 9999)}@example.com"}
        )

    if random.random() > 0.7:
        piis.append({"type": "phone", "value": f"123-456-{random.randint(1000, 9999)}"})

    if random.random() > 0.7:
        piis.append(
            {
                "type": "ssn",
                "value": f"{random.randint(100, 999)}-{random.randint(10, 99)}-{random.randint(1000, 9999)}",
            }
        )

    if random.random() > 0.8:
        piis.append(
            {
                "type": "credit_card",
                "value": f"{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",
            }
        )

    if random.random() > 0.5:
        piis.append(
            {
                "type": "url",
                "value": f"https://api.example.com/user/{random.randint(1000, 9999)}",
            }
        )

    return piis


def generate_metadata_sample() -> Dict:
    """Generate a sample metadata entry."""
    category = random.choice(CATEGORIES)

    # Create PII entries and sample text
    pii_entries = generate_sample_pii()

    # Create metadata with various fields
    metadata = {
        "url": random.choice(URL_TEMPLATES).format(
            category=category, resource=random.randint(1000, 9999)
        ),
        "description": random.choice(DESCRIPTION_TEMPLATES).format(
            category=category, user=f"User{random.randint(1000, 9999)}"
        ),
        "reason": random.choice(REASON_TEMPLATES).format(
            category=category, user=f"User{random.randint(1000, 9999)}"
        ),
        "category": category,
        "timestamp": pd.Timestamp.now().isoformat(),
    }

    # Inject PII into metadata fields
    for pii in pii_entries:
        if pii["type"] == "email" and "email" in metadata["description"]:
            metadata["description"] = metadata["description"].replace(
                f"User{random.randint(1000, 9999)}",
                f"User{random.randint(1000, 9999)} ({pii['value']})",
            )
        elif pii["type"] == "phone" and "user" in metadata["description"]:
            metadata["description"] = metadata["description"].replace(
                f"User{random.randint(1000, 9999)}",
                f"User{random.randint(1000, 9999)} ({pii['value']})",
            )
        elif pii["type"] == "ssn" and "user" in metadata["reason"]:
            metadata["reason"] = metadata["reason"].replace(
                f"User{random.randint(1000, 9999)}",
                f"User{random.randint(1000, 9999)} ({pii['value']})",
            )

    return metadata


def generate_synthetic_corpus(size: int = 2000) -> pd.DataFrame:
    """
    Generate a synthetic corpus of x402 metadata triples.

    Args:
        size (int): Number of samples to generate

    Returns:
        pd.DataFrame: DataFrame with metadata samples
    """
    samples = []

    for i in range(size):
        metadata = generate_metadata_sample()
        samples.append(
            {
                "id": i,
                "metadata": metadata,
                "pii_injection": len(generate_sample_pii()),
                "category": metadata["category"],
            }
        )

    return pd.DataFrame(samples)


def generate_synthetic_corpus_with_labels(size: int = 2000) -> pd.DataFrame:
    """
    Generate a synthetic corpus with ground truth labels for evaluation.

    Args:
        size (int): Number of samples to generate

    Returns:
        pd.DataFrame: DataFrame with metadata samples and labels
    """
    samples = []

    for i in range(size):
        metadata = generate_metadata_sample()
        # Generate ground truth PII detection
        ground_truth = generate_sample_pii()

        samples.append(
            {
                "id": i,
                "metadata": metadata,
                "ground_truth_pii": ground_truth,
                "category": metadata["category"],
                "metadata_text": f"{metadata['url']} {metadata['description']} {metadata['reason']}",
            }
        )

    return pd.DataFrame(samples)


def save_corpus(df: pd.DataFrame, filename: str) -> None:
    """Save synthetic corpus to file."""
    df.to_csv(filename, index=False)
    print(f"Saved corpus to {filename}")


def load_corpus(filename: str) -> pd.DataFrame:
    """Load synthetic corpus from file."""
    return pd.read_csv(filename)
