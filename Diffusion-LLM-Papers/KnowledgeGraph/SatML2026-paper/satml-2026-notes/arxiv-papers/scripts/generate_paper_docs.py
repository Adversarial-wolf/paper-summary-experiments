#!/usr/bin/env python3
"""
Script to generate deep dive documentation for SaTML 2026 papers with mermaid diagrams
"""

import os
import json
from datetime import datetime

# Sample paper data based on what we already know from the repository
SAMPLE_PAPERS = [
    {
        "title": "Smudged Fingerprints: A Systematic Evaluation of the Robustness of AI Image Fingerprints",
        "authors": ["Kai Yao", "Marc Juarez"],
        "institution": "University of Edinburgh",
        "abstract": "Model fingerprint detection techniques have emerged as a promising approach for attributing AI-generated images to their source models, with high detection accuracy in clean settings. Yet, their robustness under adversarial conditions remains largely unexplored. We present the first systematic security evaluation of these techniques, formalizing threat models that encompass both white- and black-box access and two attack goals: fingerprint removal, which erases identifying traces to evade attribution, and fingerprint forgery, which seeks to cause misattribution to a target model.",
        "category": "AI Fingerprinting & Attribution Security",
        "arxiv_id": "2512.11771",
        "key_findings": [
            "Fingerprint removal attacks are highly effective (success rates above 80% in white-box settings)",
            "Fingerprint forgery is more challenging but its success varies across targeted models",
            "Found utility-robustness trade-off in fingerprinting methods"
        ],
        "methodology": [
            "Implemented five attack strategies",
            "Evaluated 14 representative fingerprinting methods",
            "Tested across RGB, frequency, and learned-feature domains",
            "Used 8 state-of-the-art image generators"
        ]
    },
    {
        "title": "Privacy Risks in Time Series Forecasting: User- and Record-Level Membership Inference",
        "authors": ["Nicolas Johansson", "Tobias Olsson", "Daniel Nilsson", "Johan Östman", "Fazeleh Hoseini"],
        "institution": "Chalmers University of Technology, AI Sweden",
        "abstract": "Membership inference attacks (MIAs) aim to determine whether specific data were used to train a model. While extensively studied on classification models, their impact on time series forecasting remains largely unexplored. We address this gap by introducing two new attacks: (i) an adaptation of multivariate LiRA, a state-of-the-art MIA originally developed for classification models, to the time-series forecasting setting, and (ii) a novel end-to-end learning approach called Deep Time Series (DTS) attack.",
        "category": "Privacy Attacks & Membership Inference",
        "arxiv_id": "2502.05307",
        "key_findings": [
            "Forecasting models are vulnerable to membership inference attacks",
            "User-level attacks often achieve perfect detection",
            "Vulnerability increases with longer prediction horizons and smaller training populations"
        ],
        "methodology": [
            "Benchmarked attacks on TUH-EEG and ELD datasets",
            "Targeted LSTM and N-HiTS forecasting architectures",
            "Evaluated under both record- and user-level threat models"
        ]
    },
    {
        "title": "Certifiably Robust RAG against Retrieval Corruption",
        "authors": ["Chong Xiang", "Tong Wu", "Zexuan Zhong", "David Wagner", "Danqi Chen", "Prateek Mittal"],
        "institution": "NVIDIA, Princeton University, University of California, Berkeley",
        "abstract": "Retrieval-augmented generation (RAG) is susceptible to retrieval corruption attacks, where malicious passages injected into retrieval results can lead to inaccurate model responses. We propose RobustRAG, the first defense framework with certifiable robustness against retrieval corruption attacks.",
        "category": "LLM Security & Safety",
        "arxiv_id": "2601.21287",
        "key_findings": [
            "Introduced first defense framework with certifiable robustness against retrieval corruption",
            "Used isolate-then-aggregate strategy for secure aggregation",
            "Achieved certifiable robustness with non-trivial lower bounds on response quality",
            "Demonstrated effectiveness across multiple datasets and LLMs"
        ],
        "methodology": [
            "Developed isolate-then-aggregate approach",
            "Designed keyword-based and decoding-based algorithms for secure aggregation",
            "Evaluated on open-domain question-answering and free-form text generation tasks",
            "Tested across three datasets and three LLMs"
        ]
    }
]

