from typing import List, Optional

from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, Session

# FastAPI app instance
app = FastAPI()

# Allow all origins (frontend requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# Database Config
DATABASE_URL = "mysql+pymysql://root:vinayak%40786@localhost/music_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Many-to-Many Relationship Tables
playlist_songs = Table(
    "playlist_songs", Base.metadata,
    Column("playlist_id", Integer, ForeignKey("playlists.id"), primary_key=True),
    Column("song_id", Integer, ForeignKey("songs.id"), primary_key=True)
)

song_artists = Table(
    "song_artists", Base.metadata,
    Column("song_id", Integer, ForeignKey("songs.id"), primary_key=True),
    Column("artist_id", Integer, ForeignKey("artists.id"), primary_key=True)
)


# Models
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    playlists = relationship("Playlist", back_populates="owner", cascade="all, delete")


class Playlist(Base):
    __tablename__ = "playlists"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="playlists")
    songs = relationship("Song", secondary=playlist_songs, back_populates="playlists")


class Song(Base):
    __tablename__ = "songs"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    genre = Column(String(50))
    duration = Column(Integer)
    playlists = relationship("Playlist", secondary=playlist_songs, back_populates="songs")
    artists = relationship("Artist", secondary=song_artists, back_populates="songs")


class Artist(Base):
    __tablename__ = "artists"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    country = Column(String(100))
    songs = relationship("Song", secondary=song_artists, back_populates="artists")


# Create tables
Base.metadata.create_all(bind=engine)


# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Schemas (Pydantic Models)
class UserCreateSchema(BaseModel):
    username: str
    email: str

    class Config:
        from_attributes = True


class UserSchema(UserCreateSchema):
    id: int


# Input schema (for creation)
class PlaylistCreate(BaseModel):
    title: str
    user_id: int


# Output schema (for returning data)
class PlaylistSchema(PlaylistCreate):
    id: int

    class Config:
        from_attributes = True


# 🎵 Input schema
class SongCreate(BaseModel):
    title: str
    genre: Optional[str]
    duration: Optional[int]


# 🎵 Output schema
class SongSchema(SongCreate):
    id: int

    class Config:
        from_attributes = True


# 👤 Artist input (for POST)
class ArtistCreate(BaseModel):
    name: str
    country: Optional[str]


# 👤 Artist output (for response)
class ArtistSchema(ArtistCreate):
    id: int

    class Config:
        from_attributes = True


class PlaylistSongSchema(BaseModel):
    playlist_id: int
    song_id: int


class SongArtistSchema(BaseModel):
    song_id: int
    artist_id: int


# Routes

## Users
@app.post("/users/", response_model=UserSchema)
def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    new_user = User(username=user.username, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/", response_model=List[UserSchema])
def get_users(db: Session = Depends(get_db)):
    return db.query(User).all()


## Playlists
@app.post("/playlists/", response_model=PlaylistSchema)
def create_playlist(playlist: PlaylistCreate, db: Session = Depends(get_db)):
    new_playlist = Playlist(title=playlist.title, user_id=playlist.user_id)
    db.add(new_playlist)
    db.commit()
    db.refresh(new_playlist)
    return new_playlist


@app.get("/playlists/", response_model=List[PlaylistSchema])
def get_playlists(db: Session = Depends(get_db)):
    return db.query(Playlist).all()


## Songs
@app.post("/songs/", response_model=SongSchema)
def create_song(song: SongCreate, db: Session = Depends(get_db)):
    new_song = Song(title=song.title, genre=song.genre, duration=song.duration)
    db.add(new_song)
    db.commit()
    db.refresh(new_song)
    return new_song


@app.get("/songs/", response_model=List[SongSchema])
def get_songs(db: Session = Depends(get_db)):
    return db.query(Song).all()


## Artists
@app.post("/artists/", response_model=ArtistSchema)
def create_artist(artist: ArtistCreate, db: Session = Depends(get_db)):
    new_artist = Artist(name=artist.name, country=artist.country)
    db.add(new_artist)
    db.commit()
    db.refresh(new_artist)
    return new_artist


@app.get("/artists/", response_model=List[ArtistSchema])
def get_artists(db: Session = Depends(get_db)):
    return db.query(Artist).all()


## Playlist-Song Relationship
@app.post("/playlist-songs/")
def add_song_to_playlist(playlist_song: PlaylistSongSchema, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_song.playlist_id).first()
    song = db.query(Song).filter(Song.id == playlist_song.song_id).first()

    if not playlist or not song:
        raise HTTPException(status_code=404, detail="Playlist or Song not found")

    playlist.songs.append(song)
    db.commit()
    return {"message": "Song added to playlist successfully"}


## Song-Artist Relationship
@app.post("/song-artists/")
def add_artist_to_song(song_artist: SongArtistSchema, db: Session = Depends(get_db)):
    song = db.query(Song).filter(Song.id == song_artist.song_id).first()
    artist = db.query(Artist).filter(Artist.id == song_artist.artist_id).first()

    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    if not artist:
        raise HTTPException(status_code=404, detail="Artist not found")

    if artist in song.artists:
        return {"message": "Artist already linked to song"}

    song.artists.append(artist)
    db.commit()
    return {"message": "Artist added to song successfully"}


@app.get("/playlists/{playlist_id}/songs")
def get_songs_in_playlist(playlist_id: int, db: Session = Depends(get_db)):
    playlist = db.query(Playlist).filter(Playlist.id == playlist_id).first()

    if not playlist:
        raise HTTPException(status_code=404, detail="Playlist not found")

    result = []
    for song in playlist.songs:
        result.append({
            "song_id": song.id,
            "title": song.title,
            "genre": song.genre,
            "duration": song.duration,
            "artists": [{"id": artist.id, "name": artist.name, "country": artist.country} for artist in song.artists]
        })

    return JSONResponse(content=result)
