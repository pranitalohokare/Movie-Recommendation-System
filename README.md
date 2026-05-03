# 🎬 Movie Recommendation System (Flask)

A hybrid Movie Recommendation System built using Flask that suggests movies based on user preferences. The system combines **Content-Based Filtering** and **Collaborative Filtering** to provide accurate and personalized recommendations.

---

## 🚀 Features

* 🔍 Movie search with auto-suggestions
* 🎯 Hybrid recommendation system (Content + Collaborative)
* 📊 Trending movies section
* 🖼️ Movie cards with posters and details
* ⚡ REST API endpoints
* 🎨 Modern responsive UI (HTML, CSS, JS)
* 🛡️ Error handling with fallback system

---

## 🧠 Recommendation Techniques Used

### 1. Content-Based Filtering

* Uses movie genres
* TF-IDF vectorization
* Cosine similarity to find similar movies

### 2. Collaborative Filtering

* Based on user ratings
* Uses user-item matrix
* Finds similar movies using user behavior

### 3. Hybrid Model

* Combines both methods (50% each)
* Improves accuracy and recommendation quality

---

## 🏗️ Project Structure

movie-recommendation/
│
├── app.py
├── requirements.txt
├── .env
│
├── data/
│   ├── movies.csv
│   └── ratings.csv
│
├── static/
│   └── style.css
│
├── templates/
│   └── index.html
│
└── README.md

---

## ⚙️ Installation & Setup

### 1. Clone Repository

git clone https://github.com/pranitalohokare/movie-recommendation.git
cd movie-recommendation

---

### 2. Install Dependencies

pip install -r requirements.txt

---

### 3. Add OMDb API Key

Create a `.env` file:

OMDB_API_KEY=your_api_key_here

Get API key from: http://www.omdbapi.com/

---

## ▶️ Run the Application

python app.py

Open in browser:
http://127.0.0.1:5000

---

## 🔌 API Endpoints

| Endpoint         | Method | Description              |
| ---------------- | ------ | ------------------------ |
| `/`              | GET    | Home page                |
| `/api/search`    | GET    | Search movie suggestions |
| `/api/recommend` | POST   | Get recommendations      |
| `/api/trending`  | GET    | Get trending movies      |

---

## 📊 Example API Request

### POST `/api/recommend`

{
"movie": "Inception"
}

### Response

[
{
"title": "Interstellar",
"poster": "url_here"
}
]

---

## 🖼️ UI Highlights

* Clean and modern UI design
* Smooth animations and hover effects
* Responsive layout for laptops
* Interactive movie cards

---

## ⚠️ Limitations

* Cold start problem (new users/movies)
* Depends on dataset quality
* External API dependency for posters

---

## 🚀 Future Improvements

* User login & personalization
* Watchlist feature
* Deep learning-based recommendations
* Cloud deployment (AWS/Render)
* Mobile app version

---

## 🧑‍💻 Tech Stack

* Backend: Flask (Python)
* Frontend: HTML, CSS, JavaScript
* Machine Learning: Scikit-learn
* API: OMDb API
Sreenshots:
<img width="959" height="454" alt="image" src="https://github.com/user-attachments/assets/9a2a3ca3-b786-4977-9a41-29f2527d17eb" />
<img width="975" height="281" alt="image" src="https://github.com/user-attachments/assets/0bf3dcdf-cc48-40b4-8cc6-dbbcca5c5a39" />
<img width="981" height="473" alt="image" src="https://github.com/user-attachments/assets/b8aa877d-d963-4b5e-b817-4a829899ea50" />
<img width="975" height="451" alt="image" src="https://github.com/user-attachments/assets/9177d0cf-e16f-4178-a584-eb905eac114d" />

---

## 📌 Conclusion

This project demonstrates how machine learning can be used to build intelligent recommendation systems. The hybrid approach improves recommendation quality and enhances user experience.

---

## 🙌 Acknowledgements

* OMDb API for movie data
* Open-source datasets for movies and ratings

---

## 📬 Contact

Name: Pranita Lohokare
Email: Mailto:pranitalohokare02@gmail.com

---