def create_paper_document(paper_data):
    """Create a markdown document for a paper with deep dive analysis and mermaid diagram"""
    
    title = paper_data["title"]
    filename = title.replace(":", "").replace("/", " ").replace("\\", " ").replace("?", " ").replace("*", " ").replace("\"", " ").replace("<", " ").replace(">", " ").replace("|", " ").replace(".", " ").strip().replace(" ", "_") + ".md"
    
    content = f"""# {title}

## Paper Overview
{paper_data["abstract"]}

## Technical Details
- **Authors**: {", ".join(paper_data["authors"])}
- **Institution**: {paper_data["institution"]}
- **Category**: {paper_data["category"]}
- **ArXiv ID**: {paper_data["arxiv_id"]}

## Key Findings
"""
    
    for i, finding in enumerate(paper_data["key_findings"], 1):
        content += f"{i}. {finding}\n\n"
    
    content += """## Methodology
"""
    
    for i, method in enumerate(paper_data["methodology"], 1):
        content += f"{i}. {method}\n\n"
    
    content += """## Mermaid Diagram
```mermaid
graph TD
    A[Retrieval Corruption Attack] --> B[Malicious Passages Injected]
    B --> C[Inaccurate Model Responses]
    C --> D[Certifiable Robustness]
    D --> E[Secure Aggregation]
    E --> F[Accurate Responses]
    
    subgraph "RobustRAG Framework"
        A --> B
        B --> C
        C --> D 
        D --> E
        E --> F
    end
```

## Multi-Stakeholder Perspectives

### Data Scientists
- **Technical Approach**: Isolate-then-aggregate strategy for robust RAG defense
- **Novel Methodology**: Secure aggregation using keyword-based and decoding-based algorithms  
- **Evaluation**: Tested across multiple datasets and LLM architectures
- **Performance**: Achieved certifiable robustness with non-trivial lower bounds

### Compliance Officers
- **Privacy Considerations**: Addresses data integrity in retrieval-augmented systems
- **Security Risk**: Protects against malicious data injection in LLM systems
- **Regulatory Impact**: Provides certifiable robustness framework for compliance requirements
- **Data Protection**: Mitigates risks that could violate privacy regulations

### Executives
- **Business Risk**: Reduces threats to LLM performance and reputation
- **ROI**: Provides robust security framework that can be integrated with existing systems
- **Competitive Advantage**: Advanced security capabilities for LLM deployments
- **Governance**: Certifiable frameworks provide audit-ready security measures

## Key Takeaways
1. **Security Framework**: First defense framework with certifiable robustness against retrieval corruption attacks
2. **Technical Innovation**: Isolate-then-aggregate strategy for secure aggregation  
3. **Practical Implementation**: Demonstrated effectiveness across multiple datasets and LLMs
4. **Compliance Ready**: Provides certifiable robustness suitable for regulatory environments

## Research Implications
- The framework establishes a new baseline for robustness in RAG systems
- Opens opportunities for further work in certifiable security frameworks
- Highlights the importance of addressing retrieval corruption attacks in production LLM systems
- Demonstrates that robust security can be achieved while maintaining model utility
"""

    return content, filename

def generate_all_documents():
    """Generate documentation for all sample papers"""
    print("Generating paper documents...")
    
    for i, paper in enumerate(SAMPLE_PAPERS):
        try:
            content, filename = create_paper_document(paper)
            
            # Write to file
            filepath = os.path.join("arxiv-papers", "papers", filename)
            with open(filepath, 'w') as f:
                f.write(content)
            
            print(f"✓ Created: {filename}")
            
        except Exception as e:
            print(f"✗ Error creating document for {paper['title']}: {e}")

if __name__ == "__main__":
    generate_all_documents()
    print("\nCompleted generating paper documentation!")