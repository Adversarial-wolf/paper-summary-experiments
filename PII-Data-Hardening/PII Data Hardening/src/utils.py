"""
Helper utilities for PII data hardening
"""


def merge_dicts(dict1, dict2):
    """Merge two dictionaries."""
    merged = dict1.copy()
    merged.update(dict2)
    return merged


def validate_metadata(metadata):
    """Validate metadata structure."""
    required_fields = ["url", "description", "reason"]
    for field in required_fields:
        if field not in metadata:
            raise ValueError(f"Missing required field: {field}")
    return True


def get_pii_types():
    """Return list of known PII types."""
    return ["email", "phone", "ssn", "credit_card", "url", "name", "address"]
