# Data Analysis Portfolio
Python-based data analysis and data visualization projects using pandas, Plotly Dash, and Jupyter Notebook.

## Data Sources
- NYC Business Data: Google Maps Places API (self-collected)
- Online Retail: [Kaggle](https://www.kaggle.com/datasets/carrie1/ecommerce-data)
- Netflix Titles: [Kaggle](https://www.kaggle.com/datasets/shivamb/netflix-shows)
- Tokyo Airbnb: [Inside Airbnb](https://insideairbnb.com/get-the-data/)

## Projects

### 🗺️ NYC Business Intelligence Dashboard
Interactive dashboard analyzing 300 businesses across 5 industries in New York City using Google Maps Places API data.
- Built with Plotly Dash — live filters drive all charts simultaneously
- Visualized business density, rating distributions, and review volume on an interactive map
- Key finding: restaurants dominate review volume but show the most stable ratings (4.3–4.6); real estate and dental clinics show the widest quality variance
- - **[Live Demo →](https://data-analysis-portfolio-81dm.onrender.com)**
  - "Live demo may take ~30s to load on first visit (free hosting)"
- Tools: `pandas` `Plotly` `Dash`

---

### 🗾 Tokyo Airbnb Analysis
Analyzed 27,000+ listings to answer: where should backpackers stay in Tokyo?
- Cleaned price data and removed outliers using IQR method
- Compared room types by price and availability
- Identified best-value neighborhoods using a custom value score
- Tools: `pandas` `matplotlib` `Jupyter Notebook`

### 🎬 Netflix Content Analysis
Explored Netflix's content library to understand their programming strategy.
- Analyzed Movie vs TV Show distribution
- Handled multi-value country data using str.split + explode
- Mapped content age ratings to target audience segments
- Tools: `pandas` `matplotlib` `Jupyter Notebook`

### 🛒 E-commerce Order Analysis
Analyzed 500k+ online retail transactions to understand revenue distribution and product performance.
- Cleaned transaction data and converted price/quantity to numeric values
- Calculated revenue and compared revenue contribution by country (excluding UK)
- Analyzed monthly sales trends using pandas datetime tools
- Identified top 10 bestselling products by quantity sold
- Tools: `pandas` `matplotlib` `Jupyter Notebook`

---

## Skills
`Python` `pandas` `Plotly Dash` `Data Cleaning` `Exploratory Data Analysis` `Data Visualization`
