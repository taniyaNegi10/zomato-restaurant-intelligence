# Zomato Restaurant Intelligence

An end-to-end data analytics and machine learning project that analyzes restaurant data, segments restaurants using K-Means clustering, and evaluates customer reviews using sentiment analysis.

## Project Overview

Zomato Restaurant Intelligence transforms restaurant metadata and customer reviews into meaningful business insights.

The project combines:
- Exploratory Data Analysis (EDA)
- Data Cleaning and Feature Engineering
- K-Means Clustering
- Customer Review Sentiment Analysis using VADER
- Interactive Streamlit Analytics Dashboard

## Project Objectives

1. Understand restaurant characteristics through exploratory data analysis.
2. Identify restaurant segments based on cost, cuisine diversity, and collection count.
3. Analyze customer opinions from restaurant reviews.
4. Generate actionable business insights using data visualization and machine learning.
5. Present findings through an interactive dashboard.

## Dataset Description

The project uses two datasets:

### 1. Restaurant Metadata
- **Records:** 105 restaurants
- **Features:** Restaurant Name, Cost, Collections, Cuisines, and Timings.
- **Purpose:** Used for restaurant analysis and K-Means clustering.

### 2. Restaurant Customer Reviews
- **Records:** 10,000 customer reviews
- **Features:** Restaurant, Reviewer, Review, Rating, Metadata, Time, and Pictures.
- **Purpose:** Used for text preprocessing and sentiment analysis.

## Technologies Used

| Category | Tools |
|---|---|
| Programming Language | Python |
| Data Manipulation | Pandas, NumPy |
| Data Visualization | Matplotlib, Seaborn, Plotly |
| Machine Learning | Scikit-learn |
| Clustering Algorithm | K-Means |
| Feature Scaling | StandardScaler |
| Dimensionality Reduction | PCA |
| Sentiment Analysis | VADER |
| Dashboard | Streamlit |
| Model Persistence | Joblib |
| Development | Jupyter Notebook, VS Code |

## Project Methodology

### 1. Data Preprocessing
- Handled missing and duplicate records.
- Converted restaurant cost into numeric format.
- Cleaned customer review text.
- Preserved important negation words such as "not", "no", and "never".

### 2. Feature Engineering
Created three clustering features:
- Cost
- Cuisine Count
- Collection Count

### 3. Restaurant Clustering
- Applied StandardScaler for feature normalization.
- Used the Elbow Method and Silhouette Score to compare cluster configurations.
- Selected K-Means with 5 clusters.
- Used PCA to visualize the clusters in two dimensions.

### 4. Sentiment Analysis
Applied VADER to calculate positive, negative, neutral, and compound sentiment scores for customer reviews.

Reviews were classified using VADER compound-score thresholds:
- Positive: Compound score ≥ 0.05
- Negative: Compound score ≤ -0.05
- Neutral: Compound score between -0.05 and 0.05

## Model Evaluation

The final K-Means model was evaluated using three clustering metrics.

| Evaluation Metric | Result |
|---|---:|
| Silhouette Score | 0.345 |
| Davies-Bouldin Index | 0.9947 |
| Calinski-Harabasz Score | 59.89 |

### Evaluation Interpretation

- **Silhouette Score (0.345):** Indicates moderate separation between restaurant clusters.
- **Davies-Bouldin Index (0.9947):** Provides a measure of cluster similarity; lower values are preferable.
- **Calinski-Harabasz Score (59.89):** Measures the relationship between between-cluster and within-cluster dispersion.

These results suggest that the model provides useful exploratory restaurant segmentation, although some cluster overlap may remain.

## Key Business Insights

The analysis generated the following findings:

- **105 restaurants** were analyzed.
- Average restaurant cost was approximately **₹861**.
- The largest cluster contained **39 restaurants (Cluster 1)**.
- Cluster 0 had the highest average cost of approximately **₹1,510**.
- VADER classified approximately **75.3% of cleaned reviews as positive**.
- The Indi Grill had a **100% positive sentiment percentage across 100 reviews**.

### Restaurant Segmentation

The five clusters were interpreted using their average cost, cuisine count, and collection count:

| Cluster | Restaurants | Average Cost | Interpretation |
|---|---:|---:|---|
| 0 | 20 | ₹1,510 | Premium, diversified |
| 1 | 39 | ₹654 | Mid-range, diverse |
| 2 | 7 | ₹1,400 | Premium, collection-rich |
| 3 | 29 | ₹431 | Budget-focused |
| 4 | 10 | ₹1,245 | Premium, focused-menu |

Note: Cluster labels are descriptive interpretations, not restaurant quality rankings. Sentiment percentages are based on VADER predictions, not manually verified sentiment labels.

## Interactive Dashboard Features

The project includes a Streamlit dashboard with five analytical sections:

1. **Overview:** Displays key performance indicators and an overall project summary.
2. **Restaurant Analytics:** Explores restaurant costs, cuisines, collections, and other characteristics.
3. **Customer Sentiment:** Visualizes positive, negative, and neutral review classifications.
4. **Restaurant Clustering:** Presents K-Means cluster distributions and restaurant segmentation.
5. **Business Insights:** Highlights important findings to support data-driven decisions.

## Project Structure

```text
zomato-restaurant-intelligence/
│
├── app.py
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── 01_data_understanding.ipynb
│
├── src/
│   ├── __init__.py
│   ├── data_preprocessing.py
│   ├── clustering.py
│   ├── sentiment_analysis.py
│   └── visualizations.py
│
├── models/
├── outputs/
│   └── charts/
│
├── assets/
├── README.md
├── pyproject.toml
└── uv.lock
```

## How to Run the Project

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd zomato-restaurant-intelligence
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Run the Streamlit dashboard

```bash
uv run streamlit run app.py
```

The dashboard will open in your browser, usually at:

```text
http://localhost:8501
```

## Future Improvements

- Improve cluster separation through feature experimentation.
- Perform manual validation of sentiment predictions.
- Explore more advanced NLP-based sentiment models.
- Add restaurant recommendation capabilities.
- Deploy the dashboard for public access.

## Conclusion

Zomato Restaurant Intelligence demonstrates how data analytics, unsupervised machine learning, and sentiment analysis can be combined to understand restaurant markets and customer opinions.

The project provides an interactive platform for exploring restaurant segments, analyzing customer feedback, and extracting business insights.