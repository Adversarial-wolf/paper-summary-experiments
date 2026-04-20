# SaTML 2026 Accepted Papers - Complete Summary

## Overview
The SaTML 2026 conference accepted a diverse set of papers addressing critical security, privacy, and robustness challenges in machine learning systems. This summary provides an integrated view of the research landscape across multiple domains.

## Research Themes

### 1. AI Fingerprinting and Attribution Security
- **Smudged Fingerprints**: Systematic evaluation of AI image fingerprint robustness under adversarial conditions, revealing significant vulnerabilities in current techniques.

### 2. Privacy and Membership Inference Attacks
- **Time Series Privacy**: Demonstrated strong vulnerability of time series forecasting models to membership inference attacks, with user-level attacks achieving perfect detection.
- **FedSpy-LLM**: Scalable data reconstruction attacks from gradients in federated LLMs, showing that PEFT methods don't provide sufficient protection.
- **DP Forest Reconstruction**: Investigation into differential privacy effectiveness in classical machine learning models.

### 3. LLM Security and Safety
- **RobustRAG**: First defense framework providing certifiable robustness against retrieval corruption attacks in RAG systems.
- **Defeating Prompt Injections**: CaMeL framework that creates protective system layers against prompt injection attacks in agentic systems.
- **Targeting Alignment**: Demonstration that aligned LLMs have extractable safety classifiers, making them vulnerable to jailbreak attacks.

### 4. Model Robustness and Verification
- **Optimal Robust Recourse**: Provably optimal robust recourse with Lp-bounded model change for addressing model updates.
- **Cascading Robustness**: Methods for verifying robustness in complex model architectures.

### 5. Federated Learning Security
- **FedSpy-LLM**: Data reconstruction from gradients in federated LLMs.
- **Contribution Fragility**: Vulnerabilities in federated learning contribution evaluation mechanisms.

### 6. Model Unlearning and Privacy
- **Deep Unlearning**: Comprehensive fact removal that prevents both direct fact deletion and logical deduction.
- **Exact Unlearning**: SIFT-Masks for large-scale exact unlearning via model merging.
- **Oblivious ERT Unlearning**: Encrypted exact unlearning techniques.

### 7. Physical and Systems Security
- **Kraken**: EM side-channel attacks demonstrating model weight theft from distances up to 100 cm.

### 8. Fairness and Explainability
- **Fair Graph Neural Networks**: Homophily-aware fair GNNs with improved contrastive augmentation.
- **DeepLeak**: Privacy-enhancing hardening of model explanations.

### 9. Efficiency and Optimization
- **Efficient DP-SGD**: Scalable differentially private deep learning without computational shortcuts.
- **StriaNet**: Fast secure inference using Homomorphic Encryption architectures.

## Multi-Stakeholder Impact

### Data Scientists
Researchers and practitioners working on:
- Security techniques and attack methods
- Model robustness and privacy-preserving approaches  
- Implementation of security frameworks
- Performance evaluation and benchmarking

### Compliance Officers
Regulatory and compliance professionals focused on:
- GDPR, AI Act, and other privacy regulations
- Privacy budget and differential privacy implementation
- Security certification and audit readiness
- Data governance and protection standards

### Executives
Leaders and decision-makers concerned with:
- Business risk assessment and mitigation
- Strategic investment in AI security
- Competitive positioning in AI markets
- Organizational readiness for AI deployment

## Key Takeaways

1. **Security Vulnerabilities Are Widespread**: Across multiple ML domains, significant security gaps have been identified that threaten privacy and data integrity.

2. **Privacy in Federated Systems**: Federated learning systems, even with PEFT methods, remain vulnerable to data reconstruction attacks.

3. **LLM Safety Concerns**: Even aligned LLMs can be compromised through targeted classifier extraction techniques.

4. **Physical Security Matters**: Traditional network-centric security thinking is insufficient - physical side-channel attacks pose real threats.

5. **Scalability of Security Approaches**: Efficient approaches for privacy-preserving ML are possible but require careful implementation.

6. **Need for New Paradigms**: Current approaches need to evolve to address the complexity of modern ML systems.

## Research Directions

The accepted papers point to several promising research areas:
- Development of robust, certifiable security frameworks
- Improved privacy-preserving techniques for ML systems
- Better understanding of model vulnerabilities across different architectures
- Integration of security into ML system design from the ground up
- Cross-domain security analysis and transfer of techniques

## Conclusion
SaTML 2026 has provided a critical assessment of security and privacy challenges in modern ML systems. The research demonstrates both the vulnerabilities in current approaches and promising paths forward for developing more robust, secure, and privacy-preserving AI technologies.