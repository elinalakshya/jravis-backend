import os
import logging

logger = logging.getLogger("MusicPublisher")

OUTPUT = "output/music"
os.makedirs(OUTPUT, exist_ok=True)


def save_music_pack(title, midi_data, metadata):
    """
    Creates a folder for AI music track:
    - midi file (placeholder)
    - metadata (title, genre, bpm)
    """
    safe = title.replace(" ", "_").replace("/", "_")
    folder = os.path.join(OUTPUT, safe)
    os.makedirs(folder, exist_ok=True)

    try:
        # Save MIDI placeholder
        midi_path = os.path.join(folder, "track.mid")
        with open(midi_path, "w", encoding="utf-8") as f:
            f.write(midi_data)

        # Save metadata
        meta_path = os.path.join(folder, "metadata.txt")
        with open(meta_path, "w", encoding="utf-8") as f:
            f.write(metadata)

        logger.info(f"🎵 Music Pack Saved: {folder}")
        return folder

    except Exception as e:
        logger.error(f"❌ Error saving music pack: {e}")
        return None
