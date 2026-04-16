"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from .recommender import load_songs, recommend_songs


def main() -> None:
    songs = load_songs("data/songs.csv") 

    # Starter example profile
    # user_prefs = {
    #     "favorite_genre": "jazz",
    #     "favorite_mood": "relaxed",
    #     "target_energy": 0.35,
    #     "target_valence": 0.70,
    # }

    user_prefs = {
        "favorite_genre": "electronic",
        "favorite_mood": "intense",
        "target_energy": 0.35,
        "target_valence": 0.70,
    }

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    print("  TOP RECOMMENDATIONS")
    print("=" * 50)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']} by {song['artist']}")
        print(f"    Score: {score:.2f} / 10")
        print("    " + "-" * 30)
        for line in explanation.splitlines():
            print(f"    {line}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
