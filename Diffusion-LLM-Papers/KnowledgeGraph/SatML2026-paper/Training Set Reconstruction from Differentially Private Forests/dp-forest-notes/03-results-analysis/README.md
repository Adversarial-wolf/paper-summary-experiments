# 📊 Results & Analysis

## 📈 Main Result: Privacy-Utility-Reconstruction Trade-off

```mermaid
xychart-beta
    title "Reconstruction Error vs. Privacy Budget (ε)"
    x-axis "Privacy Budget ε" [0.1, 1, 5, 10, 30]
    y-axis "Reconstruction Error (%)" 0 --> 25
    line "UCI Adult" [15.2, 13.1, 12.3, 10.8, 8.5]
    line "COMPAS" [8.9, 6.2, 5.7, 4.9, 3.9]
    line "Random Baseline" [16.7, 16.7, 16.7, 16.7, 16.7]
```

> **Key Observation**: For ε ≥ 5, reconstruction error drops below random baseline → **meaningful privacy leakage**.

## 🔍 Statistical Privacy Leak Analysis

| Dataset | ε=0.1 | ε=1 | ε=5 | ε=10 | ε=30 |
|---------|-------|-----|-----|------|------|
| UCI Adult | ❌ 45% | ❌ 18% | ✅ 3% | ✅ 1% | ✅ <1% |
| COMPAS | ❌ 52% | ❌ 22% | ✅ 4% | ✅ 2% | ✅ <1% |

> **Interpretation**: CDF ≤ 5% indicates individual-specific information is leaking.

## ⚖️ The Utility Cliff

```mermaid
quadrantChart
    title "Model Utility vs. Reconstruction Robustness"
    x-axis "Reconstruction Robustness" Low --> High
    y-axis "Model Utility" Low --> High
    "ε = 0.1": [0.9, 0.3]
    "ε = 1": [0.6, 0.65]
    "ε = 5": [0.3, 0.78]
    "ε = 10": [0.2, 0.82]
    "No DP": [0.05, 0.87]
```

> **Critical Finding**: No "sweet spot" where DP forests are both useful AND fully private against this attack.
