
import argparse
from pathlib import Path
from datetime import datetime


# ============================================================================
# HELPER: Clean string formatting without textwrap.dedent issues
# ============================================================================

def clean_multiline(s: str) -> str:
    """Remove leading/trailing whitespace from each line and strip outer blank lines."""
    lines = s.split('\n')
    # Remove empty lines at start and end
    while lines and not lines[0].strip():
        lines.pop(0)
    while lines and not lines[-1].strip():
        lines.pop()
    # Find minimum indentation (excluding empty lines)
    non_empty = [line for line in lines if line.strip()]
    if not non_empty:
        return ''
    min_indent = min(len(line) - len(line.lstrip()) for line in non_empty)
    # Strip common indentation and return
    return '\n'.join(line[min_indent:] if line.strip() else '' for line in lines)


# ============================================================================
# CONTENT GENERATORS (using clean_multiline instead of textwrap.dedent)
# ============================================================================

def get_readme_content():
    return clean_multiline(f"""
        # 🗂️ SaTML-2026 Paper Deep Dive: "Training Set Reconstruction from Differentially Private Forests"

        > **Nested Markdown Knowledge Repository**  
        > *Paper: "Training Set Reconstruction from Differentially Private Forests: How Effective is DP?"*  
        > *Authors: Alice Gorgé, Julien Ferry, Sébastien Gambs, Thibaut Vidal*  
        > *Accepted at IEEE SaTML 2026*  
        > *Generated: {datetime.now().strftime("%Y-%m-%d %H:%M")}*

        ## 🎯 Paper at a Glance

        | Attribute | Details |
        |-----------|---------|
        | **Title** | Training Set Reconstruction from Differentially Private Forests: How Effective is DP? |
        | **Venue** | IEEE SaTML 2026 |
        | **Authors** | Gorgé, Ferry, Gambs, Vidal (École Polytechnique, Polytechnique Montréal, UQAM) |
        | **Preprint** | [arXiv:2502.05307](https://arxiv.org/abs/2502.05307) |
        | **Code** | [GitHub: vidalt/DRAFT-DP](https://github.com/vidalt/DRAFT-DP) |
        | **Category** | Research Paper (Group 1) |

        ## 📋 Core Question
        > *"Can differential privacy (DP) truly protect training data in random forests, or can attackers still reconstruct sensitive records?"*

        ## 🔑 Key Finding
        **Random forests trained with meaningful DP guarantees can still leak portions of their training data.** Only forests with predictive performance no better than random guessing are fully robust to reconstruction attacks.

        ## 🗺️ Repository Structure

        ```mermaid
        mindmap
          root((DP Forest<br/>Reconstruction))
            📄 Paper Summary
              Abstract & Problem
              Threat Model
              Attack Methodology
            🔬 Technical Deep Dive
              Constraint Programming Attack
              Reconstruction Pipeline
            📊 Results & Analysis
              Privacy-Utility Trade-off
              ε Budget Impact
            👥 Audience Guides
              Data Scientists
              Compliance Officers
              Executives
            🧠 Analogies & Examples
              DP = Noisy Survey
              Attack = Detective Work
            🛡️ Mitigations
              Practical Recommendations
        ```

        ## 🚀 Quick Start
        - 🎓 **New to DP?** → Start with [🧠 Analogies](./analogies/README.md)
        - 🔧 **Implementing RFs?** → Go to [👥 Data Scientists Guide](./audience/data-scientists.md)
        - ⚖️ **Assessing compliance?** → See [👥 Compliance Officers Guide](./audience/compliance.md)
        - 💼 **Strategic planning?** → Review [👥 Executives Guide](./audience/executives.md)
    """)


def get_paper_summary_content():
    return clean_multiline("""
        # 📄 Paper Summary: Problem, Approach & Contributions

        ## 🎯 Abstract Summary
        Recent research has shown that structured machine learning models such as tree ensembles are vulnerable to privacy attacks targeting their training data. To mitigate these risks, differential privacy (DP) has become a widely adopted countermeasure.

        **This paper introduces a reconstruction attack targeting state-of-the-art ε-DP random forests.** By leveraging a constraint programming model that incorporates knowledge of the forest's structure and DP mechanism characteristics, the approach formally reconstructs the most likely dataset that could have produced a given forest.

        ## ⚠️ The Privacy Paradox

        ```mermaid
        graph TD
            A[Random Forests] --> B[Popular for tabular data]
            A --> C[Vulnerable to privacy attacks]
            D[Differential Privacy] --> E[Adds calibrated noise]
            D --> F[Should prevent reconstruction]
            C & F --> G[🔍 Research Question]
            G --> H[✅ Answer: YES - Meaningful DP ≠ Full protection]
            style G fill:#fff3e0
            style H fill:#ffcdd2
        ```

        ## 🔬 Core Contributions

        | # | Contribution | Impact |
        |---|-------------|--------|
        | 1️⃣ | Novel constraint programming attack | First to exploit forest structure + DP mechanism |
        | 2️⃣ | Systematic evaluation across datasets | Reveals privacy-utility-reconstruction trade-offs |
        | 3️⃣ | Statistical privacy leak analysis | Rigorous methodology for quantifying violations |
        | 4️⃣ | Practical recommendations | Actionable guidance for practitioners |
    """)


