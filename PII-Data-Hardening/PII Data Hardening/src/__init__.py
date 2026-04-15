"""
__init__.py for PII Data Hardening package
"""

from .pii_filter import (
    detect_pii,
    detect_pii_regex,
    detect_pii_nlp,
    redact_pii,
    filter_metadata,
    calculate_metrics,
    benchmark_detection,
)

from .synthetic_data import (
    generate_synthetic_corpus,
    generate_synthetic_corpus_with_labels,
    save_corpus,
    load_corpus,
)

from .utils import merge_dicts, validate_metadata, get_pii_types

__all__ = [
    "detect_pii",
    "detect_pii_regex",
    "detect_pii_nlp",
    "redact_pii",
    "filter_metadata",
    "calculate_metrics",
    "benchmark_detection",
    "generate_synthetic_corpus",
    "generate_synthetic_corpus_with_labels",
    "save_corpus",
    "load_corpus",
    "merge_dicts",
    "validate_metadata",
    "get_pii_types",
]
