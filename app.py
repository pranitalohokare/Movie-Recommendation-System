from flask import Flask, render_template, request, jsonify
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer
import requests
import os
from dotenv import load_dotenv
import webbrowser

load_dotenv()

app = Flask(__name__)

# ------------------------------
# LOAD DATA
# ------------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

movies_path = os.path.join(BASE_DIR, 'data', 'movies.csv')
ratings_path = os.path.join(BASE_DIR, 'data', 'ratings.csv')

def load_csv(path):
    return pd.read_csv(path, sep=None, engine='python')

movies = load_csv(movies_path)
ratings = load_csv(ratings_path)

movies = movies.head(2000)
ratings = ratings.head(8000)

movies.columns = movies.columns.str.strip().str.lower()
ratings.columns = ratings.columns.str.strip().str.lower()

movies['title'] = movies['title'].str.strip()

if 'genres' not in movies.columns:
    movies['genres'] = movies['title']

movies['genres'] = movies['genres'].fillna('')

# ------------------------------
# CONTENT SIMILARITY
# ------------------------------
tfidf = TfidfVectorizer(stop_words='english')
tfidf_matrix = tfidf.fit_transform(movies['genres'])

content_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)

# ------------------------------
# COLLAB FILTERING
# ------------------------------
try:
    user_movie_matrix = ratings.pivot_table(
        index='userid',
        columns='movieid',
        values='rating'
    ).fillna(0)

    collab_similarity = cosine_similarity(user_movie_matrix.T)

    collab_sim_df = pd.DataFrame(
        collab_similarity,
        index=user_movie_matrix.columns,
        columns=user_movie_matrix.columns
    )

except:
    collab_sim_df = pd.DataFrame()

# ------------------------------
# POSTER FUNCTION
# ------------------------------
def fetch_poster(title):
    api_key = os.getenv("OMDB_API_KEY")

    fallback = "https://via.placeholder.com/300x450?text=Movie+Poster"

    if not api_key:
        return fallback

    try:
        clean_title = title.split("(")[0].strip()

        url = f"http://www.omdbapi.com/?apikey={api_key}&t={clean_title}"
        data = requests.get(url, timeout=5).json()

        if data.get("Response") == "True":
            poster = data.get("Poster")
            if poster and poster != "N/A":
                return poster

    except:
        pass

    return fallback

# ------------------------------
# HYBRID RECOMMENDATION + TRAILER
# ------------------------------
def hybrid_recommend(movie_title, n=10):

    if movie_title not in movies['title'].values:
        return []

    idx = movies[movies['title'] == movie_title].index[0]
    movie_id = movies.iloc[idx]['movieid']

    content_scores = list(enumerate(content_similarity[idx]))

    if not collab_sim_df.empty and movie_id in collab_sim_df.index:
        collab_scores = collab_sim_df[movie_id]
    else:
        collab_scores = pd.Series(np.zeros(len(movies)))

    combined_scores = []

    for i, score in content_scores:
        m_id = movies.iloc[i]['movieid']
        collab_score = collab_scores.get(m_id, 0)

        hybrid_score = (0.5 * score) + (0.5 * collab_score)
        combined_scores.append((i, hybrid_score))

    combined_scores = sorted(combined_scores, key=lambda x: x[1], reverse=True)

    results = []

    # ------------------------------
    # SEARCHED MOVIE FIRST
    # ------------------------------
    results.append({
        "title": movie_title,
        "poster": fetch_poster(movie_title),
        "trailer": f"https://www.youtube.com/results?search_query={movie_title.replace(' ', '+')}+trailer",
        "type": "searched"
    })

    # ------------------------------
    # RECOMMENDED MOVIES
    # ------------------------------
    count = 0
    for i, _ in combined_scores:

        title = movies.iloc[i]['title']

        if title == movie_title:
            continue

        results.append({
            "title": title,
            "poster": fetch_poster(title),
            "trailer": f"https://www.youtube.com/results?search_query={title.replace(' ', '+')}+trailer",
            "type": "recommended"
        })

        count += 1
        if count >= n:
            break

    return results

# ------------------------------
# TRENDING MOVIES
# ------------------------------
def trending_movies(n=10):
    top = ratings.groupby('movieid')['rating'].mean().sort_values(ascending=False).head(n)

    results = []

    for m_id in top.index:
        title = movies[movies['movieid'] == m_id]['title'].values

        if len(title) > 0:
            results.append({
                "title": title[0],
                "poster": fetch_poster(title[0]),
                "trailer": f"https://www.youtube.com/results?search_query={title[0].replace(' ', '+')}+trailer"
            })

    return results

# ------------------------------
# ROUTES
# ------------------------------
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/search')
def search():
    query = request.args.get('q', '').lower()

    if not query:
        return jsonify([])

    results = movies[movies['title'].str.lower().str.contains(query)]
    return jsonify(results['title'].head(10).tolist())

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.get_json()

    if not data or 'movie' not in data:
        return jsonify({"error": "Movie not provided"}), 400

    recs = hybrid_recommend(data['movie'])

    if not recs:
        return jsonify({"error": "Movie not found"}), 404

    return jsonify(recs)

@app.route('/api/trending')
def trending():
    return jsonify(trending_movies())

# ------------------------------
# RUN APP
# ------------------------------
if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=False)