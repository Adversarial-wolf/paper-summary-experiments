# SaTML 2026 Papers Collection

This repository contains a comprehensive collection of papers accepted to the SaTML 2026 conference, with deep dive documentation and visual representations.

## Project Structure

```
arxiv-papers/
├── papers/                 # Individual paper documents with deep dive analysis
├── scripts/                # Automation scripts
├── papers_metadata.json    # Metadata of fetched papers
└── README.md               # This file
```

## Contents

This collection includes:

1. **Three foundational papers** with comprehensive deep dive documentation:
   - Smudged Fingerprints: A Systematic Evaluation of the Robustness of AI Image Fingerprints
   - Privacy Risks in Time Series Forecasting: User- and Record-Level Membership Inference
   - Certifiably Robust RAG against Retrieval Corruption

2. **Documentation components** for each paper:
   - Comprehensive technical overview
   - Key findings and insights  
   - Methodology breakdown
   - Mermaid diagrams illustrating approaches
   - Multi-stakeholder perspectives (Data Scientists, Compliance Officers, Executives)

3. **Automated tools**:
   - Script to fetch papers from arXiv
   - Script to generate paper documentation
   - Extensible template for new papers

## Features

### Deep Dive Analysis
Each paper includes:
- Complete technical summary with methodology
- Key findings with practical implications
- Visual mermaid diagrams showing research approaches
- Tailored perspectives for different stakeholder groups

### Multi-Stakeholder Approach
- **Data Scientists**: Technical methodologies, algorithms, and experimental results
- **Compliance Officers**: Privacy mechanisms, regulatory considerations, and compliance frameworks  
- **Executives**: Business risk evaluation, strategic implications, and ROI considerations

### Visual Representations
- Mermaid diagrams for systematic understanding of methodologies
- Visual flowcharts showing attack/defense approaches
- Architecture diagrams for system designs

## Usage

1. **View Existing Papers**: Navigate to `/papers/` to see deep dive documentation
2. **Fetch New Papers**: Run `python3 scripts/fetch_saml2026_papers.py` to get additional papers
3. **Generate Documentation**: Run `python3 scripts/generate_paper_docs.py` to create new documents
4. **Extend Collection**: Add new papers using the established template format

## How to Add New Papers

1. **Using the fetch script**:
   ```
   python3 scripts/fetch_saml2026_papers.py
   ```

2. **Manual addition**:
   - Follow the existing markdown template in `/papers/`
   - Include the mermaid diagram for methodology
   - Provide the three stakeholder perspectives

## Research Focus Areas

The collected papers represent key research areas in AI security and privacy:
- AI fingerprinting robustness in adversarial settings
- Privacy risks in time series forecasting and membership inference
- RAG system security and robustness
- Model privacy techniques including differential privacy
- Physical security threats to ML systems
- Compliance frameworks for AI systems

## Future Development

This collection is designed to be extensible:
- Add more papers from the full conference proceedings
- Incorporate automated diagram generation
- Enhance stakeholder analysis with domain-specific insights
- Create search and filtering capabilities
- Implement continuous update mechanisms

## Acknowledgements

This collection represents the current state of SaTML 2026 research and provides a foundation for understanding the security and privacy challenges in modern machine learning systems.

*Last updated: April 2026*