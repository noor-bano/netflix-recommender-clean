import streamlit as st
import pickle
import os
import gdown
import requests

# Replace with your actual TMDB API key
TMDB_API_KEY = "9697b8019fd7c3d9424b3de56620d51d"

# Function to get poster
def fetch_poster(movie_title):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={TMDB_API_KEY}&query={movie_title}"
        response = requests.get(url).json()
        if response['results']:
            poster_path = response['results'][0].get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except:
        pass
    return None



def download_file(file_id, filename):
    url = f"https://drive.google.com/uc?id={file_id}&export=download"
    if not os.path.exists(filename):
        gdown.download(url, filename, quiet=False, fuzzy=True)

# Actual file IDs from your Drive links
download_file("1eJ8wtcL5wwjI7YUpL_DXcU0dZ4ZeM-Os", "movies.pkl")
download_file("12lj8E4Xkt-bzLsrwORUsDBfG-G1p6pMe", "similarity.pkl")

# Load after download
df = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))


# Sidebar filters
st.sidebar.header("🎛️ Filter Titles")
genres = df['listed_in'].str.split(', ').explode()
type_filter = st.sidebar.selectbox("Type", ["All"] + sorted(df['type'].unique()))
genre_filter = st.sidebar.selectbox("Genre", ["All"] + sorted(genres.dropna().unique()))

filtered_df = df.copy()
if type_filter != "All":
    filtered_df = filtered_df[filtered_df['type'] == type_filter]
if genre_filter != "All":
    filtered_df = filtered_df[filtered_df['listed_in'].str.contains(genre_filter, case=False)]

# UI
st.title("🎬 Netflix Movie Recommender")
movie_list = filtered_df['title'].unique()
selected_movie = st.selectbox("Choose a movie", movie_list)

if st.button("🎯 Recommend Similar Titles"):
    index = df[df['title'] == selected_movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)

    st.markdown("### 🎬 You might also enjoy:")
    cols = st.columns(2)

    for i, col in zip(distances[1:6], cols * 3):
        movie_title = df.iloc[i[0]].title
        movie_type = df.iloc[i[0]].type
        genres = df.iloc[i[0]].listed_in

        poster_url = fetch_poster(movie_title)

        with col:
            if poster_url:
                st.image(poster_url, width=150)
            st.markdown(f"**{movie_title}**")
            st.caption(f"📺 {movie_type} | 🎭 {genres}")


