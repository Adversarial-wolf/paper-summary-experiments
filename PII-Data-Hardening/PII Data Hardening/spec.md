# Spec: PII Data Hardening Implementation

## Objective
Implement a PII data hardening system for x402 agentic payments that detects and redacts personally identifiable information from payment metadata before transmission. The system should be able to:
- Detect PII in various metadata fields (URLs, descriptions, reason strings)
- Apply filtering based on declarative spending policies
- Block duplicate request attempts
- Maintain performance within 50ms overhead budget
- Demonstrate high precision and recall (F1 > 0.85)

## Tech Stack
- Python 3.8+
- Presidio NLP library for PII detection
- Jupyter Notebook for experimentation
- Pandas for data handling
- Scikit-learn for metrics calculation
- Regular expressions for basic pattern matching

## Commands
```
Build: n/a
Test: python -m pytest tests/
Lint: python -m flake8 .
Dev: jupyter notebook
```

## Project Structure
```
PII Data Hardening/
├── spec.md                 # This specification
├── src/
│   ├── __init__.py
│   ├── pii_filter.py       # Main PII filtering functions
│   ├── synthetic_data.py   # Synthetic data generation
│   └── utils.py            # Helper utilities
├── experiments/
│   └── pii_hardening_experiment.ipynb  # Jupyter notebook with experiments
├── tests/
│   ├── __init__.py
│   └── test_pii_filter.py
└── README.md               # Documentation
```

## Code Style
- Follow PEP8 style guide
- Use descriptive variable names
- Include docstrings for all functions
- Modular design with clear separation of concerns
- Example:
```python
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
        # regex implementation
    elif method == "nlp":
        # nlp implementation
    else:
        raise ValueError("Unknown method")
```

## Testing Strategy
- Unit tests for each function in pii_filter.py
- Integration tests for complete pipeline
- Performance tests to ensure <50ms latency
- Evaluation tests with synthetic dataset
- Use pytest framework

## Boundaries
- Always: 
  - Validate inputs to all functions
  - Run tests before any commit
  - Follow PEP8 styling rules
- Ask first: 
  - Adding new dependencies
  - Modifying existing test structure
- Never: 
  - Commit secrets or credentials
  - Run tests without proper environment setup
  - Use external APIs without proper authorization

## Success Criteria
- PII detection accuracy > 0.85 F1 score
- Processing latency < 50ms
- Support for both regex and NLP detection methods
- Complete synthetic dataset generation
- Jupyter notebook with comprehensive experimentation results

## Open Questions
Should we include support for more PII types beyond what's mentioned in the paper?