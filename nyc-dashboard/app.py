import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, Input, Output

# ── 数据 ──────────────────────────────────────────
files = {
    "auto_repair": "New York_auto repair.csv",
    "dental_clinic": "New York_dental clinic.csv",
    "gym": "New York_gym.csv",
    "real_estate": "New York_real estate agency.csv",
    "restaurant": "New York_restaurants.csv",
}

dfs = []
for industry, filename in files.items():
    df_temp = pd.read_csv(filename)
    df_temp["industry"] = industry
    dfs.append(df_temp)

  # 过滤掉没有评分的记录
df = pd.concat(dfs, ignore_index=True)
df["rating"] = df["rating"].fillna(0)
df = df[df["rating"] > 0]
df["reviews"] = df["reviews"].fillna(0)


# ── App ───────────────────────────────────────────
app = Dash(__name__)

app.layout = html.Div([

    html.H1("NYC Business Intelligence Dashboard",
            style={"textAlign": "center", "marginBottom": "20px"}),

    # Dropdown 筛选器
    dcc.Dropdown(
        id="industry-filter",
        options=[{"label": i.replace("_", " ").title(), "value": i}
                 for i in df["industry"].unique()],
        multi=True,
        placeholder="Filter by industry (default: all)...",
        style={"marginBottom": "20px"}
    ),

    # 地图
    dcc.Graph(id="map-scatter"),

    # 箱线图
    dcc.Graph(id="rating-box"),

    # 散点图
    dcc.Graph(id="reviews-scatter"),

    # Key Insights
    html.Div([
        html.H3("Key Insights", style={"marginBottom": "10px"}),
        html.Ul([
            html.Li("Restaurants dominate in review volume (100–5000+), but their ratings are the most stable (4.3–4.6), suggesting established reputation."),
            html.Li("Real estate and dental clinics show the widest rating variance — quality is harder to predict in these categories."),
            html.Li("Gyms cluster tightly around 4.0–4.5 with low review counts, indicating loyal but smaller customer bases."),
            html.Li("High reviews ≠ high rating: several restaurants with 1000+ reviews still sit below 4.0."),
        ])
    ], style={
        "backgroundColor": "#f9f9f9",
        "border": "1px solid #ddd",
        "borderRadius": "8px",
        "padding": "20px",
        "marginTop": "30px"
    }),

], style={"maxWidth": "1200px", "margin": "auto", "padding": "20px", "fontFamily": "Arial"})



# ── Callback ──────────────────────────────────────
@app.callback(
    Output("map-scatter", "figure"),
    Output("rating-box", "figure"),
    Output("reviews-scatter", "figure"),
    Input("industry-filter", "value")
)
def update_charts(selected_industries):
    filtered = df if not selected_industries else df[df["industry"].isin(selected_industries)]

    map_fig = px.scatter_map(
        filtered,
        lat="location_lat", lon="location_lng",
        color="industry",
        size="rating", size_max=8,
        hover_name="name",
        hover_data={"rating": True, "address": True, "reviews": True,
                    "location_lat": False, "location_lng": False},
        zoom=11,
        center={"lat": 40.73, "lon": -73.95},
        height=500,
        title="Business Locations by Industry"
    )
    map_fig.update_layout(map_style="carto-positron")

    box_fig = px.box(
        filtered,
        x="industry", y="rating",
        color="industry",
        points="all",
        height=400,
        title="Rating Distribution by Industry"
    )

    scatter_fig = px.scatter(
        filtered,
        x="reviews", y="rating",
        color="industry",
        hover_name="name",
        hover_data={"address": True},
        size_max=10,
        height=400,
        title="Reviews vs Rating by Industry",
        labels={"reviews": "Number of Reviews", "rating": "Google Rating"}
    )
    scatter_fig.update_layout(xaxis_type="log")  # log scale 因为reviews差距大

    return map_fig, box_fig, scatter_fig


if __name__ == "__main__":
    app.run(debug=True)

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)