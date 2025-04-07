import requests
import streamlit as st

API_URL = "http://localhost:8000"

st.set_page_config(page_title="🎵 Music DBMS", layout="wide")

st.title("🎶 Music DBMS Dashboard")

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "👤 Users", "📃 Playlists", "🎵 Songs", "🎤 Artists", "➕ Playlist ↔ Song", "➕ Song ↔ Artist", "🎼 View Playlist Songs"
])


# Utilities
def get(endpoint):
    return requests.get(f"{API_URL}/{endpoint}").json()


def post(endpoint, payload):
    try:
        res = requests.post(f"{API_URL}/{endpoint}", json=payload)
        res.raise_for_status()  # raises HTTPError for 4xx/5xx
        return res.json()
    except requests.exceptions.RequestException as e:
        st.error(f"❌ Request failed: {e}")
        return None
    except ValueError:
        st.error("❌ Response is not valid JSON (likely a backend error).")
        return None


### 👤 Users
with tab1:
    st.subheader("Add New User")
    c1, c2 = st.columns(2)
    with c1:
        username = st.text_input("Username")
    with c2:
        email = st.text_input("Email")
    if st.button("Create User", use_container_width=True):
        res = post("users/", {"username": username, "email": email})
        if "id" in res:
            st.success(f"✅ Created user: {res['username']}")
        else:
            st.error(f"❌ Error: {res.get('detail', res)}")

    st.divider()
    st.subheader("All Users")
    users = get("users/")
    for u in users:
        st.markdown(f"**{u['username']}** ({u['email']})  –  ID: `{u['id']}`")

### 📃 Playlists
with tab2:
    st.subheader("Create Playlist")
    title = st.text_input("Playlist Title")
    users = get("users/")
    user_dict = {f"{u['username']} (ID: {u['id']})": u['id'] for u in users}
    owner = st.selectbox("Select Owner", user_dict.keys())

    if st.button("Create Playlist", use_container_width=True):
        res = post("playlists/", {"title": title, "user_id": user_dict[owner]})
        if "id" in res:
            st.success(f"✅ Playlist '{res['title']}' created.")
        else:
            st.error(f"❌ Error: {res.get('detail', res)}")

    st.divider()
    st.subheader("All Playlists")
    playlists = get("playlists/")
    for p in playlists:
        st.markdown(f"**{p['title']}**  –  ID: `{p['id']}` | User ID: `{p['user_id']}`")

### 🎵 Songs
with tab3:
    st.subheader("Create Song")
    col1, col2, col3 = st.columns(3)
    with col1:
        song_title = st.text_input("Song Title")
    with col2:
        genre = st.text_input("Genre")
    with col3:
        duration = st.number_input("Duration (sec)", min_value=1, value=180, step=1)

    if st.button("Add Song", use_container_width=True):
        res = post("songs/", {
            "title": song_title,
            "genre": genre,
            "duration": int(duration)
        })
        if "id" in res:
            st.success(f"✅ Song '{res['title']}' created.")
        else:
            st.error(f"❌ Error: {res.get('detail', res)}")

    st.divider()
    st.subheader("All Songs")
    songs = get("songs/")
    for s in songs:
        st.markdown(f"🎵 **{s['title']}** | Genre: `{s['genre']}` | Duration: `{s['duration']}s`")

### 🎤 Artists
with tab4:
    st.subheader("Create Artist")
    a1, a2 = st.columns(2)
    with a1:
        artist_name = st.text_input("Artist Name")
    with a2:
        country = st.text_input("Country")

    if st.button("Add Artist", use_container_width=True):
        res = post("artists/", {"name": artist_name, "country": country})
        if "id" in res:
            st.success(f"✅ Artist '{res['name']}' created.")
        else:
            st.error(f"❌ Error: {res.get('detail', res)}")

    st.divider()
    st.subheader("All Artists")
    artists = get("artists/")
    for a in artists:
        st.markdown(f"🎤 **{a['name']}** ({a['country']})  –  ID: `{a['id']}`")

### ➕ Playlist ↔ Song
with tab5:
    st.subheader("Add Song to Playlist")
    playlists = get("playlists/")
    songs = get("songs/")
    if playlists and songs:
        p_options = {f"{p['title']} (ID: {p['id']})": p['id'] for p in playlists}
        s_options = {f"{s['title']} (ID: {s['id']})": s['id'] for s in songs}
        col1, col2 = st.columns(2)
        with col1:
            selected_p = st.selectbox("Playlist", p_options.keys(), key="playlist_select_tab")
        with col2:
            selected_s = st.selectbox("Song", s_options.keys(), key="song_select_tab")

        if st.button("Add Song to Playlist", use_container_width=True):
            res = post("playlist-songs/", {
                "playlist_id": p_options[selected_p],
                "song_id": s_options[selected_s]
            })
            if "message" in res:
                st.success(f"✅ {res['message']}")
            else:
                st.error("❌ Failed to add song.")
    else:
        st.warning("Please create at least one playlist and one song.")

### ➕ Song ↔ Artist
with tab6:
    st.subheader("Add Artist to Song")
    songs = get("songs/")
    artists = get("artists/")
    if songs and artists:
        s_options = {f"{s['title']} (ID: {s['id']})": s['id'] for s in songs}
        a_options = {f"{a['name']} (ID: {a['id']})": a['id'] for a in artists}
        col1, col2 = st.columns(2)
        with col1:
            selected_s = st.selectbox("Song", s_options.keys(), key="song_select_artist_tab")
        with col2:
            selected_a = st.selectbox("Artist", a_options.keys(), key="artist_select_song_tab")

        if st.button("Add Artist to Song", use_container_width=True):
            res = post("song-artists/", {
                "song_id": s_options[selected_s],
                "artist_id": a_options[selected_a]
            })
            if "message" in res:
                st.success(f"✅ {res['message']}")
            else:
                st.error("❌ Failed to add artist.")
    else:
        st.warning("Please create at least one song and one artist.")

with tab7:
    st.subheader("🎼 View Songs in Playlist")
    playlists = get("playlists/")
    if playlists:
        p_options = {f"{p['title']} (ID: {p['id']})": p['id'] for p in playlists}
        selected_playlist = st.selectbox("Select Playlist", p_options.keys(), key="view_playlist_songs")

        if st.button("Show Songs", use_container_width=True):
            songs_data = get(f"playlists/{p_options[selected_playlist]}/songs")
            if songs_data:
                for song in songs_data:
                    st.markdown(f"**🎵 {song['title']}** ({song['genre']}, {song['duration']}s)")
                    st.markdown("👨‍🎤 Artists:")
                    for artist in song["artists"]:
                        st.markdown(f"- {artist['name']} ({artist['country']})")
                    st.divider()
            else:
                st.warning("No songs found in this playlist.")
