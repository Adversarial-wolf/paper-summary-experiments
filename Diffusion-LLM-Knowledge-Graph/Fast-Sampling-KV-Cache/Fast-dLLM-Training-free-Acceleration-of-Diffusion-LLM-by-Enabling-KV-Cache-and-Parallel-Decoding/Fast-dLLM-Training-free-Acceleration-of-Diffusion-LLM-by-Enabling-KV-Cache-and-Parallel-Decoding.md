# Fast-dLLM: Training-free Acceleration of Diffusion LLM by Enabling KV Cache and Parallel Decoding

> **📅 Date:** 2025-05-28 | **🔗 Link:** [Paper](https://nvlabs.github.io/Fast-dLLM/paper/fast_dllm.pdf) | **📂 Category:** [[Fast Sampling KV Cache]]

## 📖 Overview
*(Add summary after reading the paper)*

This paper contributes to the **Fast Sampling KV Cache** category of diffusion language models.

## 🔬 Core Methodology
- *(Key technique 1)*
- *(Key technique 2)*
- *(Key innovation)*

```mermaid
flowchart LR
    A[Step t-1 KV] --> B[Step t: Diffuse]
    B --> C{Confidence > τ?}
    C -->|Yes| D[Cache KV]
    C -->|No| E[Recompute]
    D --> F[Accelerated Inference]
    style D fill:#d4edda,stroke:#28a745
    style E fill:#f8d7da,stroke:#dc3545
```

## 🔗 Related Papers
*(Add related papers using [[title]])*
- 

## 💡 Key Insights
- *(Takeaway 1)*
- *(Takeaway 2)*
- *(Practical implication)*

## 📝 Notes
*(Add your personal notes here)*

---
#diffusion-llm #fast-sampling-kv-cache #research-paper
