# Nusha Bhat
# DS3500 Adv Programming with Data
# HW6 - Mini Project
# parser for lyrics
from collections import Counter
import re
import string
import nltk
from nltk.corpus import stopwords

def lyrics_parser(filename):
    """parser for song lyrics"""
    with open(filename, 'r') as f:
        text = f.read()
        # remove [Intro], [Verse]
    cleaned_text = re.sub(r'\[.*?\]', '', text)
        # lower / remove punctuation
    cleaned_text = cleaned_text.lower().translate(str.maketrans('', '', string.punctuation))
    words = cleaned_text.split()
    stop_words = set(stopwords.words('english'))
    custom_stopwords = {"yeah", "uh", "ah", "oh", "the", "can", "its", "in", "it", "is"}
    stop_words.update(custom_stopwords)

    # rem stopwords
    filtered_words = [word for word in words if word not in stop_words]

    # wc
    word_count = Counter(filtered_words)

    return {
        'raw_text': text,
        'cleaned_text': cleaned_text,
        'wordcount': word_count,
        'numwords': len(words)
      }

