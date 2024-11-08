from pathlib import Path

class Settings:
    # Audio settings
    SAMPLE_RATE = 44100
    CHANNELS = 2

    # MIDI settings
    DEFAULT_TEMPO = 120
    DEFAULT_VELOCITY = 100
    DEFAULT_INSTRUMENT = 'Piano'

    # File paths
    RESOURCES_DIR = Path(__file__).parent.parent / "resources"
    SOUNDFONTS_DIR = RESOURCES_DIR / "soundfonts"
    DEFAULT_SOUNDFONT = SOUNDFONTS_DIR / "default.sf2"

    # Generation settings
    MIN_DURATION = 10
    MAX_DURATION = 60
    MIN_TEMPO = 60
    MAX_TEMPO = 180
