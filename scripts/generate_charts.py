import duckdb
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

DB_PATH = 'warehouse/imdb.duckdb'
OUTPUT_DIR = 'visualizations'

# Create output directory
os.makedirs(OUTPUT_DIR, exist_ok=True)
sns.set_theme(style="whitegrid")

con = duckdb.connect(DB_PATH)

print("Generating charts...")

# ==========================================
# CHART 1: Top 10 Directors (Bar Chart)
# ==========================================
query1 = """
SELECT
    p.primary_name AS director_name,
    ROUND(AVG(f.average_rating), 2) AS avg_director_rating
FROM fct_title_ratings f
JOIN bridge_title_crew b ON f.title_id = b.title_id
JOIN dim_person p ON b.name_id = p.name_id
JOIN stg_title_basics stg ON f.title_id = stg.title_id
WHERE b.role = 'director' AND stg.title_type = 'movie'
GROUP BY p.primary_name
HAVING COUNT(f.title_id) >= 5 AND SUM(f.num_votes) >= 500000
ORDER BY avg_director_rating DESC
LIMIT 10
"""
df1 = con.execute(query1).df()

plt.figure(figsize=(10, 6))
barplot = sns.barplot(x='avg_director_rating', y='director_name', data=df1, palette='viridis')
plt.title('Top 10 Hollywood Directors by Average Rating\n(Min. 5 movies & 500k votes)', fontsize=14, fontweight='bold')
plt.xlabel('Average Rating (1-10)')
plt.ylabel('')
plt.xlim(7.5, 9.5)

# Add values directly on the bars
for p in barplot.patches:
    width = p.get_width()
    plt.text(width + 0.05, p.get_y() + p.get_height()/2. + 0.1, '{:1.2f}'.format(width), ha="center")

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/top_10_directors.png', dpi=300)
plt.close()


# ==========================================
# CHART 1B: Top 10 Directors - Raw/Original (Bar Chart)
# ==========================================
query1_raw = """
SELECT
    p.primary_name AS director_name,
    ROUND(AVG(f.average_rating), 2) AS avg_director_rating
FROM fct_title_ratings f
JOIN bridge_title_crew b ON f.title_id = b.title_id
JOIN dim_person p ON b.name_id = p.name_id
WHERE b.role = 'director'
GROUP BY p.primary_name
HAVING COUNT(f.title_id) >= 5 AND SUM(f.num_votes) >= 1000
ORDER BY avg_director_rating DESC
LIMIT 10
"""
df1_raw = con.execute(query1_raw).df()

plt.figure(figsize=(10, 6))
barplot_raw = sns.barplot(x='avg_director_rating', y='director_name', data=df1_raw, palette='magma')
plt.title('Top 10 Directors - Raw Data / Low Vote Threshold\n(Min. 5 titles & 1k votes - Showing Data Skew)', fontsize=14, fontweight='bold')
plt.xlabel('Average Rating (1-10)')
plt.ylabel('')
plt.xlim(9.0, 10.05)

for p in barplot_raw.patches:
    width = p.get_width()
    plt.text(width + 0.02, p.get_y() + p.get_height()/2. + 0.1, '{:1.2f}'.format(width), ha="center")

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/top_10_directors_raw.png', dpi=300)
plt.close()

# ==========================================
# CHART 2: Runtime Evolution & Correlation (Dual-Axis Line Chart)
# ==========================================
query2 = """
SELECT
    CAST((y.year_value // 10) * 10 AS INTEGER) AS decade,
    ROUND(AVG(t.runtime_minutes), 2) AS avg_runtime,
    ROUND(CORR(f.average_rating, t.runtime_minutes), 4) AS runtime_rating_correlation
FROM fct_title_ratings f
JOIN dim_title_snapshot t ON f.title_id = t.title_id
JOIN dim_year y ON f.year_id = y.year_id
JOIN stg_title_basics stg ON f.title_id = stg.title_id
WHERE t.runtime_minutes IS NOT NULL
  AND t.dbt_valid_to IS NULL
  AND y.year_value IS NOT NULL
  AND stg.title_type = 'movie'
GROUP BY decade
ORDER BY decade ASC
"""
df2 = con.execute(query2).df()

# Filter out older years lacking sufficient data (keep 1920 onwards)
df2 = df2[df2['decade'] >= 1920]

fig, ax1 = plt.subplots(figsize=(12, 6))

# Axis 1: Average Runtime (Blue line)
color = 'tab:blue'
ax1.set_xlabel('Decade', fontsize=12)
ax1.set_ylabel('Average Runtime (minutes)', color=color, fontsize=12)
ax1.plot(df2['decade'], df2['avg_runtime'], color=color, marker='o', linewidth=2.5, label='Avg Runtime')
ax1.tick_params(axis='y', labelcolor=color)

