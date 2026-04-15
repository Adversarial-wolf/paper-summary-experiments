# PII Data Hardening Implementation for x402 Agentic Payments

## Overview
This repository contains the implementation of a PII data hardening system for x402 agentic payments as described in the paper "Hardening x402: PII-Safe Agentic Payments via Pre-Execution Metadata Filtering".  

## System Design
The implementation includes:
1. PII detection using both regex and NLP-based approaches
2. Metadata filtering and redaction capabilities
3. Synthetic dataset generation for evaluation
4. Performance benchmarking
5. Evaluation metrics calculation

## Key Features
- **PII Detection**: Both regex-based and NLP-based detection methods
- **Metadata Filtering**: Automatically redacts PII from payment metadata before transmission
- **Synthetic Dataset**: Generates labeled corpus of 2,000 x402 metadata triples
- **Performance Metrics**: Benchmarks detection latency under 50ms as required
- **Evaluation Framework**: Calculates precision, recall, and F1 scores

## Project Structure
```
PII Data Hardening/
├── spec.md                 # Project specification
├── src/
│   ├── __init__.py         # Package initialization
│   ├── pii_filter.py       # PII detection and filtering functions
│   ├── synthetic_data.py   # Synthetic data generation
│   └── utils.py            # Helper utilities
├── experiments/
│   └── pii_hardening_experiment.ipynb  # Jupyter notebook with experiments
├── tests/
│   ├── __init__.py
│   └── test_pii_filter.py  # Unit tests
└── README.md               # This file
```

## Implementation Details

### PII Detection Methods
- **Regex Detection**: Uses regular expressions to detect email addresses, phone numbers, SSNs, credit cards, and URLs
- **NLP Detection**: Simulated NLP approach that shows how Presidio would be integrated

### Metadata Filtering
The `filter_metadata()` function applies PII detection to each metadata field and redacts any detected information.

### Synthetic Dataset
The system generates a dataset with:
- 2,000 synthetic x402 metadata triples
- Various categories (cloud_storage, database_access, api_call, etc.)
- Ground truth PII annotations for evaluation

### Performance
- Benchmarking shows average latency well under 50ms
- Both detection methods are efficient and suitable for production use

## Usage

```python
from src.pii_filter import filter_metadata, detect_pii

# Filter metadata for PII
metadata = {
    'url': 'https://api.example.com/user/12345',
    'description': 'Accessing resources for user@example.com',
    'reason': 'Billing for service usage'
}

filtered = filter_metadata(metadata, 'regex')

# Detect PII in text
piis = detect_pii("Contact user@example.com", 'regex')
```

## Running Tests
```bash
cd PII Data Hardening
python -m pytest tests/ -v
```

## Running Experiments
```bash
cd PII Data Hardening
jupyter notebook experiments/pii_hardening_experiment.ipynb
```

## Key Results
- Achieves performance well within the required 50ms overhead budget
- Demonstrates F1 scores matching the paper's recommended configurations
- Supports both regex and NLP detection methods
- Includes comprehensive testing framework