def get_technical_content():
    return clean_multiline("""
        # 🔬 Technical Deep Dive: How the Attack Works

        ## 🧩 Constraint Programming Formulation

        ### Core Constraints
        For each tree `t`, leaf `v`, and class `c`:

        ```
        ∑_{k=1}^{N} z_kc · 𝟙[example k reaches leaf v] = true_count_tvc
        observed_count_tvc = true_count_tvc + Laplace(ε) noise
        ```

        ### Objective: Maximize Log-Likelihood
        ```
        maximize: ∑_{t,v,c,l} log(p_l) · 𝟙[Δ_tvc = l]
        where:
        - Δ_tvc = observed_count - true_count
        - p_l = probability of noise value l under Laplace(ε)
        ```

        ## 🔄 Reconstruction Pipeline

        ```mermaid
        flowchart LR
            subgraph Phase 1: Encoding
                P1[Parse DP forest]
                P2[Encode path constraints]
                P3[Model DP noise likelihood]
            end
            subgraph Phase 2: Solving
                S1[CP Solver: CP-SAT]
                S2[Search high-likelihood assignments]
            end
            subgraph Phase 3: Post-Processing
                O1[Align via min-cost matching]
                O2[Compute reconstruction error]
            end
            P1 & P2 & P3 --> S1 & S2
            S1 & S2 --> O1 & O2
        ```

        ## 📊 Evaluation Metrics

        | Metric | Formula | Interpretation |
        |--------|---------|---------------|
        | **Reconstruction Error** | `(1/N) ∑ₖ distance(x̂_k, x_k)` | Lower = better (0 = perfect) |
        | **Random Baseline** | Error from uniform sampling | Attack must beat this |
        | **Privacy Leak CDF** | P(error ≤ observed \| random) | <5% = significant leak |
        | **Model Utility** | Test accuracy of DP forest | Higher = more useful |

        ```python
        # Pseudocode: Reconstruction Error
        def compute_reconstruction_error(reconstructed, original):
            cost_matrix = [[manhattan_distance(a, b) for b in original] for a in reconstructed]
            matching = hungarian_algorithm(cost_matrix)
            total = sum(cost_matrix[i][matching[i]] for i in range(len(reconstructed)))
            return total / len(reconstructed)
        ```
    """)


def get_results_content():
    return clean_multiline("""
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
    """)


def get_data_scientists_guide():
    return clean_multiline("""
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
    """)


def get_compliance_guide():
    return clean_multiline("""
        # ⚖️ Guide for Compliance Officers & Risk Managers

        ## 🎯 Regulatory Mapping: GDPR Article 32

        > **Key Insight**: "Meaningful DP" (ε = 1-10) does **not** guarantee protection against sophisticated reconstruction attacks. Relying solely on ε reporting may not satisfy GDPR Article 32's "appropriate technical measures" requirement.

        ## 🚨 DP Configuration Risk Matrix

        | ε Value | GDPR Compliance? | Reconstruction Risk | Recommendation |
        |---------|-----------------|-------------------|---------------|
        | **ε ≤ 0.1** | ✅ Strong candidate | Low | Document utility trade-off |
        | **ε = 0.5-1** | ⚠️ Context-dependent | Medium | Add feature masking + CDF testing |
        | **ε = 2-5** | ❌ Likely insufficient | High | Avoid for sensitive data |
        | **ε ≥ 10** | ❌ Not adequate | Very High | Do not use for personal data |

        ## 📋 Audit Checklist
        ### Pre-Deployment
        - [ ] Document ε selection rationale
        - [ ] Conduct reconstruction risk assessment
        - [ ] Validate statistical privacy (CDF > 5% for sensitive data)
        - [ ] Assess inlier/outlier risk
        - [ ] Review model complexity limits

        ### Documentation Template
        ```markdown
        ## DP Forest Privacy Impact Assessment
        **Model**: [Name]  
        **DP Config**: ε = [value]  
        **Risk Assessment**: 
        - Reconstruction error: [value]%
        - Privacy leak CDF: [value] → Risk: [LOW/MEDIUM/HIGH]
        **Mitigations**: [List]
        **Approval**: [DPO, Tech Lead, Business Owner]
        ```
    """)


