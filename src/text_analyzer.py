import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter
import numpy as np


class TextAnalyzer:
    def __init__(self):
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
            nltk.data.find('sentiment/vader_lexicon')
        except LookupError:
            nltk.download('punkt')
            nltk.download('vader_lexicon')
            nltk.download('stopwords')

        self.sia = SentimentIntensityAnalyzer()
        self.stop_words = set(stopwords.words('english'))

        # Genre-related keywords
        self.genre_keywords = {
            'classical': ['orchestra', 'symphony', 'classical', 'piano', 'violin', 'concert'],
            'rock': ['guitar', 'rock', 'band', 'drums', 'electric', 'heavy'],
            'jazz': ['jazz', 'blues', 'swing', 'improvisation', 'saxophone', 'trumpet'],
            'pop': ['pop', 'dance', 'rhythm', 'beat', 'modern', 'contemporary']
        }

    def analyze_text(self, text):
        """
        Analyze text to determine mood and genre.
        Returns tuple of (mood, genre)
        """
        # Sentiment analysis for mood
        sentiment = self.sia.polarity_scores(text)
        mood = self._determine_mood(sentiment)

        # Genre analysis
        genre = self._determine_genre(text)

        return mood, genre

    def _determine_mood(self, sentiment):
        """
        Determine mood based on sentiment scores
        """
        compound = sentiment['compound']

        if compound >= 0.5:
            return 'happy'
        elif compound <= -0.5:
            return 'sad'
        elif compound >= 0.2:
            return 'upbeat'
        elif compound <= -0.2:
            return 'melancholic'
        else:
            return 'neutral'

    def _determine_genre(self, text):
        """
        Determine genre based on keyword analysis
        """
        # Tokenize and clean text
        tokens = word_tokenize(text.lower())
        tokens = [word for word in tokens if word.isalnum() and word not in self.stop_words]

        # Count genre-related keywords
        genre_scores = {genre: 0 for genre in self.genre_keywords}

        for word in tokens:
            for genre, keywords in self.genre_keywords.items():
                if word in keywords:
                    genre_scores[genre] += 1

        # If no clear genre is detected, use sentiment to suggest one
        if max(genre_scores.values()) == 0:
            sentiment = self.sia.polarity_scores(text)['compound']
            if sentiment > 0.3:
                return 'pop'
            elif sentiment < -0.3:
                return 'classical'
            else:
                return 'jazz'

        return max(genre_scores.items(), key=lambda x: x[1])[0]


def analyze_text(text):
    """
    Wrapper function for text analysis
    """
    analyzer = TextAnalyzer()
    return analyzer.analyze_text(text)
