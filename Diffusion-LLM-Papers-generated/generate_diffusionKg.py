# 🚀 Complete Diffusion-LLM Knowledge Graph Generator


#!/usr/bin/env python3
"""
Diffusion-LLM Knowledge Graph Generator for Obsidian
Generates complete folder structure, MOC, and individual paper notes with Mermaid diagrams
"""

import os
import re
from datetime import datetime
from typing import Dict, List, Tuple

# ============================================================================
# PAPER DATA (Parsed from Diffusion.md)
# ============================================================================

PAPERS = {
    "Theoretical-Basis": [
        {
            "title": "Deep Unsupervised Learning using Nonequilibrium Thermodynamics",
            "date": "2015-03-12",
            "url": "https://arxiv.org/abs/1503.03585",
            "diagram_type": "thermodynamics"
        },
        {
            "title": "Structured Denoising Diffusion Models in Discrete State-Spaces",
            "date": "2021-07-07",
            "url": "https://arxiv.org/abs/2107.03006",
            "diagram_type": "discrete_diffusion"
        },
        {
            "title": "Discrete Diffusion Modeling by Estimating the Ratios of the Data Distribution",
            "date": "2023-10-25",
            "url": "https://arxiv.org/abs/2310.16834",
            "diagram_type": "ratio_estimation"
        },
        {
            "title": "Your Absorbing Discrete Diffusion Secretly Models the Conditional Distributions of Clean Data",
            "date": "2024-06-06",
            "url": "https://arxiv.org/abs/2406.03736",
            "diagram_type": "absorbing_diffusion"
        },
        {
            "title": "Simplified and Generalized Masked Diffusion for Discrete Data",
            "date": "2024-06-06",
            "url": "https://arxiv.org/abs/2406.04329",
            "diagram_type": "masked_diffusion"
        },
        {
            "title": "Simple and Effective Masked Diffusion Language Models",
            "date": "2024-06-11",
            "url": "https://arxiv.org/abs/2406.07524",
            "diagram_type": "masked_diffusion"
        },
    ],
    "Foundation-Model": [
        {
            "title": "LLaDA: Large Language Diffusion Models",
            "date": "2025-02-14",
            "url": "https://arxiv.org/abs/2502.09992",
            "diagram_type": "foundation"
        },
        {
            "title": "Dream 7B",
            "date": "2025-04-02",
            "url": "https://hkunlp.github.io/blog/2025/dream/",
            "diagram_type": "foundation"
        },
        {
            "title": "Seed Diffusion: A Large-Scale Diffusion Language Model with High-Speed Inference",
            "date": "2025-08-04",
            "url": "https://www.arxiv.org/abs/2508.02193",
            "diagram_type": "foundation"
        },
    ],
    "Multimodal-Understanding": [
        {
            "title": "LLaDA-V: Large Language Diffusion Models with Visual Instruction Tuning",
            "date": "2025-05-22",
            "url": "https://arxiv.org/abs/2505.16933",
            "diagram_type": "multimodal"
        },
        {
            "title": "LaViDa: A Large Diffusion Language Model for Multimodal Understanding",
            "date": "2025-05-22",
            "url": "https://arxiv.org/abs/2505.16839",
            "diagram_type": "multimodal"
        },
        {
            "title": "Dimple: Discrete Diffusion Multimodal Large Language Model with Parallel Decoding",
            "date": "2025-05-22",
            "url": "https://arxiv.org/abs/2505.16990",
            "diagram_type": "multimodal"
        },
    ],
    "Unified-Multimodal-Model": [
        {
            "title": "MMaDA: Multimodal Large Diffusion Language Models",
            "date": "2025-05-21",
            "url": "https://arxiv.org/abs/2505.15809",
            "diagram_type": "multimodal"
        },
    ],
    "Speech-ASR": [
        {
            "title": "Whisfusion: Parallel ASR Decoding via a Diffusion Transformer",
            "date": "2025-08-09",
            "url": "https://arxiv.org/abs/2508.07048",
            "diagram_type": "speech"
        },
    ],
    "Fast-Sampling-KV-Cache": [
        {
            "title": "dKV-Cache: The Cache for Diffusion Language Models",
            "date": "2025-05-21",
            "url": "https://arxiv.org/abs/2505.15781",
            "diagram_type": "kv_cache"
        },
        {
            "title": "dLLM-Cache: Accelerating Diffusion Large Language Models with Adaptive Caching",
            "date": "2025-05-22",
            "url": "https://github.com/maomaocun/dLLM-cache?tab=readme-ov-file",
            "diagram_type": "kv_cache"
        },
        {
            "title": "Accelerating Diffusion Language Model Inference via Efficient KV Caching and Guided Diffusion",
            "date": "2025-05-27",
            "url": "https://arxiv.org/pdf/2505.21467",
            "diagram_type": "kv_cache"
        },
        {
            "title": "Fast-dLLM: Training-free Acceleration of Diffusion LLM by Enabling KV Cache and Parallel Decoding",
            "date": "2025-05-28",
            "url": "https://nvlabs.github.io/Fast-dLLM/paper/fast_dllm.pdf",
            "diagram_type": "kv_cache"
        },
        {
            "title": "Esoteric Language Models",
            "date": "2025-06-02",
            "url": "https://arxiv.org/abs/2506.01928",
            "diagram_type": "kv_cache"
        },
        {
            "title": "Sparse-dLLM: Accelerating Diffusion LLMs with Dynamic Cache Eviction",
            "date": "2025-08-04",
            "url": "https://arxiv.org/abs/2508.02558",
            "diagram_type": "kv_cache"
        },
        {
            "title": "DPad: Efficient Diffusion Language Models with Suffix Dropout",
            "date": "2025-08-19",
            "url": "https://arxiv.org/abs/2508.14148",
            "diagram_type": "kv_cache"
        },
    ],
    "Advanced-Sampling-Method": [
        {
            "title": "Variational Autoencoding Discrete Diffusion with Enhanced Dimensional Correlations Modeling",
            "date": "2025-05-23",
            "url": "https://arxiv.org/abs/2505.17384",
            "diagram_type": "sampling"
        },
        {
            "title": "Accelerated Sampling from Masked Diffusion Models via Entropy Bounded Unmasking",
            "date": "2025-05-30",
            "url": "https://arxiv.org/abs/2505.24857",
            "diagram_type": "sampling"
        },
        {
            "title": "Accelerating Diffusion LLMs via Adaptive Parallel Decoding",
            "date": "2025-05-31",
            "url": "https://arxiv.org/abs/2506.00413",
            "diagram_type": "sampling"
        },
        {
            "title": "Accelerating Diffusion Large Language Models with SlowFast Sampling: The Three Golden Principles",
            "date": "2025-06-12",
            "url": "https://arxiv.org/abs/2506.10848",
            "diagram_type": "sampling"
        },
        {
            "title": "Wide-In, Narrow-Out: Revokable Decoding for Efficient and Effective DLLMs",
            "date": "2025-07-24",
            "url": "https://arxiv.org/abs/2507.18578",
            "diagram_type": "sampling"
        },
    ],
    "Reinforcement-Learning": [
        {
            "title": "d1: Scaling Reasoning in Diffusion Large Language Models via Reinforcement Learning",
            "date": "2025-04-16",
            "url": "https://arxiv.org/abs/2504.12216",
            "diagram_type": "rl"
        },
        {
            "title": "Reinforcing the Diffusion Chain of Lateral Thought with Diffusion Language Models",
            "date": "2025-05-15",
            "url": "https://arxiv.org/abs/2505.10446",
            "diagram_type": "rl"
        },
        {
            "title": "LLaDA 1.5: Variance-Reduced Preference Optimization for Large Language Diffusion Models",
            "date": "2025-05-25",
            "url": "https://arxiv.org/abs/2505.19223",
            "diagram_type": "rl"
        },
        {
            "title": "DiffuCoder: Understanding and Improving Masked Diffusion Models for Code Generation",
            "date": "2025-07-25",
            "url": "https://arxiv.org/abs/2506.20639",
            "diagram_type": "rl"
        },
        {
            "title": "MDPO: Overcoming the Training-Inference Divide of Masked Diffusion Language Models",
            "date": "2025-08-18",
            "url": "https://arxiv.org/pdf/2508.13148",
            "diagram_type": "rl"
        },
        {
            "title": "Revolutionizing Reinforcement Learning Framework for Diffusion Large Language Models",
            "date": "2025-09-08",
            "url": "https://arxiv.org/pdf/2509.06949",
            "diagram_type": "rl"
        },
        {
            "title": "Inpainting-Guided Policy Optimization for Diffusion Large Language Models",
            "date": "2025-09-12",
            "url": "https://arxiv.org/pdf/2509.10396",
            "diagram_type": "rl"
        },
    ],
    "Long-Context": [
        {
            "title": "LongLLaDA: Unlocking Long Context Capabilities in Diffusion LLMs",
            "date": "2025-06-17",
            "url": "https://arxiv.org/abs/2506.14429",
            "diagram_type": "long_context"
        },
    ],
    "Variable-Length": [
        {
            "title": "Edit Flows: Flow Matching with Edit Operations",
            "date": "2025-06-10",
            "url": "https://arxiv.org/abs/2506.09018",
            "diagram_type": "variable_length"
        },
        {
            "title": "DreamOn: Diffusion Language Models For Code Infilling Beyond Fixed-Size Canvas",
            "date": "2025-07-15",
            "url": "https://hkunlp.github.io/blog/2025/dreamon/",
            "diagram_type": "variable_length"
        },
        {
            "title": "Beyond Fixed: Variable-Length Denoising for Diffusion Large Language Models",
            "date": "2025-08-04",
            "url": "https://arxiv.org/abs/2508.00819",
            "diagram_type": "variable_length"
        },
        {
            "title": "Any-Order Flexible Length Masked Diffusion",
            "date": "2025-08-31",
            "url": "https://arxiv.org/pdf/2509.01025",
            "diagram_type": "variable_length"
        },
    ],
    "Others": [
        {
            "title": "Time Is a Feature: Exploiting Temporal Dynamics in Diffusion Language Models",
            "date": "2025-08-12",
            "url": "https://arxiv.org/abs/2508.09138",
            "diagram_type": "temporal"
        },
        {
            "title": "Thinking Inside the Mask: In-Place Prompting in Diffusion LLMs",
            "date": "2025-08-14",
            "url": "https://arxiv.org/pdf/2508.10736",
            "diagram_type": "prompting"
        },
    ],
}

