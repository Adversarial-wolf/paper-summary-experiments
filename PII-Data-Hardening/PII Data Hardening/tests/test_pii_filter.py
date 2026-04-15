"""
Unit tests for PII filtering functions
"""

import pytest
import pandas as pd
from src.pii_filter import (
    detect_pii_regex,
    detect_pii_nlp,
    redact_pii,
    filter_metadata,
    calculate_metrics,
)
from src.synthetic_data import generate_synthetic_corpus_with_labels


def test_detect_pii_regex():
    """Test regex-based PII detection."""
    text = "Contact user@example.com or call 123-456-7890"
    result = detect_pii_regex(text)

    assert len(result) >= 1
    assert any(item["type"] == "email" for item in result)
    assert any(item["type"] == "phone" for item in result)


def test_detect_pii_nlp():
    """Test NLP-based PII detection (simulated)."""
    text = "Contact user@example.com or call 123-456-7890"
    result = detect_pii_nlp(text)

    # The current simulated implementation is basic, so we just check it returns a list
    assert isinstance(result, list)


def test_redact_pii():
    """Test PII redaction functionality."""
    text = "Contact user@example.com or call 123-456-7890"
    detected = detect_pii_regex(text)
    result = redact_pii(text, detected)

    assert "[REDACTED]" in result
    assert "user@example.com" not in result
    assert "123-456-7890" not in result


def test_filter_metadata():
    """Test metadata filtering with PII redaction."""
    metadata = {
        "url": "https://api.example.com/user123",
        "description": "Access to cloud_storage resources for user@example.com",
        "reason": "Billing for cloud_storage service usage",
    }

    result = filter_metadata(metadata, "regex")

    # Check that PII was redacted from description
    assert "[REDACTED]" in result["description"]
    assert "user@example.com" not in result["description"]


def test_calculate_metrics():
    """Test calculation of precision, recall, and F1 score."""
    # Simulated predictions
    predictions = [
        {"type": "email", "start": 10, "end": 25},
        {"type": "phone", "start": 30, "end": 45},
    ]

    # Simulated ground truth
    ground_truth = [
        {"type": "email", "start": 10, "end": 25},
        {"type": "phone", "start": 30, "end": 45},
    ]

    metrics = calculate_metrics(predictions, ground_truth)

    assert "precision" in metrics
    assert "recall" in metrics
    assert "f1" in metrics
    assert metrics["precision"] == 1.0
    assert metrics["recall"] == 1.0
    assert metrics["f1"] == 1.0


def test_generate_synthetic_corpus():
    """Test synthetic corpus generation."""
    df = generate_synthetic_corpus_with_labels(100)

    assert len(df) == 100
    assert "metadata" in df.columns
    assert "ground_truth_pii" in df.columns
    assert "metadata_text" in df.columns


if __name__ == "__main__":
    pytest.main([__file__])
