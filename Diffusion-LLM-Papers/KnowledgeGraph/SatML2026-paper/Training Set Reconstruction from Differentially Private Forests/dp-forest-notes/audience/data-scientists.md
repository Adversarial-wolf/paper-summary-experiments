# 🔬 Guide for Data Scientists & ML Engineers

## ✅ Do This
- Use ε ≤ 1 for sensitive data
- Limit tree depth: d ≤ 3 reduces leakage surface
- Reduce number of trees: |𝒯| ≤ 10 minimizes signal
- Monitor reconstruction risk via statistical CDF testing

## ❌ Avoid This
- Using ε ≥ 5 for PII-containing data
- Deep trees (d ≥ 7) with moderate DP
- Assuming "DP = safe" without empirical validation

## 🛠️ Hyperparameter Selection Guide

| Use Case | Recommended ε | Max Trees | Max Depth | Risk |
|----------|--------------|-----------|-----------|------|
| High-sensitivity PII | 0.1 - 0.5 | ≤ 10 | ≤ 3 | ✅ Low |
| Moderate sensitivity | 1.0 - 2.0 | ≤ 20 | ≤ 5 | ⚠️ Medium |
| Low sensitivity | 5.0 - 10 | ≤ 50 | ≤ 7 | ❌ High |

## 🔍 Validation Protocol (Pseudocode)
```python
def audit_dp_forest_privacy(trained_forest, epsilon):
    # Run reconstruction attack approximation
    reconstructed = constraint_programming_attack(trained_forest, epsilon)
    # Compute alignment-matched error
    error = compute_aligned_error(reconstructed, true_data)
    # Statistical test
    cdf = compute_privacy_leak_cdf(error, random_samples=100)
    return {"risk": "HIGH" if cdf < 0.05 else "SAFE", "cdf": cdf}
```