# ============================================================================
# MERMAID DIAGRAM TEMPLATES
# ============================================================================

MERMAID_TEMPLATES = {
    "thermodynamics": """
```mermaid
flowchart LR
    A[x₀: Clean Data] -->|q(x₁|x₀)| B[x₁: Slightly Noisy]
    B -->|... t steps| C[xₜ: Pure Noise]
    C -->|p_θ(xₜ₋₁|xₜ)| D[Reconstructed Data]
    D -->|ELBO Loss| E[Parameter Update θ]
    style A fill:#d4edda,stroke:#28a745
    style C fill:#f8d7da,stroke:#dc3545
    style D fill:#cce5ff,stroke:#007bff
```
""",
    "discrete_diffusion": """
```mermaid
flowchart TD
    A[Discrete State Space] --> B[Forward Diffusion q]
    B --> C[Mask/Corrupt Tokens]
    C --> D[Reverse Process p_θ]
    D --> E[Denoise & Predict]
    style B fill:#fff3cd,stroke:#ffc107
    style D fill:#d1ecf1,stroke:#0c5460
```
""",
    "ratio_estimation": """
```mermaid
flowchart LR
    A[Data Distribution] --> B[Ratio Estimator]
    B --> C[Score Function]
    C --> D[Sampling]
    style B fill:#e2e3e5,stroke:#383d41
```
""",
    "absorbing_diffusion": """
```mermaid
flowchart TD
    A[Clean Data] --> B[Absorbing State]
    B --> C[Conditional Distribution]
    C --> D[Generation]
    style B fill:#f8d7da,stroke:#dc3545
```
""",
    "masked_diffusion": """
```mermaid
flowchart TD
    A[Prompt + MASK] --> B[Denoise Step 1]
    B --> C[Unmask High-Confidence]
    C --> D[Repeat Until Complete]
    D --> E[Final Output]
    style B fill:#fff3cd,stroke:#ffc107
    style D fill:#d4edda,stroke:#28a745
```
""",
    "foundation": """
```mermaid
flowchart TD
    A[Input Prompt] --> B[Transformer Backbone]
    B --> C[Masked Diffusion Head]
    C --> D[Iterative Denoising]
    D --> E[Generated Text]
    style B fill:#cce5ff,stroke:#007bff
    style D fill:#d4edda,stroke:#28a745
```
""",
    "multimodal": """
```mermaid
flowchart LR
    A[Text Input] --> C[Fusion Layer]
    B[Visual Input] --> C
    C --> D[Diffusion Decoder]
    D --> E[Multimodal Output]
    style C fill:#fff3cd,stroke:#ffc107
    style D fill:#d1ecf1,stroke:#0c5460
```
""",
    "speech": """
```mermaid
flowchart LR
    A[Audio Spectrogram] --> B[Diffusion Transformer]
    B --> C[Parallel Decoding]
    C --> D[Text Transcription]
    style B fill:#cce5ff,stroke:#007bff
```
""",
    "kv_cache": """
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
""",
    "sampling": """
```mermaid
flowchart TD
    A[Initial Noise] --> B[Adaptive Sampling]
    B --> C[Parallel Decoding]
    C --> D[Quality Check]
    D --> E[Final Output]
    style B fill:#fff3cd,stroke:#ffc107
    style C fill:#d1ecf1,stroke:#0c5460
```
""",
    "rl": """
```mermaid
flowchart TD
    A[Diffusion Policy π_θ] --> B[Sample Trajectory]
    B --> C[Compute Reward R]
    C --> D[Advantage Estimation]
    D --> E[Policy Gradient Update]
    E --> A
    style B fill:#e2e3e5,stroke:#383d41
    style D fill:#f8d7da,stroke:#dc3545
```
""",
    "long_context": """
```mermaid
flowchart LR
    A[Long Context Input] --> B[Chunked Diffusion]
    B --> C[Attention Window]
    C --> D[Coherent Generation]
    style B fill:#cce5ff,stroke:#007bff
```
""",
    "variable_length": """
```mermaid
flowchart TD
    A[Variable Input] --> B[Dynamic Masking]
    B --> C[Flexible Denoising]
    C --> D[Variable Output]
    style B fill:#fff3cd,stroke:#ffc107
    style C fill:#d4edda,stroke:#28a745
```
""",
    "temporal": """
```mermaid
flowchart LR
    A[Timestep Embedding] --> B[Temporal Attention]
    B --> C[Dynamic Features]
    C --> D[Enhanced Generation]
    style B fill:#cce5ff,stroke:#007bff
```
""",
    "prompting": """
```mermaid
flowchart TD
    A[In-Place Prompt] --> B[Mask Preservation]
    B --> C[Contextual Denoising]
    C --> D[Prompt-Aware Output]
    style B fill:#fff3cd,stroke:#ffc107
    style C fill:#d1ecf1,stroke:#0c5460
```
""",
}

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def sanitize_filename(title: str) -> str:
    """Convert paper title to safe filename"""
    safe = re.sub(r'[^\w\s-]', '', title)
    safe = re.sub(r'[-\s]+', '-', safe)
    return safe.strip('-')

