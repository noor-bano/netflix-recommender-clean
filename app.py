import streamlit as st
import pickle

# Load files
df = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

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

if st.button("Recommend"):
    index = df[df['title'] == selected_movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), key=lambda x: x[1], reverse=True)
    st.write("### Recommended Titles:")
    for i in distances[1:6]:
        st.write(f"- {df.iloc[i[0]].title}")