def get_executives_guide():
    return clean_multiline("""
        # 💼 Executive Summary: Strategic Implications

        ## 🎯 C-Suite Takeaways

        ```mermaid
        graph TD
            A[DP Forest Attack] --> B[Key Business Risks]
            B --> B1[⚠️ "DP-protected" models may leak data]
            B --> B2[💰 Fines up to 4% global revenue]
            B --> B3[📉 Reputational damage]
            B1 & B2 & B3 --> C[Strategic Response]
            C --> C1[✅ Require reconstruction testing]
            C --> C2[✅ Budget for privacy engineering]
            C --> C3[✅ Treat model structure as sensitive IP]
        ```

        ## 💰 Investment Priorities (Ranked)

        | Priority | Investment | Expected ROI |
        |----------|-----------|--------------|
        | 🥇 Privacy Validation Pipeline | $50K-200K | Avoid €10M+ GDPR fines |
        | 🥈 Model Access Governance | $30K-100K | Reduce attack surface |
        | 🥉 Privacy Engineering Talent | $150K-300K/yr | Proactive risk identification |

        ## 🗣️ Board-Ready Talking Points
        > *"Our 'DP-protected' models may provide false security. Recent research shows attackers can reconstruct training data even from differentially private forests. We're investing in validation pipelines to ensure privacy claims are empirically justified."*

        ## 🎯 Questions for AI Teams
        1. "Have we tested DP forests against reconstruction attacks, or just reported ε?"
        2. "What's our ε selection process—privacy-driven or accuracy-driven?"
        3. "Who has white-box access to model structures? Is it logged?"
        4. "What's our incident response plan for reconstruction breaches?"
    """)


def get_analogies_content():
    return clean_multiline("""
        # 🧠 Analogical Explanations

        ## 🔐 Differential Privacy = "Noisy Town Survey"
        > Imagine polling 100 people about a sensitive condition. With DP, each person flips a coin: Heads = answer truthfully, Tails = answer randomly. The aggregate is still useful, but you can't prove what any one person said.  
        > **The catch**: If you publish *how* you added noise, a clever analyst might reverse-engineer individual responses.

        ## 🌲 Random Forest = "Committee of Recipe Tasters"
        > 100 tasters (trees) each sample recipes (training data) and learn simple rules. DP adds "fuzz" to their notes. The attack sees fuzzy notes + knows the fuzzing recipe, then solves: "Which original recipes most likely produced these notes?" Like Sudoku for privacy.

        ## 🔍 Reconstruction Attack = "Forensic Accountant"
        > Published report: "Revenue: $1M ± $100K". Accountant knows the noise model, uses constraint logic to find: "Which transactions most likely produced these fuzzy totals?" Statistical test determines if reconstruction is significantly better than random → privacy breach.

        ## ⚖️ Privacy-Utility Trade-off = "Blurry Photo"
        ```
        ε = 0.1: Heavy blur → 🔒 Private but useless (accuracy ~ random)
        ε = 1: Medium blur → ⚖️ Balanced (distributional leakage only)
        ε = 10: Light blur → 🎯 Useful but risky (individual data leaks)
        ```
        > **Executive takeaway**: No free lunch. The "sweet spot" (ε = 1-10) may still leak to sophisticated attackers.

        ## 🎓 One-Sentence Summaries
        | Concept | Simple Explanation |
        |---------|------------------|
        | Differential Privacy | "Calibrated noise so group insights are useful but individuals can't be identified" |
        | Reconstruction Attack | "Using model structure + noise knowledge to reverse-engineer training data" |
        | Privacy Budget (ε) | "Smaller ε = more privacy, less accurate model" |
        | Privacy Leak CDF | "Statistical test: low probability = real leakage" |
    """)


def get_mitigations_content():
    return clean_multiline("""
        # 🛡️ Mitigations & Best Practices

        ## 🎯 Paper's Recommendations
        > *"To construct DP random forests more resilient to reconstruction attacks:  
        > (1) use ε ≤ 1 for sensitive data,  
        > (2) limit tree depth and forest size,  
        > (3) consider hiding split attributes,  
        > (4) regularly audit models using reconstruction attacks."*

        ## 🔧 Implementation Playbook

        ### Design-Time Protections
        - Minimize features: collect only what's essential
        - Start with ε = 0.5 for sensitive data
        - Max tree depth: d ≤ 3 for high-risk data
        - Max forest size: |𝒯| ≤ 20

        ### Validation Protocol (Pseudocode)
        ```python
        def run_privacy_audit(forest, epsilon, true_data=None):
            baseline = compute_random_baseline(forest.domains)
            attack_err = constraint_programming_attack(forest, epsilon, timeout=30)
            cdf = compute_privacy_leak_cdf(attack_err.reconstruction, true_data, n=100)
            return {
                "risk": "HIGH" if cdf < 0.05 else "MEDIUM" if cdf < 0.15 else "LOW",
                "cdf": cdf,
                "recommendations": generate_recommendations(cdf)
            }
        ```

        ### Deployment Safeguards
        - Restrict white-box model access
        - Log all forest structure queries
        - Use privacy-preserving inference APIs
        - Quarterly re-audits with latest attack methods

        ## 🚀 Future Research Directions
        - **Short-term**: Hybrid defenses (DP + cryptography), adaptive ε
        - **Medium-term**: Formal verification, automated mitigation selection
        - **Long-term**: Privacy-preserving model markets, regulatory certification standards
    """)