def create_wikilink(title: str) -> str:
    """Create Obsidian wikilink from title"""
    return f"[[{title}]]"

def get_category_papers(category: str, exclude_title: str) -> List[str]:
    """Get 3-5 related papers from same category for linking"""
    papers = []
    for cat, paper_list in PAPERS.items():
        if cat == category or cat.replace('-', ' ') == category.replace('-', ' '):
            for p in paper_list:
                if p["title"] != exclude_title:
                    papers.append(p["title"])
    return papers[:4]

def get_cross_category_links(category: str) -> List[str]:
    """Get papers from related categories"""
    links = []
    category_map = {
        "Foundation-Model": ["Theoretical-Basis", "Fast-Sampling-KV-Cache"],
        "Fast-Sampling-KV-Cache": ["Foundation-Model", "Advanced-Sampling-Method"],
        "Reinforcement-Learning": ["Foundation-Model"],
        "Multimodal-Understanding": ["Foundation-Model"],
        "Advanced-Sampling-Method": ["Fast-Sampling-KV-Cache"],
    }
    for related_cat in category_map.get(category, []):
        if related_cat in PAPERS:
            for p in PAPERS[related_cat][:2]:
                links.append(p["title"])
    return links[:3]

# ============================================================================
# PAPER NOTE TEMPLATE
# ============================================================================

