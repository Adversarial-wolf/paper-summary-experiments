## 📊 Dynamic Paper Tables

### All Papers by Date
```dataview
TABLE date as "Date", category as "Category", file.link as "Paper"
FROM #diffusion-llm
WHERE date
SORT date DESC
```

### Papers by Category 
TABLE date as "Date", file.link as "Paper"
FROM #diffusion-llm
WHERE category = "Foundation-Model"
SORT date DESC

### Recent Papers (Last 30 Days)
TABLE date as "Date", category as "Category"
FROM #diffusion-llm
WHERE date >= (date(now) - dur(30 days))
SORT date DESC

### Papers with Notes
TABLE date as "Date", length(notes) as "Notes Length"
FROM #diffusion-llm
WHERE notes AND length(notes) > 0
SORT length(notes) DESC

### Papers by Tag
TABLE date as "Date", category as "Category"
FROM #diffusion-llm
WHERE contains(tags, "#reinforcement-learning")
SORT date DESC

