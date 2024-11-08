import pretty_midi
import subprocess
import os
from pathlib import Path
from typing import List, Optional
import numpy as np


class MIDIGenerator:
    def __init__(self):
        self.instrument_programs = {
            'Piano': 0,
            'Guitar': 24,
            'Strings': 48,
            'Flute': 73
        }

    def create_midi(self,
                    notes: List[int],
                    durations: List[float],
                    tempo: int,
                    instrument: str = 'Piano') -> pretty_midi.PrettyMIDI:
        """
        Create MIDI file from notes and durations
        """
        # Initialize PrettyMIDI object
        pm = pretty_midi.PrettyMIDI(initial_tempo=tempo)

        # Create instrument instance
        program = self.instrument_programs.get(instrument, 0)
        instrument_instance = pretty_midi.Instrument(program=program)

        # Create notes
        current_time = 0.0
        for note, duration in zip(notes, durations):
            note_instance = pretty_midi.Note(
                velocity=80 + int(20 * np.random.random()),  # Random velocity between 80-100
                pitch=int(note),
                start=current_time,
                end=current_time + duration
            )
            instrument_instance.notes.append(note_instance)
            current_time += duration

        # Add instrument to PrettyMIDI object
        pm.instruments.append(instrument_instance)
        return pm


def create_midi(melody: tuple, tempo: int, instrument: str = 'Piano') -> pretty_midi.PrettyMIDI:
    """
    Wrapper function for MIDI creation
    """
    generator = MIDIGenerator()
    notes, durations = melody
    return generator.create_midi(notes, durations, tempo, instrument)


def convert_to_mp3(midi_path: str, soundfont_path: Optional[str] = None) -> str:
    """
    Convert MIDI file to MP3 using FluidSynth and FFmpeg
    """
    if soundfont_path is None:
        # Use default soundfont path
        soundfont_path = str(Path(__file__).parent.parent / "resources" / "soundfonts" / "default.sf2")

    # Generate output paths
    wav_path = midi_path.replace('.mid', '.wav')
    mp3_path = midi_path.replace('.mid', '.mp3')

    try:
        # MIDI to WAV conversion
        subprocess.run([
            'fluidsynth',
            '-ni',
            soundfont_path,
            midi_path,
            '-F',
            wav_path
        ], check=True)

        # WAV to MP3 conversion
        subprocess.run([
            'ffmpeg',
            '-i',
            wav_path,
            '-y',  # Overwrite output files
            '-loglevel',
            'error',  # Reduce output verbosity
            mp3_path
        ], check=True)

    except subprocess.CalledProcessError as e:
        raise Exception(f"Conversion failed: {str(e)}")
    finally:
        # Cleanup temporary files
        if os.path.exists(wav_path):
            os.remove(wav_path)
        if os.path.exists(midi_path):
            os.remove(midi_path)

    return mp3_path
