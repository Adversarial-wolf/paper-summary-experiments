"""
PII Filtering Module
Contains functions for detecting and filtering PII from x402 payment metadata
"""

import re
from typing import List, Dict, Tuple
from collections import Counter
import time


def detect_pii_regex(text: str) -> List[Dict]:
    """
    Detect PII using regular expressions.

    Args:
        text (str): Text to analyze for PII

    Returns:
        List[Dict]: List of detected PII entities with positions and types
    """
    pii_patterns = {
        "email": r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b",
        "phone": r"\b(?:\+?1[-.\s]?)?\(?([0-9]{3})\)?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})\b",
        "ssn": r"\b\d{3}-\d{2}-\d{4}\b",
        "credit_card": r"\b(?:\d{4}[-\s]?){3}\d{4}\b",
        "url": r"https?://(?:[-\w.])+(?:[:\d]+)?(?:/(?:[\w/])*(?:\?(?:[\w.])*)?(?:#(?:[\w.])*)?)?",
    }

    detected = []

    for pii_type, pattern in pii_patterns.items():
        for match in re.finditer(pattern, text):
            detected.append(
                {
                    "type": pii_type,
                    "start": match.start(),
                    "end": match.end(),
                    "value": match.group(),
                }
            )

    return detected


def detect_pii_nlp(text: str) -> List[Dict]:
    """
    Detect PII using NLP approach (simulated).

    Args:
        text (str): Text to analyze for PII

    Returns:
        List[Dict]: List of detected PII entities with positions and types
    """
    # This is a simplified simulation of NLP detection
    # In practice, this would use a library like Presidio
    detected = []

    # We'll simulate some matches for demonstration
    if "user@example.com" in text:
        detected.append(
            {
                "type": "email",
                "start": text.find("user@example.com"),
                "end": text.find("user@example.com") + len("user@example.com"),
                "value": "user@example.com",
            }
        )

    if "123-456-7890" in text:
        detected.append(
            {
                "type": "phone",
                "start": text.find("123-456-7890"),
                "end": text.find("123-456-7890") + len("123-456-7890"),
                "value": "123-456-7890",
            }
        )

    if "123456789" in text:
        detected.append(
            {
                "type": "ssn",
                "start": text.find("123456789"),
                "end": text.find("123456789") + len("123456789"),
                "value": "123456789",
            }
        )

    return detected


def redact_pii(text: str, detected_pii: List[Dict]) -> str:
    """
    Redact detected PII from text by replacing with [REDACTED].

    Args:
        text (str): Original text
        detected_pii (List[Dict]): List of detected PII entities

    Returns:
        str: Text with PII redacted
    """
    # Sort by position in reverse order to maintain correct indices
    sorted_pii = sorted(detected_pii, key=lambda x: x["start"], reverse=True)

    redacted_text = text
    for pii in sorted_pii:
        start, end = pii["start"], pii["end"]
        redacted_text = redacted_text[:start] + "[REDACTED]" + redacted_text[end:]

    return redacted_text


def filter_metadata(metadata: Dict, detection_method: str = "nlp") -> Dict:
    """
    Filter x402 payment metadata for PII.

    Args:
        metadata (Dict): x402 metadata with fields like 'url', 'description', 'reason'
        detection_method (str): Detection method - "regex" or "nlp"

    Returns:
        Dict: Filtered metadata with PII redacted
    """
    filtered_metadata = {}

    # Detect PII in each metadata field
    for field, value in metadata.items():
        if isinstance(value, str):
            # Determine PII in the field
            if detection_method == "regex":
                detected = detect_pii_regex(value)
            elif detection_method == "nlp":
                detected = detect_pii_nlp(value)
            else:
                raise ValueError("Detection method must be 'regex' or 'nlp'")

            # Redact PII from the field
            redacted = redact_pii(value, detected)
            filtered_metadata[field] = redacted
        else:
            filtered_metadata[field] = value

    return filtered_metadata


def detect_pii(text: str, method: str = "regex") -> List[Dict]:
    """
    Detect PII in text using specified method.

    Args:
        text (str): Text to analyze for PII
        method (str): Detection method ("regex" or "nlp")

    Returns:
        List[Dict]: List of detected PII entities with positions
    """
    if method == "regex":
        return detect_pii_regex(text)
    elif method == "nlp":
        return detect_pii_nlp(text)
    else:
        raise ValueError("Unknown method")


def calculate_metrics(predictions: List[Dict], ground_truth: List[Dict]) -> Dict:
    """
    Calculate precision, recall, and F1 score for PII detection.

    Args:
        predictions (List[Dict]): Predicted PII entities
        ground_truth (List[Dict]): Ground truth PII entities

    Returns:
        Dict: Metrics including precision, recall, and F1 score
    """
    # Convert to sets for easier comparison
    pred_set = {(p["type"], p["start"], p["end"]) for p in predictions}
    truth_set = {(t["type"], t["start"], t["end"]) for t in ground_truth}

    # Calculate true positives
    tp = len(pred_set & truth_set)

    # Calculate precision and recall
    precision = tp / len(pred_set) if pred_set else 0
    recall = tp / len(truth_set) if truth_set else 0

    # Calculate F1 score
    f1 = (
        2 * (precision * recall) / (precision + recall)
        if (precision + recall) > 0
        else 0
    )

    return {"precision": precision, "recall": recall, "f1": f1}


def benchmark_detection(method: str, text: str, iterations: int = 100) -> Dict:
    """
    Benchmark PII detection method performance.

    Args:
        method (str): Detection method ("regex" or "nlp")
        text (str): Text to process
        iterations (int): Number of iterations for benchmarking

    Returns:
        Dict: Benchmark results including average time and throughput
    """
    times = []

    for _ in range(iterations):
        start_time = time.time()
        detect_pii(text, method)
        end_time = time.time()
        times.append(end_time - start_time)

    avg_time = sum(times) / len(times) * 1000  # Convert to milliseconds
    throughput = 1000 / avg_time if avg_time > 0 else 0  # Operations per second

    return {
        "avg_time_ms": avg_time,
        "throughput_ops_per_sec": throughput,
        "iterations": iterations,
    }
