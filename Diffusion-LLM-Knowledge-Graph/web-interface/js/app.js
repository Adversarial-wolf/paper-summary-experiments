class KnowledgeGraphApp {
    constructor() {
        this.data = null;
        this.init();
    }

    async init() {
        await this.loadData();
        this.render();
    }

    async loadData() {
        try {
            const response = await fetch('data/knowledge-graph.json');
            this.data = await response.json();
        } catch (error) {
            console.error('Failed to load data:', error);
        }
    }

    render() {
        const grid = document.getElementById('papers-grid');
        grid.innerHTML = this.data.papers.map(paper => `
            <div class="paper-card">
                <h3>${paper.title}</h3>
                <div class="meta">
                    <span>📅 ${paper.date}</span>
                    <span>📂 ${paper.category}</span>
                </div>
                <span class="category-tag">${paper.category}</span>
            </div>
        `).join('');
    }
}

const app = new KnowledgeGraphApp();
