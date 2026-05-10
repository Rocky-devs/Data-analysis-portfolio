# NYC Business Intelligence Dashboard

Interactive dashboard analyzing 300 businesses across 5 industries in New York City.

**[Live Demo →](https://data-analysis-portfolio-81dm.onrender.com)**

## Overview
Built with Plotly Dash, this dashboard allows users to filter by industry and explore business distribution, rating patterns, and review volume across NYC.

## Features
- Interactive map with business locations colored by industry
- Rating distribution boxplot by industry
- Reviews vs Rating scatter plot (log scale)
- Key insights panel summarizing findings

## Key Findings
- Restaurants dominate review volume (100–5,000+) but show the most stable ratings (4.3–4.6)
- Real estate and dental clinics show the widest rating variance
- Gyms cluster tightly around 4.0–4.5 with lower review counts
- High review count does not guarantee high rating

## Data Source
Google Maps Places API — self-collected via Python (300 businesses, 5 industries: auto repair, dental clinic, gym, real estate, restaurant)

## Tech Stack
`Python` `Plotly Dash` `pandas`

## Run Locally
```bash
pip install -r requirements.txt
python app.py
```
