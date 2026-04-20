#!/usr/bin/env python3
"""
Script to fetch papers from arXiv for SaTML 2026 conference
"""

import arxiv
import os
import json
import time
from datetime import datetime

def fetch_saml2026_papers():
    """
    Fetch papers related to SaTML 2026 from arXiv
    """
    # Search for papers related to SaTML 2026
    search_terms = [
        'SaTML 2026',
        'IEEE SaTML 2026',
        'satml 2026',
        'Security and Privacy in Machine Learning 2026'
    ]
    
    papers = []
    
    # Try different search approaches
    for term in search_terms:
        try:
            search = arxiv.Search(
                query=term,
                max_results=10,
                sort_by=arxiv.SortCriterion.Relevance
            )
            
            print(f"Searching for papers with query: {term}")
            
            for result in search.results():
                # Check if this is a SaTML paper based on title/abstract
                if any(keyword in result.title.lower() for keyword in ['satml', 'security', 'privacy', 'ai security', 'ml security']):
                    paper_info = {
                        'title': result.title,
                        'authors': [author.name for author in result.authors],
                        'abstract': result.summary,
                        'arxiv_id': result.get_short_id(),
                        'primary_category': result.primary_category,
                        'categories': result.categories,
                        'submitted': result.published.isoformat() if result.published else None,
                        'url': result.entry_id,
                        'comments': result.comment
                    }
                    papers.append(paper_info)
                    print(f"Found: {result.title}")
            
            # Be respectful to the API
            time.sleep(1)
            
        except Exception as e:
            print(f"Error searching with term '{term}': {e}")
            continue
    
    return papers

def save_paper_metadata(papers):
    """Save paper metadata to JSON file"""
    if not papers:
        print("No papers to save")
        return
    
    output_file = os.path.join("arxiv-papers", "papers_metadata.json")
    
    with open(output_file, 'w') as f:
        json.dump(papers, f, indent=2, default=str)
    
    print(f"Saved metadata for {len(papers)} papers to {output_file}")

def main():
    """Main function to fetch and save SaTML 2026 papers"""
    print("Starting SaTML 2026 paper fetching...")
    
    # Create output directory if it doesn't exist
    os.makedirs("arxiv-papers", exist_ok=True)
    
    papers = fetch_saml2026_papers()
    
    if papers:
        save_paper_metadata(papers)
        print(f"Successfully fetched {len(papers)} papers")
    else:
        print("No papers found with current search criteria")

if __name__ == "__main__":
    main()