# Axis 2: Correlation (Red line)
ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Pearson Correlation (Runtime vs Rating)', color=color, fontsize=12)
ax2.plot(df2['decade'], df2['runtime_rating_correlation'], color=color, marker='s', linestyle='--', linewidth=2.5, label='Correlation')
ax2.tick_params(axis='y', labelcolor=color)
ax2.axhline(0, color='gray', linestyle=':', linewidth=1.5) # Zero line for correlation

plt.title('Movie Runtime Evolution vs. Audience Rating Correlation (1920-2020)', fontsize=14, fontweight='bold')
fig.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/runtime_and_correlation.png', dpi=300)
plt.close()

# ==========================================
# CHART 3: Hidden Gems vs Overrated (Scatter Plot)
# ==========================================
query3 = """
WITH categorized AS (
    SELECT
        g.genre_name,
        CASE WHEN f.average_rating >= 7.5 AND f.num_votes BETWEEN 1000 AND 10000 THEN 1 ELSE 0 END AS is_hidden_gem,
        CASE WHEN f.average_rating <= 6.0 AND f.num_votes > 50000 THEN 1 ELSE 0 END AS is_overrated
    FROM fct_title_ratings f
    JOIN bridge_title_genres bg ON f.title_id = bg.title_id
    JOIN dim_genre g ON bg.genre_id = g.genre_id
    JOIN stg_title_basics stg ON f.title_id = stg.title_id
    WHERE stg.title_type = 'movie'
)
SELECT
    genre_name,
    SUM(is_hidden_gem) AS hidden_gems,
    SUM(is_overrated) AS overrated
FROM categorized
GROUP BY genre_name
HAVING SUM(is_hidden_gem) > 10 AND SUM(is_overrated) > 0
"""
df3 = con.execute(query3).df()

plt.figure(figsize=(12, 8))
sns.scatterplot(
    data=df3, x='overrated', y='hidden_gems',
    hue='genre_name', s=150, palette='tab20', legend=False
)

for i in range(df3.shape[0]):
    plt.text(
        df3['overrated'][i] + 5,
        df3['hidden_gems'][i] + 5,
        df3['genre_name'][i],
        fontsize=10,
        alpha=0.8
    )

plt.title('Hidden Gems vs Overrated Titles by Genre (Volume)', fontsize=14, fontweight='bold')
plt.xlabel('Number of Overrated Titles (Score <= 6.0, Votes > 50k)')
plt.ylabel('Number of Hidden Gems (Score >= 7.5, Votes 1k - 10k)')
plt.axline((0, 0), slope=1, color='gray', linestyle='--', alpha=0.5) # Linie de egalitate

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/hidden_gems_scatter.png', dpi=300)
plt.close()

# ==========================================
# CHART 4: Top Director-Actor Collaborations (Bar Chart)
# ==========================================
query4 = """
SELECT
    p_dir.primary_name || ' & ' || p_act.primary_name AS collaboration,
    ROUND(AVG(f.average_rating), 2) AS avg_collab_rating
FROM fct_title_ratings f
JOIN stg_title_basics stg ON f.title_id = stg.title_id
JOIN bridge_title_crew b_dir ON f.title_id = b_dir.title_id AND b_dir.role = 'director'
JOIN dim_person p_dir ON b_dir.name_id = p_dir.name_id
JOIN stg_title_principals prin ON f.title_id = prin.title_id AND prin.category IN ('actor', 'actress')
JOIN dim_person p_act ON prin.name_id = p_act.name_id
WHERE stg.title_type = 'movie'
GROUP BY p_dir.primary_name, p_act.primary_name
HAVING COUNT(f.title_id) >= 4 AND SUM(f.num_votes) >= 100000
ORDER BY avg_collab_rating DESC
LIMIT 10
"""
df4 = con.execute(query4).df()

plt.figure(figsize=(11, 6))
barplot4 = sns.barplot(x='avg_collab_rating', y='collaboration', data=df4, palette='crest')
plt.title('Top 10 Director-Actor Collaborations by Average Rating\n(Min. 4 movies & 100k total votes)', fontsize=14, fontweight='bold')
plt.xlabel('Average Rating (1-10)')
plt.ylabel('')
plt.xlim(8.0, 9.2)

for p in barplot4.patches:
    width = p.get_width()
    plt.text(width + 0.02, p.get_y() + p.get_height()/2. + 0.1, '{:1.2f}'.format(width), ha="center")

plt.tight_layout()
plt.savefig(f'{OUTPUT_DIR}/top_collaborations.png', dpi=300)
plt.close()
