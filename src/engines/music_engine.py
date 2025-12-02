import logging
import random
from openai import OpenAI
from publishers.music_publisher import save_music_pack

logger = logging.getLogger("MusicEngine")
client = OpenAI()

MUSIC_GENRES = [
    "lofi chill",
    "cyberpunk synthwave",
    "meditation calm",
    "cinematic ambient",
    "workout trap beat",
    "future bass rhythm",
    "retro 80s vibe",
    "deep focus background"
]


def generate_music_track():
    """AI generates track metadata + MIDI placeholder."""
    genre = random.choice(MUSIC_GENRES)

    prompt = f"""
    Create an AI music track concept for genre '{genre}'.
    Provide JSON:
    {{
        "title": "...",
        "bpm": "...",
        "genre": "...",
        "midi": "MIDI placeholder text",
        "description": "..."
    }}
    """

    r = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    return r.choices[0].message["content"]


def run_music_engine():
    logger.info("🎵 Music Engine Running...")

    try:
        import json
        raw = generate_music_track()
        data = json.loads(raw)

        title = data["title"]
        midi = data["midi"]
        metadata = f"Genre: {data['genre']}\nBPM: {data['bpm']}\nDescription:\n{data['description']}"

        save_music_pack(title, midi, metadata)

        logger.info("✅ Music Track Generated")

    except Exception as e:
        logger.error(f"❌ Music Engine Error: {e}")