def generate_paper_note(paper: Dict, category: str) -> str:
    """Generate complete markdown note for a paper"""
    title = paper["title"]
    safe_name = sanitize_filename(title)
    diagram = MERMAID_TEMPLATES.get(paper["diagram_type"], MERMAID_TEMPLATES["foundation"])
    
    # Get related papers
    same_category = get_category_papers(category, title)
    cross_category = get_cross_category_links(category)
    
    related_links = ""
    for p in same_category:
        related_links += f"- {create_wikilink(p)}\n"
    for p in cross_category:
        if p not in same_category:
            related_links += f"- {create_wikilink(p)}\n"
    
    # Category wikilink
    category_link = category.replace('-', ' ')
    
    content = f"""# {title}

> **📅 Date:** {paper["date"]} | **🔗 Link:** [Paper]({paper["url"]}) | **📂 Category:** [[{category_link}]]

## 📖 Overview
*(Add summary after reading the paper)*

This paper contributes to the **{category_link}** category of diffusion language models.

## 🔬 Core Methodology
- *(Key technique 1)*
- *(Key technique 2)*
- *(Key innovation)*

{diagram}

## 🔗 Related Papers
{related_links}

## 💡 Key Insights
- *(Takeaway 1)*
- *(Takeaway 2)*
- *(Practical implication)*

## 📝 Notes
*(Add your personal notes here)*

---
#diffusion-llm #{category.lower()} #research-paper
"""
    return content

