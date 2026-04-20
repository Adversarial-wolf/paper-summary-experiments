# 🌐 Diffusion-LLM Knowledge Graph

A comprehensive knowledge graph of **40** Diffusion Language Model papers, designed for Obsidian with web interface support.

## 📁 Structure

```
Diffusion-LLM-Knowledge-Graph/
├── 00-Diffusion-LLM-MOC.md          # Main entry point
├── Theoretical-Basis/               # Theory papers
├── Foundation-Model/                # Foundation models
├── Multimodal-Understanding/        # Multimodal papers
├── Fast-Sampling-KV-Cache/         # Acceleration methods
├── Reinforcement-Learning/         # RL alignment
├── scripts/                         # Automation scripts
├── web-interface/                   # Web browser
└── requirements.txt                 # Python dependencies
```

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Open in Obsidian
- Open `Diffusion-LLM-Knowledge-Graph/` folder as Obsidian vault
- Enable Mermaid: Settings → Markdown → Mermaid → Enable
- Start with `00-Diffusion-LLM-MOC.md`

### 3. Fetch arXiv Metadata (Optional)
```bash
python scripts/fetch_arxiv_metadata.py Diffusion-LLM-Knowledge-Graph
```

### 4. Launch Web Interface (Optional)
```bash
python scripts/generate_web_data.py Diffusion-LLM-Knowledge-Graph web-interface/data/knowledge-graph.json
cd web-interface
python -m http.server 8000
# Open http://localhost:8000
```

## 📊 Categories

| Category | Papers |
|----------|--------|
| Theoretical Basis | 6 |
| Foundation Model | 3 |
| Multimodal Understanding | 3 |
| Unified Multimodal Model | 1 |
| Speech ASR | 1 |
| Fast Sampling KV Cache | 7 |
| Advanced Sampling Method | 5 |
| Reinforcement Learning | 7 |
| Long Context | 1 |
| Variable Length | 4 |
| Others | 2 |

**Total:** 40 papers

## 🛠️ Scripts

| Script | Purpose |
|--------|---------|
| `fetch_arxiv_metadata.py` | Auto-fetch paper metadata from arXiv |
| `incremental_update.py` | Detect and add new papers |
| `export_graph.py` | Export to Graphviz/Neo4j |
| `generate_web_data.py` | Generate web interface data |

## 📄 License

MIT License - Feel free to use and contribute!

## 🤝 Contributing

1. Fork the repository
2. Add new papers to `Diffusion.md`
3. Run `python generate_complete_kg.py` to regenerate
4. Submit a pull request

---
**Last Updated:** 2026-04-20
