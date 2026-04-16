# 🔬 Hypothesis Testing & Statistical Analysis

## Hypotheses Formulation
```mermaid
graph TD
    H[Hypotheses] --> H1["H1: resource_url has highest PII injection rate"]
    H --> H2["H2: EMAIL+PERSON ≥70% of all entity labels"]
    H --> H3["H3: NLP adds PERSON recall over regex"]
    H --> H4["H4: Top-3 entity types capture ≥95% of full recall"]
    H --> H5["H5: NLP overhead exceeds 50ms latency budget"]
```

## Statistical Methods
- **Precision/Recall/F1**: Standard information retrieval metrics
- **Micro-averaging**: Aggregate TP/FP/FN across all entity types before computing F1
- **Latency**: Percentile-based (p50/p95/p99) to capture tail behavior
- **Significance**: Bootstrap confidence intervals (1,000 resamples, 95% CI)

## Results Summary

### H1: `resource_url` has highest PII injection rate
```python
# Observed distribution
field_counts = {
    'resource_url': 396,  # 45.3%
    'description': 333,   # 38.1% 
    'reason': 146         # 16.6%
}
```
✅ **Confirmed**: URL field contains plurality of PII labels  
🎯 **Implication**: Prioritize `resource_url` scanning in resource-constrained deployments

### H2: EMAIL+PERSON ≥70% of all entity labels
```python
# Entity distribution
entity_counts = {
    'EMAIL_ADDRESS': 312,  # 35.7%
    'PERSON': 322,         # 36.8%
    # ... others
}
email_person_pct = (312 + 322) / 875  # = 72.5%
```
✅ **Confirmed**: Two entities dominate PII landscape  
🎯 **Implication**: Minimum viable filter should support EMAIL + PERSON

### H3: NLP adds PERSON recall over regex
```python
# PERSON detection results
regex_person_recall = 0.000   # Regex cannot detect names
nlp_person_recall = 0.551     # NLP recovers ~55% of name instances
delta = 0.551                 # +55.1 percentage points
```
✅ **Confirmed**: NLP essential for PERSON detection  
⚠️ **Caveat**: Recall still limited by URL context (see PERSON Recall Ceiling)

### H4: Top-3 types capture ≥95% of full recall
```python
# Cumulative recall by entity (sorted by frequency)
cumulative_recall = {
    'EMAIL+PERSON': 0.725,
    '+PHONE_NUMBER': 0.827,   # Top-3
    '+US_SSN': 0.891,         # Top-4
    '+IBAN_CODE': 0.946,      # Top-5
    '+CREDIT_CARD': 1.000     # All 6
}
top3_recall = 0.827  # < 0.95 threshold
```
❌ **Refuted**: Top-3 entities capture only 82.7% of full recall  
🎯 **Recommendation**: Deploy all 6 entity types—marginal latency cost for meaningful recall gain

### H5: NLP overhead >50ms latency budget
```python
# Observed latencies (p99)
regex_p99 = 0.02   # ms
nlp_p99 = 5.73     # ms
budget = 50.0      # ms x402 target

nlp_p99 < budget  # True: 5.73 < 50.0
```
❌ **Refuted**: NLP overhead well within budget  
🎯 **Implication**: No performance justification for sacrificing PERSON detection

## Effect Sizes & Confidence Intervals
```mermaid
graph LR
    subgraph EffectSizes["Key Effect Sizes (95% CI)"]
        E1["PERSON recall delta:<br/>+0.551 [0.512, 0.589]"]
        E2["Micro-F1 delta (NLP-regex):<br/>+0.125 [0.108, 0.142]"]
        E3["Latency delta (NLP-regex):<br/>+5.71ms [5.63, 5.79]"]
    end
```

All effects statistically significant (p < 0.001, bootstrap test)

## Practical Significance Assessment
| Metric | Statistical Sig. | Practical Impact | Recommendation |
|--------|-----------------|-----------------|---------------|
| PERSON recall +55pp | ✅ Yes | High (GDPR compliance) | Use NLP mode |
| Micro-F1 +12.5pp | ✅ Yes | Medium-High | Use all 6 entities |
| Latency +5.71ms | ✅ Yes | Low (within budget) | Accept overhead |
| PHONE recall +22pp | ✅ Yes | Low-Medium | Include PHONE type |

> 💡 **Conclusion**: Statistical and practical significance align—recommended configuration (NLP, min_score=0.4, all entities) is both empirically optimal and operationally feasible.