# ============================================================================
# MOC TEMPLATE
# ============================================================================

def generate_moc() -> str:
    """Generate the main Map of Content file"""
    toc_sections = ""
    
    for category, papers in PAPERS.items():
        category_display = category.replace('-', ' ')
        toc_sections += f"## 📚 {category_display}\n"
        for paper in papers:
            toc_sections += f"- [[{paper['title']}]]\n"
        toc_sections += "\n"
    
    content = f"""# 🌐 Diffusion-LLM Knowledge Graph

> [!summary] Overview
> A curated collection of **{sum(len(p) for p in PAPERS.values())}** diffusion language model papers, organized by theoretical foundations, architecture, acceleration methods, alignment techniques, and advanced capabilities.
> 
> **Last Updated:** {datetime.now().strftime('%Y-%m-%d')}
> **Designed for:** Obsidian with bidirectional linking and Mermaid visualizations

## 📊 Statistics
| Category | Papers |
|----------|--------|
"""
    
    for category, papers in PAPERS.items():
        content += f"| {category.replace('-', ' ')} | {len(papers)} |\n"
    
    content += f"""
**Total:** {sum(len(p) for p in PAPERS.values())} papers

## 🗺️ Table of Contents

{toc_sections}

## 🔍 Quick Navigation
- [[#Theoretical Basis|Theoretical Basis]] - Foundation papers on diffusion theory
- [[#Foundation Model|Foundation Model]] - Large-scale diffusion LLMs
- [[#Multimodal Understanding|Multimodal Understanding]] - Vision-language diffusion models
- [[#Fast Sampling|Fast Sampling]] - KV caching and acceleration
- [[#Reinforcement Learning|Reinforcement Learning]] - RL alignment and reasoning
- [[#Long Context|Long Context]] - Extended context handling
- [[#Variable Length|Variable Length]] - Flexible sequence generation

## 📈 Graph View Tips
1. Enable **Graph View** in Obsidian to see connections
2. Use **Search** (Ctrl/Cmd+O) to find papers by keyword
3. Click any `[[wikilink]]` to navigate between related papers
4. Use **Backlinks** panel to see what references each paper

---
#diffusion-llm #knowledge-graph #obsidian #research
"""
    return content