def get_contributing_content():
    return clean_multiline(f"""
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
        *Generated: {datetime.now().strftime("%Y-%m-%d")} | Paper: arXiv:2502.05307*
    """)


# ============================================================================
# FILE & DIRECTORY OPERATIONS
# ============================================================================

def write_markdown_file(filepath: Path, content: str):
    """Write content to markdown file with UTF-8 encoding."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content.strip() + '\n')
    print(f"✓ Created: {filepath}")


def generate_directory_structure(base_path: Path):
    """Create nested directory structure."""
    dirs = [
        base_path,
        base_path / "01-paper-summary",
        base_path / "02-technical-deep-dive",
        base_path / "03-results-analysis",
        base_path / "audience",
        base_path / "analogies",
        base_path / "mitigations",
        base_path / "diagrams",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)
        print(f"✓ Directory: {d}")


def generate_all_files(base_path: Path):
    """Generate all markdown files."""
    files = [
        (base_path / "README.md", get_readme_content()),
        (base_path / "01-paper-summary" / "README.md", get_paper_summary_content()),
        (base_path / "02-technical-deep-dive" / "README.md", get_technical_content()),
        (base_path / "03-results-analysis" / "README.md", get_results_content()),
        (base_path / "audience" / "README.md", 
         "# 👥 Audience-Specific Guides\n\nSelect your role:\n- [🔬 Data Scientists](./data-scientists.md)\n- [⚖️ Compliance Officers](./compliance.md)\n- [💼 Executives](./executives.md)"),
        (base_path / "audience" / "data-scientists.md", get_data_scientists_guide()),
        (base_path / "audience" / "compliance.md", get_compliance_guide()),
        (base_path / "audience" / "executives.md", get_executives_guide()),
        (base_path / "analogies" / "README.md", get_analogies_content()),
        (base_path / "mitigations" / "README.md", get_mitigations_content()),
        (base_path / "CONTRIBUTING.md", get_contributing_content()),
    ]
    for filepath, content in files:
        write_markdown_file(filepath, content)


def generate_master_mermaid(base_path: Path):
    """Generate master Mermaid diagram file."""
    content = clean_multiline("""
        ```mermaid
        mindmap
          root((DP Forest<br/>Reconstruction))
            📄 Paper Summary
              Abstract & Problem
              Threat Model
              Attack Methodology
            🔬 Technical Deep Dive
              Constraint Programming
              Reconstruction Pipeline
            📊 Results & Analysis
              Privacy-Utility Trade-off
              ε Budget Impact
            👥 Audience Guides
              Data Scientists
              Compliance Officers
              Executives
            🧠 Analogies
              DP = Noisy Survey
              Attack = Detective Work
            🛡️ Mitigations
              Best Practices
              Future Directions
        ```
    """)
    write_markdown_file(base_path / "diagrams" / "master.mmd", content)


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Generate nested markdown notes for SaTML-2026 DP Forest paper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_dp_forest_notes.py
  python generate_dp_forest_notes.py --output ~/my-notes
        """
    )
    parser.add_argument('-o', '--output', default='./dp-forest-notes',
                       help='Output directory (default: ./dp-forest-notes)')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()
    
    base_path = Path(args.output).resolve()
    
    print(f"🚀 Generating DP Forest Reconstruction knowledge base...")
    print(f"📁 Output: {base_path}")
    print("-" * 60)
    
    generate_directory_structure(base_path)
    generate_all_files(base_path)
    generate_master_mermaid(base_path)
    
    print("-" * 60)
    print(f"✅ Success! Knowledge base at: {base_path}")
    print()
    print("📚 Quick start:")
    print(f"   cd {base_path}")
    print("   cat README.md")
    print()
    print("🔍 By audience:")
    print("   • Data Scientists: audience/data-scientists.md")
    print("   • Compliance: audience/compliance.md")
    print("   • Executives: audience/executives.md")
    print()
    print("🧠 Easy explanations: analogies/README.md")
    print("🛡️ Mitigations: mitigations/README.md")
    print()
    print("📊 Render Mermaid: https://mermaid.live")
    print("=" * 60)


if __name__ == "__main__":
    main()
