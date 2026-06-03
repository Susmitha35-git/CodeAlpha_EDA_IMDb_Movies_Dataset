import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

def generate_imdb_data():
    np.random.seed(42)
    genres     = ['Action','Comedy','Drama','Thriller','Sci-Fi','Romance','Horror','Animation','Documentary','Crime']
    directors  = ['Christopher Nolan','Steven Spielberg','Martin Scorsese','Quentin Tarantino',
                  'James Cameron','Ridley Scott','Denis Villeneuve','David Fincher',
                  'Peter Jackson','Coen Brothers','Wes Anderson','Alfonso Cuaron',
                  'Guillermo del Toro','David Lynch','Stanley Kubrick']
    languages  = ['English','Hindi','French','Spanish','Japanese','Korean','Italian','German']
    countries  = ['USA','UK','India','France','Japan','South Korea','Germany','Australia']
    n = 1000
    years  = np.random.randint(1980, 2024, n)
    genres_list = np.random.choice(genres, n)
    ratings = np.clip(np.random.normal(6.5, 1.2, n), 1.0, 10.0).round(1)
    votes   = np.random.randint(1000, 2000000, n)
    runtime = np.random.randint(70, 220, n)
    budget  = np.round(np.random.exponential(60, n), 1)
    gross   = np.round(budget * np.random.uniform(0.2, 8.0, n), 1)
    gross   = np.clip(gross, 0.5, 3000)
    df = pd.DataFrame({
        'title':        [f'Movie Title {i+1}' for i in range(n)],
        'genre':        genres_list,
        'year':         years,
        'rating':       ratings,
        'votes':        votes,
        'runtime_min':  runtime,
        'director':     np.random.choice(directors, n),
        'language':     np.random.choice(languages, n),
        'country':      np.random.choice(countries, n),
        'budget_million':  budget,
        'gross_million':   gross,
        'metascore':    np.random.randint(20, 100, n),
    })
    df['profit_million'] = (df['gross_million'] - df['budget_million']).round(1)
    df['roi_percent']    = ((df['gross_million'] / df['budget_million'].replace(0,1) - 1) * 100).round(1)
    null_mask = np.random.choice([True, False], n, p=[0.08, 0.92])
    df.loc[null_mask, 'metascore'] = np.nan
    return df

print("=" * 60)
print("EDA: IMDb MOVIES DATASET")
print("=" * 60)

df = generate_imdb_data()
df.to_csv("imdb_movies.csv", index=False)
print(f"Dataset ready: {len(df)} movies saved as 'imdb_movies.csv'")

print("\nShape:", df.shape)
print("\nColumn Names & Data Types:")
print(df.dtypes)
print("\nFirst 5 Rows:")
print(df.head())
print("\nBasic Statistics:")
print(df.describe().round(2))
print("\nMissing Values:")
missing = df.isnull().sum()
print(missing[missing > 0])