# ============================================================================
# MAIN GENERATION FUNCTION
# ============================================================================

def generate_all(base_dir: str = "Diffusion-LLM-Knowledge-Graph"):
    """Generate complete knowledge graph structure"""
    
    print(f"🚀 Generating Diffusion-LLM Knowledge Graph in: {base_dir}/")
    print("=" * 60)
    
    # Create base directory
    os.makedirs(base_dir, exist_ok=True)
    
    # Generate MOC
    moc_path = os.path.join(base_dir, "00-Diffusion-LLM-MOC.md")
    with open(moc_path, "w", encoding="utf-8") as f:
        f.write(generate_moc())
    print(f"✅ Created: 00-Diffusion-LLM-MOC.md")
    
    total_papers = 0
    
    # Generate each category and paper
    for category, papers in PAPERS.items():
        category_dir = os.path.join(base_dir, category)
        os.makedirs(category_dir, exist_ok=True)
        
        # Create category index
        category_display = category.replace('-', ' ')
        category_index = f"""# {category_display}

> **📂 Path:** `/{category}/` | **📊 Papers:** {len(papers)}

## 📋 Papers in This Category

"""
        for paper in papers:
            safe_name = sanitize_filename(paper["title"])
            category_index += f"- [[{paper['title']}]]\n"
        
        category_index += f"""
## 🔗 Back to MOC
- [[00-Diffusion-LLM-MOC|🌐 Diffusion-LLM Knowledge Graph]]

---
#diffusion-llm #{category.lower()}
"""
        
        index_path = os.path.join(category_dir, f"{category}-Index.md")
        with open(index_path, "w", encoding="utf-8") as f:
            f.write(category_index)
        
        print(f"📁 Created category: {category}/ ({len(papers)} papers)")
        
        # Generate each paper note
        for paper in papers:
            safe_name = sanitize_filename(paper["title"])
            paper_dir = os.path.join(category_dir, safe_name)
            os.makedirs(paper_dir, exist_ok=True)
            
            note_content = generate_paper_note(paper, category)
            note_path = os.path.join(paper_dir, f"{safe_name}.md")
            
            with open(note_path, "w", encoding="utf-8") as f:
                f.write(note_content)
            
            total_papers += 1
    
    print("=" * 60)
    print(f"✅ Generation Complete!")
    print(f"📊 Total Papers: {total_papers}")
    print(f"📁 Categories: {len(PAPERS)}")
    print(f"📄 Files Created: {total_papers + len(PAPERS) + 1}")
    print(f"📂 Base Directory: {os.path.abspath(base_dir)}/")
    print("=" * 60)
    print("\n🔮 Next Steps:")
    print("1. Open the folder in Obsidian")
    print("2. Enable Mermaid: Settings → Markdown → Mermaid → Enable")
    print("3. View 00-Diffusion-LLM-MOC.md as your entry point")
    print("4. Use Graph View to explore connections")
    print("=" * 60)

# ============================================================================
# RUN
# ============================================================================

if __name__ == "__main__":
    generate_all()
