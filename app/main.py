import streamlit as st
import sys
from pathlib import Path
import time

# Add the src directory to the system path
sys.path.append(str(Path(__file__).parent.parent))

from src.text_analyzer import analyze_text
from src.melody_generator import generate_melody
from src.midi_utils import create_midi, convert_to_mp3


def main():
    st.set_page_config(page_title="AI Music Generator", layout="wide")

    # Custom CSS
    st.markdown("""
        <style>
        .stTextInput > div > div > input {
            font-size: 16px;
        }
        .stTitle {
            font-size: 42px;
            font-weight: bold;
            margin-bottom: 30px;
        }
        </style>
    """, unsafe_allow_html=True)

    st.title("Text to Music Generator")

    # Sidebar controls
    st.sidebar.header("Advanced Settings")
    instrument = st.sidebar.selectbox(
        "Select Instrument",
        ["Piano", "Guitar", "Strings", "Flute"],
        index=0
    )

    # Main interface
    text_input = st.text_area(
        "Enter your text to generate music:",
        height=150,
        help="Enter any text - a story, poem, or description. The AI will analyze its mood and create matching music."
    )

    # Advanced controls in columns
    col1, col2, col3 = st.columns(3)
    with col1:
        tempo = st.slider("Tempo (BPM)", 60, 180, 120)
    with col2:
        duration = st.slider("Duration (seconds)", 10, 60, 30)
    with col3:
        complexity = st.slider("Complexity", 1, 10, 5)

    if st.button("Generate Music", type="primary"):
        if text_input:
            with st.spinner("Analyzing text and generating music..."):
                try:
                    # Show progress
                    progress_bar = st.progress(0)

                    # Analyze text
                    progress_bar.progress(20)
                    mood, genre = analyze_text(text_input)

                    # Generate melody
                    progress_bar.progress(40)
                    melody = generate_melody(mood, genre, duration, complexity)

                    # Create MIDI
                    progress_bar.progress(60)
                    midi_data = create_midi(melody, tempo, instrument)
                    midi_path = "temp.mid"
                    midi_data.write(midi_path)

                    # Convert to MP3
                    progress_bar.progress(80)
                    mp3_path = convert_to_mp3(midi_path)

                    # Display results
                    progress_bar.progress(100)

                    # Create two columns for results
                    result_col1, result_col2 = st.columns(2)

                    with result_col1:
                        st.success("Music generated successfully!")
                        # Audio player
                        audio_file = open(mp3_path, 'rb')
                        audio_bytes = audio_file.read()
                        st.audio(audio_bytes, format='audio/mp3')

                    with result_col2:
                        # Analysis results
                        st.subheader("Analysis Results")
                        st.write(f"📊 Detected mood: {mood.title()}")
                        st.write(f"🎵 Musical genre: {genre.title()}")
                        st.write(f"⏱️ Duration: {duration} seconds")
                        st.write(f"🎹 Instrument: {instrument}")

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please enter some text to generate music.")


if __name__ == "__main__":
    main()
