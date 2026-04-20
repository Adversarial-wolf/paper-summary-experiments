
---

## 2️⃣ **Graph Visualization Export (Graphviz/Neo4j)**

### 📜 Python Script: `export_graph.py`

```python
#!/usr/bin/env python3
"""
Export Diffusion-LLM Knowledge Graph to Graphviz and Neo4j formats
"""

import os
import json
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

class GraphExporter:
    def __init__(self, vault_path: str):
        self.vault_path = Path(vault_path)
        self.nodes = {}
        self.edges = []
        self.categories = set()
        
    def parse_markdown_files(self):
        """Parse all markdown files to extract metadata and links"""
        print("📄 Parsing markdown files...")
        
        for md_file in self.vault_path.rglob("*.md"):
            if md_file.name.startswith("."):
                continue
                
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract metadata
            node_id = md_file.stem
            node_data = {
                'id': node_id,
                'path': str(md_file.relative_to(self.vault_path)),
                'label': self._extract_title(content),
                'date': self._extract_date(content),
                'category': self._extract_category(content),
                'url': self._extract_url(content),
                'tags': self._extract_tags(content)
            }
            
            self.nodes[node_id] = node_data
            
            if node_data['category']:
                self.categories.add(node_data['category'])
            
            # Extract wikilinks
            links = re.findall(r'\[\[([^\]]+)\]\]', content)
            for link in links:
                # Clean link (remove aliases)
                clean_link = link.split('|')[0].strip()
                if clean_link != node_id:
                    self.edges.append({
                        'source': node_id,
                        'target': clean_link,
                        'type': 'reference'
                    })
        
        print(f"✅ Parsed {len(self.nodes)} nodes and {len(self.edges)} edges")
    
    def _extract_title(self, content: str) -> str:
        """Extract title from markdown"""
        match = re.search(r'^#\s+(.+)$', content, re.MULTILINE)
        return match.group(1).strip() if match else "Unknown"
    
    def _extract_date(self, content: str) -> str:
        """Extract date from metadata"""
        match = re.search(r'📅 Date:\s*(\d{4}-\d{2}-\d{2})', content)
        return match.group(1) if match else ""
    
    def _extract_category(self, content: str) -> str:
        """Extract category from metadata"""
        match = re.search(r'📂 Category:\s*\[\[([^\]]+)\]\]', content)
        return match.group(1) if match else ""
    
    def _extract_url(self, content: str) -> str:
        """Extract paper URL"""
        match = re.search(r'🔗 Link:\s*\[Paper\]\(([^)]+)\)', content)
        return match.group(1) if match else ""
    
    def _extract_tags(self, content: str) -> List[str]:
        """Extract hashtags"""
        return re.findall(r'#([\w-]+)', content)
    
    def export_graphviz(self, output_file: str = "diffusion_llm_graph.dot"):
        """Export to Graphviz DOT format"""
        print("🎨 Generating Graphviz format...")
        
        dot_content = ['digraph DiffusionLLM {']
        dot_content.append('  rankdir=TB;')
        dot_content.append('  node [shape=box, style=rounded, fontname="Arial"];')
        dot_content.append('  edge [fontname="Arial", fontsize=8];')
        dot_content.append('')
        
        # Color scheme for categories
        category_colors = {
            'Theoretical-Basis': '#FF6B6B',
            'Foundation-Model': '#4ECDC4',
            'Multimodal-Understanding': '#45B7D1',
            'Fast-Sampling': '#96CEB4',
            'Reinforcement-Learning': '#FFEAA7',
            'Long-Context': '#DDA0DD',
            'Variable-Length': '#98D8C8',
            'Others': '#F7DC6F'
        }
        
        # Add nodes
        for node_id, data in self.nodes.items():
            label = data['label'].replace('"', '\\"')
            color = category_colors.get(data['category'], '#D5DBDB')
            
            attrs = [
                f'label="{label}"',
                f'color="{color}"',
                f'style="filled,rounded"',
                f'fillcolor="{color}20"',  # 20% opacity
                f'tooltip="{data.get("url", "")}"'
            ]
            
            if data['date']:
                attrs.append(f'date="{data["date"]}"')
            
            dot_content.append(f'  "{node_id}" [{", ".join(attrs)}];')
        
        dot_content.append('')
        
        # Add edges
        for edge in self.edges:
            dot_content.append(f'  "{edge["source"]}" -> "{edge["target"]}" [color="#85929E"];')
        
        dot_content.append('}')
        
        output_path = self.vault_path / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(dot_content))
        
        print(f"✅ Graphviz file saved to: {output_path}")
        return output_path
    
    def export_neo4j(self, output_file: str = "diffusion_llm_neo4j.cypher"):
        """Export to Neo4j Cypher format"""
        print("🗄️ Generating Neo4j Cypher format...")
        
        cypher_commands = []
        
        # Create constraints
        cypher_commands.append("// Create constraints")
        cypher_commands.append("CREATE CONSTRAINT paper_id IF NOT EXISTS FOR (p:Paper) REQUIRE p.id IS UNIQUE;")
        cypher_commands.append("CREATE CONSTRAINT category_name IF NOT EXISTS FOR (c:Category) REQUIRE c.name IS UNIQUE;")
        cypher_commands.append("")
        
        # Create category nodes
        cypher_commands.append("// Create Category nodes")
        for category in self.categories:
            safe_name = category.replace('-', ' ')
            cypher_commands.append(
                f'MERGE (c:Category {{name: "{category}"}}) '
                f'SET c.displayName = "{safe_name}";'
            )
        cypher_commands.append("")
        
        # Create paper nodes
        cypher_commands.append("// Create Paper nodes")
        for node_id, data in self.nodes.items():
            props = [
                f'id: "{node_id}"',
                f'title: "{data["label"].replace(chr(34), "\\'")}"',
            ]
            
            if data['date']:
                props.append(f'date: date("{data["date"]}")')
            if data['url']:
                props.append(f'url: "{data["url"]}"')
            if data['category']:
                props.append(f'category: "{data["category"]}"')
            if data['tags']:
                tags_str = ', '.join([f'"{t}"' for t in data['tags']])
                props.append(f'tags: [{tags_str}]')
            
            props_str = ', '.join(props)
            cypher_commands.append(f'CREATE (p:Paper {{{props_str}}});')
        
        cypher_commands.append("")
        
        # Create relationships
        cypher_commands.append("// Create relationships")
        cypher_commands.append("// Paper -> Category")
        for node_id, data in self.nodes.items():
            if data['category']:
                cypher_commands.append(
                    f'MATCH (p:Paper {{id: "{node_id}"}}), (c:Category {{name: "{data["category"]}"}}) '
                    f'CREATE (p)-[:BELONGS_TO]->(c);'
                )
        
        cypher_commands.append("")
        cypher_commands.append("// Paper -> Paper (references)")
        for edge in self.edges:
            cypher_commands.append(
                f'MATCH (source:Paper {{id: "{edge["source"]}"}}), '
                f'(target:Paper {{id: "{edge["target"]}"}}) '
                f'CREATE (source)-[:REFERENCES]->(target);'
            )
        
        output_path = self.vault_path / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(cypher_commands))
        
        print(f"✅ Neo4j Cypher file saved to: {output_path}")
        return output_path
    
    def export_json(self, output_file: str = "diffusion_llm_graph.json"):
        """Export to JSON format for D3.js or other visualizations"""
        print("📦 Generating JSON format...")
        
        graph_data = {
            'nodes': [],
            'links': [],
            'metadata': {
                'total_nodes': len(self.nodes),
                'total_edges': len(self.edges),
                'categories': list(self.categories),
                'generated_at': str(Path.now())
            }
        }
        
        # Add nodes
        for node_id, data in self.nodes.items():
            graph_data['nodes'].append({
                'id': node_id,
                'label': data['label'],
                'category': data['category'],
                'date': data['date'],
                'url': data['url'],
                'tags': data['tags'],
                'group': list(self.categories).index(data['category']) if data['category'] else 0
            })
        
        # Add edges
        for edge in self.edges:
            graph_data['links'].append({
                'source': edge['source'],
                'target': edge['target'],
                'type': edge['type']
            })
        
        output_path = self.vault_path / output_file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(graph_data, f, indent=2, ensure_ascii=False)
        
        print(f"✅ JSON file saved to: {output_path}")
        return output_path
    
    def generate_all(self):
        """Generate all export formats"""
        self.parse_markdown_files()
        
        exports = {
            'graphviz': self.export_graphviz,
            'neo4j': self.export_neo4j,
            'json': self.export_json
        }
        
        results = {}
        for format_name, export_func in exports.items():
            try:
                results[format_name] = export_func()
            except Exception as e:
                print(f"❌ Error exporting {format_name}: {e}")
                results[format_name] = None
        
        return results


if __name__ == "__main__":
    import sys
    
    vault_path = sys.argv[1] if len(sys.argv) > 1 else "Diffusion-LLM-Knowledge-Graph"
    
    exporter = GraphExporter(vault_path)
    results = exporter.generate_all()
    
    print("\n" + "="*60)
    print("📊 Export Summary:")
    for format_name, path in results.items():
        if path:
            print(f"  ✅ {format_name.upper()}: {path}")
    print("="*60)