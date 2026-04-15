# 📋 PII Entity Taxonomy & Surface Forms

## Supported Entity Types (Presidio + Extensions)

### Core Entities (Presidio Built-in)
| Entity | Description | Regex Pattern | NLP Required | Example Surface Forms |
|--------|-------------|---------------|--------------|---------------------|
| `EMAIL_ADDRESS` | RFC 5322 compliant email | ✅ Yes | ❌ No | `user@example.com`, `user%40example.com`, `?email=user@example.com` |
| `PERSON` | Human name (first, last, full) | ❌ No | ✅ Yes | `Alice Martin`, `alice-martin`, `A. Martin`, `Martin, Alice` |
| `US_SSN` | US Social Security Number | ✅ `XXX-XX-XXXX` | ❌ No | `123-45-6789`, `123456789` |
| `IBAN_CODE` | International Bank Account Number | ✅ ISO 13616 | ❌ No | `DE89370400440532013000`, `GB29NWBK60161331926819` |
| `PHONE_NUMBER` | Telephone number (US/intl.) | ✅ US formats | ✅ Contextual | `(415) 555-0182`, `+14155550182`, `415-555-0182` |
| `CREDIT_CARD` | Payment card number (Luhn-valid) | ✅ 13-19 digits + Luhn | ❌ No | `4111111111111111`, `5500 0000 0000 0004` |

### Domain-Specific Extensions (Custom Recognizers)
| Entity | Use Case | Pattern Example | Confidence |
|--------|----------|----------------|------------|
| `MEDICAL_RECORD_NUMBER` | Healthcare systems | `MRN-\d{8,10}` | 0.95 |
| `EMPLOYEE_ID` | Corporate systems | `EMP-\d{6}` | 0.95 |
| `PATIENT_ID` | Clinical trials | `PT-\d{4}-\d{4}` | 0.90 |
| `FINANCIAL_ACCOUNT` | Banking apps | `ACC-\d{10,12}` | 0.92 |

## Surface Form Handling Strategy

### URL-Specific Challenges
```python
# Preprocessing pipeline for resource_url field
def preprocess_url(url: str) -> list[str]:
    """Extract tokenizable segments from URL for NER"""
    segments = []
    
    # Decode URL encoding
    decoded = urllib.parse.unquote(url)
    segments.append(decoded)
    
    # Split path segments on delimiters
    path = urllib.parse.urlparse(decoded).path
    for delimiter in ['/', '-', '_', '.', '?', '&', '=']:
        path = path.replace(delimiter, ' ')
    segments.append(path)
    
    # Extract query parameters
    params = urllib.parse.parse_qs(urllib.parse.urlparse(decoded).query)
    segments.extend(params.keys())
    segments.extend(v for values in params.values() for v in values)
    
    return segments
```

### Confidence Score Calibration
| Entity | Typical Score Range | Recommended min_score | Notes |
|--------|-------------------|---------------------|-------|
| EMAIL_ADDRESS | 0.95-1.0 | 0.85 | Structural patterns highly reliable |
| PERSON | 0.35-0.95 | 0.40 | Context-dependent; lower bound for URL slugs |
| US_SSN | 0.90-1.0 | 0.85 | Format strict; high confidence |
| PHONE_NUMBER | 0.40-1.0 | 0.40 | Compact intl. formats score ~0.45 |
| IBAN_CODE | 0.95-1.0 | 0.85 | Country-specific validation boosts confidence |
| CREDIT_CARD | 0.90-1.0 | 0.85 | Luhn check + format = high confidence |

## False Positive Mitigation Strategies

### Common False Positive Sources
| Trigger | Example | Mitigation |
|---------|---------|-----------|
| Service names matching PERSON | "Export for Alice Service" | Add negative examples to custom recognizer |
| Numeric IDs matching SSN | "Order #123-45-6789" | Context-aware filtering: require "SSN" keyword nearby |
| Random strings matching IBAN | "Ref: DE89370400440532013000" | Domain whitelist: only scan known PII-bearing endpoints |

### Custom Context Rules
```python
# Example: Require contextual keywords for SSN detection
def contextual_ssn_filter(text: str, entity_result) -> bool:
    """Only flag SSN if contextual keywords present"""
    context_keywords = ['ssn', 'social security', 'tax id', 'employee id']
    window = text[max(0, entity_result.start-20):entity_result.end+20].lower()
    return any(keyword in window for keyword in context_keywords)

# Integrate with Presidio via custom logic
if entity_result.entity_type == "US_SSN":
    if not contextual_ssn_filter(text, entity_result):
        continue  # Skip redaction
```
