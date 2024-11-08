# src/midi_utils.py
import pretty_midi
import subprocess
import os
from pathlib import Path
import logging
import random

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


class MIDIGenerator:
    def __init__(self):
        self.instrument_programs = {
            'Piano': 0,
            'Guitar': 24,
            'Strings': 48,
            'Flute': 73
        }

    def create_midi(self, notes, durations, tempo, instrument='Piano'):
        """Create MIDI file with debug logging"""
        try:
            logger.debug(f"Creating MIDI with {len(notes)} notes, tempo={tempo}, instrument={instrument}")

            # Initialize PrettyMIDI object
            pm = pretty_midi.PrettyMIDI(initial_tempo=float(tempo))

            # Create instrument instance
            program = self.instrument_programs.get(instrument, 0)
            instrument_instance = pretty_midi.Instrument(program=program)

            # Create notes with higher velocity
            current_time = 0.0
            for i, (note, duration) in enumerate(zip(notes, durations)):
                note_instance = pretty_midi.Note(
                    velocity=100,  # Fixed higher velocity
                    pitch=int(note),
                    start=current_time,
                    end=current_time + duration
                )
                instrument_instance.notes.append(note_instance)
                current_time += duration
                logger.debug(f"Added note {i}: pitch={note}, start={current_time:.2f}, duration={duration:.2f}")

            # Add instrument to PrettyMIDI object
            pm.instruments.append(instrument_instance)
            logger.debug(f"MIDI created successfully with {len(instrument_instance.notes)} notes")
            return pm

        except Exception as e:
            logger.error(f"Error creating MIDI: {str(e)}")
            raise


def convert_to_mp3(midi_path, soundfont_path=None):
    """Convert MIDI to MP3 with detailed logging"""
    try:
        if soundfont_path is None:
            # Use default soundfont path
            soundfont_path = str(Path(__file__).parent.parent / "resources" / "soundfonts" / "default.sf2")

        logger.debug(f"Using soundfont: {soundfont_path}")
        logger.debug(f"Input MIDI path: {midi_path}")

        # Generate output paths
        wav_path = midi_path.replace('.mid', '.wav')
        mp3_path = midi_path.replace('.mid', '.mp3')

        logger.debug(f"WAV path: {wav_path}")
        logger.debug(f"MP3 path: {mp3_path}")

        # MIDI to WAV using FluidSynth with better settings
        fluidsynth_cmd = [
            'fluidsynth',
            '-F', wav_path,  # Output WAV file
            '-O', 's16',  # 16-bit output
            '-R', '44100',  # Sample rate
            '-g', '2.0',  # Gain (increase volume)
            '-C', '0',  # Audio channels (0=auto)
            soundfont_path,  # Soundfont file
            midi_path  # Input MIDI file
        ]

        logger.debug(f"Running FluidSynth command: {' '.join(fluidsynth_cmd)}")
        result = subprocess.run(fluidsynth_cmd,
                                capture_output=True,
                                text=True)
        logger.debug(f"FluidSynth output: {result.stdout}")
        logger.debug(f"FluidSynth errors: {result.stderr}")

        # WAV to MP3 using FFmpeg with better quality
        ffmpeg_cmd = [
            'ffmpeg',
            '-i', wav_path,
            '-codec:a', 'libmp3lame',
            '-qscale:a', '2',  # Variable bitrate quality (2 is high quality)
            '-y',  # Overwrite output file
            mp3_path
        ]

        logger.debug(f"Running FFmpeg command: {' '.join(ffmpeg_cmd)}")
        result = subprocess.run(ffmpeg_cmd,
                                capture_output=True,
                                text=True)
        logger.debug(f"FFmpeg output: {result.stdout}")
        logger.debug(f"FFmpeg errors: {result.stderr}")

        # Verify file sizes
        if os.path.exists(mp3_path):
            mp3_size = os.path.getsize(mp3_path)
            logger.debug(f"Generated MP3 file size: {mp3_size} bytes")
            if mp3_size < 1000:  # If file is too small, something went wrong
                logger.warning("Generated MP3 file is suspiciously small")

        return mp3_path

    except Exception as e:
        logger.error(f"Conversion failed: {str(e)}")
        raise
    finally:
        # Cleanup
        if os.path.exists(wav_path):
            os.remove(wav_path)
        if os.path.exists(midi_path):
            os.remove(midi_path)


# src/melody_generator.py
class MelodyGenerator:
    def __init__(self):
        # Define scales for different moods (expanded range)
        self.scales = {
            'happy': [60, 62, 64, 65, 67, 69, 71, 72, 74, 76],  # C major with higher notes
            'sad': [48, 51, 53, 55, 56, 58, 60, 63, 65],  # C minor with lower notes
            'upbeat': [60, 62, 64, 67, 69, 72, 74, 76, 79],  # C major pentatonic extended
            'melancholic': [48, 51, 53, 55, 58, 60, 63, 65],  # C minor pentatonic extended
            'neutral': [60, 62, 64, 65, 67, 69, 71, 72]  # C major
        }

        # Updated rhythm patterns for more variation
        self.rhythm_patterns = {
            'happy': [0.25, 0.25, 0.5, 0.25, 0.25],
            'sad': [0.75, 0.25, 1.0, 0.5],
            'upbeat': [0.125, 0.125, 0.25, 0.125, 0.125],
            'melancholic': [1.0, 0.5, 0.75, 0.25],
            'neutral': [0.5, 0.25, 0.25, 0.5]
        }

    def generate_melody(self, mood, genre, duration, complexity):
        """Generate more dynamic melody"""
        scale = self.scales.get(mood, self.scales['neutral'])

        # Calculate number of notes
        base_notes = int(duration * 2)  # Base: 2 notes per second
        notes_count = max(base_notes, int(duration * complexity / 3))

        # Generate notes with more variation
        notes = []
        current_index = len(scale) // 2  # Start in middle of scale

        for _ in range(notes_count):
            # Add current note
            notes.append(scale[current_index])

            # Determine next note movement
            if len(notes) > 1:
                # More musical movement based on previous note
                prev_note = notes[-2]
                if prev_note < scale[current_index]:
                    # Move down with higher probability
                    move = -1 if random.random() < 0.7 else 1
                else:
                    # Move up with higher probability
                    move = 1 if random.random() < 0.7 else -1

                # Apply movement with bounds checking
                new_index = current_index + move
                current_index = max(0, min(new_index, len(scale) - 1))
            else:
                # Random movement for first note
                current_index = random.randint(0, len(scale) - 1)

        # Generate more varied durations
        pattern = self.rhythm_patterns.get(mood, [0.5])
        durations = []
        total_time = 0

        while total_time < duration:
            for d in pattern:
                if total_time + d <= duration:
                    durations.append(d)
                    total_time += d
                else:
                    remaining = duration - total_time
                    if remaining > 0.1:  # Only add if significant duration
                        durations.append(remaining)
                    total_time = duration
                    break

        # Trim or extend notes/durations to match
        min_len = min(len(notes), len(durations))
        notes = notes[:min_len]
        durations = durations[:min_len]

        return notes, durations


def generate_melody(mood, genre, duration, complexity=5):
    """Wrapper function"""
    generator = MelodyGenerator()
    return generator.generate_melody(mood, genre, duration, complexity)