print("\nGenre Distribution:")
print(df['genre'].value_counts())
print("\nTop 10 Highest Rated Movies:")
print(df.nlargest(10, 'rating')[['title','genre','year','rating','votes']].to_string(index=False))
print("\nAverage Rating by Genre:")
print(df.groupby('genre')['rating'].mean().round(2).sort_values(ascending=False))
print("\nAverage Gross by Genre (Million $):")
print(df.groupby('genre')['gross_million'].mean().round(1).sort_values(ascending=False))
print("\nMovies per Decade:")
df['decade'] = (df['year'] // 10 * 10).astype(str) + 's'
print(df['decade'].value_counts().sort_index())

sns.set_theme(style='whitegrid')
DARK   = '#0f0f1a'
GOLD   = '#FFD700'
BLUE   = '#4361ee'
RED    = '#e63946'
GREEN  = '#2dc653'
WHITE  = '#f0f0f0'
GREY   = '#1e1e2e'

fig, axes = plt.subplots(3, 3, figsize=(20, 18), facecolor=DARK)
fig.suptitle('  IMDb Movies Dataset — Exploratory Data Analysis',
             fontsize=22, fontweight='bold', color=WHITE, y=1.01)

def style(ax, title):
    ax.set_facecolor(GREY)
    ax.set_title(title, color=WHITE, fontsize=12, fontweight='bold', pad=8)
    ax.tick_params(colors=WHITE)
    ax.xaxis.label.set_color(WHITE)
    ax.yaxis.label.set_color(WHITE)
    for spine in ax.spines.values():
        spine.set_edgecolor('#333')

genre_counts = df['genre'].value_counts()
axes[0, 0].bar(genre_counts.index, genre_counts.values,
               color=sns.color_palette('tab10', len(genre_counts)),
               edgecolor=DARK)
style(axes[0, 0], 'Number of Movies by Genre')
axes[0, 0].set_ylabel('Count', color=WHITE)
axes[0, 0].tick_params(axis='x', rotation=35)

axes[0, 1].hist(df['rating'], bins=30, color=GOLD, edgecolor=DARK, alpha=0.9)
axes[0, 1].axvline(df['rating'].mean(), color=RED, linestyle='--', linewidth=2,
                   label=f"Mean: {df['rating'].mean():.2f}")
axes[0, 1].axvline(df['rating'].median(), color=GREEN, linestyle='--', linewidth=2,
                   label=f"Median: {df['rating'].median():.2f}")
style(axes[0, 1], 'IMDb Rating Distribution')
axes[0, 1].set_xlabel('Rating', color=WHITE)
axes[0, 1].set_ylabel('Count', color=WHITE)
axes[0, 1].legend(facecolor=GREY, labelcolor=WHITE)

genre_rating = df.groupby('genre')['rating'].mean().sort_values(ascending=False)
axes[0, 2].barh(genre_rating.index[::-1], genre_rating.values[::-1],
                color=BLUE, edgecolor=DARK)
style(axes[0, 2], 'Average Rating by Genre')
axes[0, 2].set_xlabel('Average IMDb Rating', color=WHITE)
for bar in axes[0, 2].patches:
    w = bar.get_width()
    axes[0, 2].text(w + 0.02, bar.get_y() + bar.get_height()/2,
                    f'{w:.2f}', va='center', color=WHITE, fontsize=8)

decade_counts = df['decade'].value_counts().sort_index()
axes[1, 0].bar(decade_counts.index, decade_counts.values,
               color=GREEN, edgecolor=DARK)
style(axes[1, 0], 'Movies Released per Decade')
axes[1, 0].set_ylabel('Number of Movies', color=WHITE)
axes[1, 0].tick_params(axis='x', rotation=20)

axes[1, 1].scatter(df['budget_million'], df['gross_million'],
                   c=df['rating'], cmap='RdYlGn', alpha=0.5, s=20)
sc = axes[1, 1].scatter(df['budget_million'], df['gross_million'],
                         c=df['rating'], cmap='RdYlGn', alpha=0.5, s=20)
plt.colorbar(sc, ax=axes[1, 1], label='IMDb Rating').ax.yaxis.set_tick_params(color=WHITE)
axes[1, 1].plot([0, df['budget_million'].max()],
                [0, df['budget_million'].max()],
                color=RED, linestyle='--', linewidth=1.5, label='Break-even')
style(axes[1, 1], 'Budget vs Gross Revenue (Color = Rating)')
axes[1, 1].set_xlabel('Budget (Million $)', color=WHITE)
axes[1, 1].set_ylabel('Gross Revenue (Million $)', color=WHITE)
axes[1, 1].legend(facecolor=GREY, labelcolor=WHITE, fontsize=8)

axes[1, 2].hist(df['runtime_min'], bins=30, color='#bc8cff', edgecolor=DARK, alpha=0.9)
axes[1, 2].axvline(df['runtime_min'].mean(), color=RED, linestyle='--', linewidth=2,
                   label=f"Mean: {df['runtime_min'].mean():.0f} min")
style(axes[1, 2], 'Movie Runtime Distribution')
axes[1, 2].set_xlabel('Runtime (minutes)', color=WHITE)
axes[1, 2].set_ylabel('Count', color=WHITE)
axes[1, 2].legend(facecolor=GREY, labelcolor=WHITE)

top_directors = df.groupby('director')['rating'].mean().sort_values(ascending=False).head(10)
axes[2, 0].barh(top_directors.index[::-1], top_directors.values[::-1],
                color=GOLD, edgecolor=DARK)
style(axes[2, 0], 'Top 10 Directors by Avg Rating')
axes[2, 0].set_xlabel('Average IMDb Rating', color=WHITE)

genre_gross = df.groupby('genre')['gross_million'].mean().sort_values(ascending=False)
axes[2, 1].bar(genre_gross.index, genre_gross.values,
               color=sns.color_palette('tab10', len(genre_gross)),
               edgecolor=DARK)
style(axes[2, 1], 'Average Gross Revenue by Genre (Million $)')
axes[2, 1].set_ylabel('Avg Gross (Million $)', color=WHITE)
axes[2, 1].tick_params(axis='x', rotation=35)

num_cols = df[['rating','votes','runtime_min','budget_million','gross_million','metascore']].dropna()
corr = num_cols.corr()
sns.heatmap(corr, ax=axes[2, 2], annot=True, fmt='.2f',
            cmap='coolwarm', center=0, linewidths=0.5,
            annot_kws={'color': WHITE})
style(axes[2, 2], 'Correlation Heatmap')

plt.tight_layout()
plt.savefig('imdb_eda.png', dpi=150, bbox_inches='tight', facecolor=DARK)
plt.show()
print("\n Plot saved as 'imdb_eda.png'")

print("\n" + "=" * 60)
print(" KEY FINDINGS")
print("=" * 60)
print(f"   Total movies analyzed     : {len(df)}")
print(f"   Year range                : {df['year'].min()} – {df['year'].max()}")
print(f"   Average IMDb rating       : {df['rating'].mean():.2f}")
print(f"   Most common genre         : {df['genre'].value_counts().idxmax()}")
print(f"   Highest rated genre       : {genre_rating.idxmax()} ({genre_rating.max():.2f})")
print(f"   Highest grossing genre    : {genre_gross.idxmax()} (${genre_gross.max():.1f}M avg)")
print(f"   Average runtime           : {df['runtime_min'].mean():.0f} minutes")
print(f"   Average budget            : ${df['budget_million'].mean():.1f}M")
print(f"   Average gross revenue     : ${df['gross_million'].mean():.1f}M")
print("=" * 60)
