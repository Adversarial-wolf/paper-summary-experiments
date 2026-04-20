#!/usr/bin/env python3
"""
Fetch paper metadata from arXiv and generate summary templates
"""

import os
import re
import time
import requests
import feedparser
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime


class ArXivFetcher:
    """Fetch and process arXiv metadata for papers"""
    
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'DiffusionLLM-KG/1.0 (research tool)'
        })
    
    def extract_arxiv_id(self, url: str) -> Optional[str]:
        """Extract arXiv ID from URL"""
        patterns = [
            r'arxiv\.org/abs/(\d+\.\d+)',
            r'arxiv\.org/pdf/(\d+\.\d+)',
            r'arxiv\.org/abs/(\d{4}\.\d{5})',
            r'arxiv\.org/pdf/(\d{4}\.\d{5})',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def fetch_arxiv_metadata(self, arxiv_id: str) -> Optional[Dict]:
        """Fetch metadata from arXiv API"""
        try:
            url = f'http://export.arxiv.org/api/query?id_list={arxiv_id}'
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            
            feed = feedparser.parse(response.content)
            
            if not feed.entries:
                return None
            
            entry = feed.entries[0]
            authors = [author.name for author in entry.authors]
            categories = [tag.term for tag in entry.tags]
            abstract = re.sub(r'<[^>]+>', '', entry.summary)
            abstract = re.sub(r'\s+', ' ', abstract).strip()
            published = datetime.strptime(entry.published, '%Y-%m-%dT%H:%M:%SZ')
            
            return {
                'arxiv_id': arxiv_id,
                'title': entry.title,
                'authors': authors,
                'abstract': abstract,
                'published': published.strftime('%Y-%m-%d'),
                'categories': categories,
                'pdf_url': f'https://arxiv.org/pdf/{arxiv_id}.pdf',
                'abstract_url': f'https://arxiv.org/abs/{arxiv_id}'
            }
        
        except Exception as e:
            print(f"⚠️ Error fetching {arxiv_id}: {e}")
            return None
    
    def generate_summary_template(self, metadata: Dict, existing_content: str = "") -> str:
        """Generate enhanced summary template with fetched metadata"""
        existing_notes = re.search(r'## 📝 Notes\n(.+?)(?=## |$)', existing_content, re.DOTALL)
        existing_notes = existing_notes.group(1).strip() if existing_notes else ""
        authors_str = ' and '.join(metadata['authors'])
        year = metadata['published'].split('-')[0]
        
        return f"""# {metadata['title']}

> **📅 Published:** {metadata['published']} | **🔗 arXiv:** [{metadata['arxiv_id']}](https://arxiv.org/abs/{metadata['arxiv_id']}) | **📄 PDF:** [Download]({metadata['pdf_url']})

## 👥 Authors
{', '.join(metadata['authors'])}

## 📖 Abstract
{metadata['abstract']}

## 🏷️ Categories
{', '.join(metadata['categories'])}

## 🔬 Core Methodology
- 
- 
- 

## 📊 Experiments & Results
- Dataset: 
- Metrics: 
- Results: 

## 💡 Key Insights
- 
- 
- 

## 🔗 Related Work
- 

## 📝 Notes
{existing_notes if existing_notes else "*(Add your personal notes here)*"}

## 📚 Citation
```bibtex
@article{{{metadata['arxiv_id'].replace('.', '_')}},
  title={{{metadata['title']}}},
  author={{{authors_str}}},
  journal={{arXiv preprint arXiv:{metadata['arxiv_id']}}},
  year={{{year}}}
}}
```

---
#diffusion-llm #arxiv-{metadata['arxiv_id'].replace('.', '-')}
"""
    
    def update_all_papers(self, delay: float = 3.0):
        """Update all papers with arXiv metadata"""
        print("🔄 Fetching arXiv metadata for all papers...")
        updated_count = 0
        error_count = 0
        skipped_count = 0
        
        for md_file in self.vault_path.rglob("*.md"):
            if md_file.name.startswith(".") or md_file.name.endswith("-Index.md"):
                continue
            
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            url_match = re.search(r'🔗 Link:\s*\[Paper\]\(([^)]+)\)', content)
            if not url_match:
                skipped_count += 1
                continue
            
            url = url_match.group(1)
            arxiv_id = self.extract_arxiv_id(url)
            
            if not arxiv_id:
                skipped_count += 1
                continue
            
            print(f"📄 Processing: {arxiv_id} ({md_file.name})")
            metadata = self.fetch_arxiv_metadata(arxiv_id)
            
            if not metadata:
                error_count += 1
                continue
            
            new_content = self.generate_summary_template(metadata, content)
            
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            updated_count += 1
            print(f"  ✅ Updated with metadata")
            time.sleep(delay)
        
        print(f"\n✅ Update Complete!")
        print(f"  📝 Updated: {updated_count} papers")
        print(f"  ⚠️ Errors: {error_count} papers")
        print(f"  ⏭️ Skipped: {skipped_count} papers")


def main():
    import sys
    vault_path = sys.argv[1] if len(sys.argv) > 1 else "Diffusion-LLM-Knowledge-Graph"
    fetcher = ArXivFetcher(vault_path)
    
    if len(sys.argv) > 2:
        fetcher.update_single_paper(sys.argv[2])
    else:
        fetcher.update_all_papers()


if __name__ == "__main__":
    main()
