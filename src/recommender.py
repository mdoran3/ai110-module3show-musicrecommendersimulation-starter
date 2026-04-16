from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    target_valence: float = 0.5

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    import csv

    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            songs.append({
                "id":           int(row["id"]),
                "title":        row["title"],
                "artist":       row["artist"],
                "genre":        row["genre"],
                "mood":         row["mood"],
                "energy":       float(row["energy"]),
                "tempo_bpm":    float(row["tempo_bpm"]),
                "valence":      float(row["valence"]),
                "danceability": float(row["danceability"]),
                "acousticness": float(row["acousticness"]),
            })
    print(f"Loaded Songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py

    Scoring formula (max = 10):
      score = (4 × genre_match)
            + (3 × mood_match)
            + (2 × (1 - |user.energy - song.energy|))
            + (1 × (1 - |user.valence - song.valence|))
    """
    reasons: List[str] = []

    # Genre (weight 4) — categorical hard constraint
    genre_match = 1 if user_prefs.get("favorite_genre", "").lower() == song["genre"].lower() else 0
    genre_score = 4 * genre_match
    if genre_match:
        reasons.append(f"Genre matches ({song['genre']})")
    else:
        reasons.append(f"Genre mismatch (wanted {user_prefs.get('favorite_genre')}, got {song['genre']})")

    # Mood (weight 3) — categorical intent signal
    mood_match = 1 if user_prefs.get("favorite_mood", "").lower() == song["mood"].lower() else 0
    mood_score = 3 * mood_match
    if mood_match:
        reasons.append(f"Mood matches ({song['mood']})")
    else:
        reasons.append(f"Mood mismatch (wanted {user_prefs.get('favorite_mood')}, got {song['mood']})")

    # Energy (weight 2) — numeric proximity
    energy_diff = abs(user_prefs.get("target_energy", 0.5) - song["energy"])
    energy_score = 2 * (1 - energy_diff)
    reasons.append(f"Energy score {energy_score:.2f}/2 (diff={energy_diff:.2f})")

    # Valence (weight 1) — numeric proximity
    valence_diff = abs(user_prefs.get("target_valence", 0.5) - song["valence"])
    valence_score = 1 * (1 - valence_diff)
    reasons.append(f"Valence score {valence_score:.2f}/1 (diff={valence_diff:.2f})")

    score = genre_score + mood_score + energy_score + valence_score
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = [
        (song, score, "\n".join(reasons))
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    ranked = sorted(scored, key=lambda x: x[1], reverse=True)

    return ranked[:k]
