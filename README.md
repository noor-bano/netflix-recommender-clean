# Netflix Movie Recommender

A Streamlit app that recommends similar Netflix movies or shows based on content.

## Features
- Filter by genre and type
- Recommend 5 similar titles using TF-IDF + cosine similarity
- Clean and interactive UI

## Run Locally
```
streamlit run app.py
```

## Deploy on Streamlit Cloud
1. Push to GitHub
2. Go to https://streamlit.io/cloud
3. Deploy `app.py` with the included `movies.pkl` and `similarity.pkl`
