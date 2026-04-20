# Using the DP Forest Reconstruction Knowledge Base

## 🔍 Finding Information
1. **New to topic?** → [🧠 Analogies](./analogies/README.md)
2. **Implementing?** → [🔬 Data Scientists](./audience/data-scientists.md)
3. **Compliance?** → [⚖️ Compliance](./audience/compliance.md)
4. **Strategy?** → [💼 Executives](./audience/executives.md)

## 🔄 Updating Content
- Paper updates: Review arXiv diff and update summaries
- New mitigations: Add evidence-based recommendations to mitigations/README.md
- Feedback: Refine "One-Sentence Summaries" based on stakeholder input

## 🎯 Recommended Workflows
### Technical Teams
```bash
git clone https://github.com/vidalt/DRAFT-DP
cd DRAFT-DP
python run_reconstruction_attack.py --epsilon 5 --dataset adult
python audit_privacy.py --model-path ./my_forest.pkl --epsilon 1.0
```

### Compliance Reviews
1. Fill out Privacy Impact Assessment Template
2. Run statistical privacy leak test (CDF calculation)
3. Document risk acceptance or mitigation plan

## 📬 Contributions
This is a living document. To contribute:
1. Fork repository
2. Add content to appropriate section
3. Include Mermaid diagrams for visual clarity
4. Cite sources (arXiv, SaTML, GDPR)
5. Submit PR with clear description

> **License**: CC-BY-SA 4.0 for content, MIT for code examples. Verify regulatory guidance with legal counsel.
*Generated: 2026-04-20 | Paper: arXiv:2502.05307*
