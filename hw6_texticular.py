from collections import Counter, defaultdict
import re
import string
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob
import plotly.graph_objects as go
from math import ceil, sqrt
import matplotlib.pyplot as plt
from wordcloud import WordCloud

nltk.download('stopwords')

class Textastic:
    def __init__(self):
        self.data = defaultdict(dict)  # store text data
    def default_parser(self, filename):
        """parase text file to produce results"""
        with open(filename, 'r') as f:
            raw_text = f.read()
        cleaned_text = self.preprocess(raw_text)
        word_count = Counter(cleaned_text.split())
        return {
            'raw_text': raw_text,
            'cleaned_text': cleaned_text,
            'wordcount': word_count,
            'numwords': len(cleaned_text.split())
        }

    def preprocess(self, text):
        """CLEAN text by removing punctuation, stopwords, and lowering case"""
        stop_words = set(stopwords.words('english'))
        text = text.lower()
        text = re.sub(r'\[.*?\]', '', text)  # Remove [Intro], [Verse], etc.
        text = text.translate(str.maketrans('', '', string.punctuation))
        text = ' '.join(word for word in text.split() if word not in stop_words)
        return text

    def load_text(self, filename, label=None, parser=None):
        """process txt files"""
        try:
            if parser is None:
                results = self.default_parser(filename)
            else:
                results = parser(filename)

            if label is None:
                label = filename

            for k, v in results.items():
                self.data[k][label] = v
        # exception handling
        except FileNotFoundError:
            print(f"Error: File {filename} not found.")
        except Exception as e:
            print(f"Error processing file {filename}: {e}") #helped for errors in parser

    def word_clouds(self):
        """word clouds for each song w subplot layout"""

        num_texts = len(self.data['cleaned_text'])
        # exception handling
        if num_texts == 0:
            print("No texts available to generate word clouds.")
            return

        cols = max(1, ceil(sqrt(num_texts)))
        rows = ceil(num_texts / cols)

        fig, axs = plt.subplots(rows, cols, figsize=(15, 10))
        axs = axs.flatten()  # flatten

        for i, (label, text) in enumerate(self.data['cleaned_text'].items()):
            wordcloud = WordCloud(width=800, height=400, max_words=15).generate(text)
            axs[i].imshow(wordcloud, interpolation='bilinear')
            axs[i].axis('off')
            axs[i].set_title(label)

        for j in range(i + 1, len(axs)):
            axs[j].axis('off')

        plt.tight_layout()
        plt.savefig("hw6_wordcloud", dpi=300)
        plt.show()

    def word_count_summary(self):
        """summary of word counts for each song"""
        print("Word Count Summary:")
        for label, count in self.data['numwords'].items():
            print(f"{label}: {count} words")

    def plotly_sankey(self, k=5):
        """ Sankey diagram which displays counts on interactive
            hover, fixed spacing, grouping common words across
            songs
        """
        sources = []
        targets = []
        values = []
        labels = []

        # songs as nodes (source nodes)
        song_labels = list(self.data['wordcount'].keys())
        for song in song_labels:
            labels.append(song)

        # identify common words
        word_set = set()
        for wordcount in self.data['wordcount'].values():
            top_words = [word for word, _ in wordcount.most_common(k)]
            word_set.update(top_words)
        word_labels = sorted(word_set)  # Sorted for consistency
        labels.extend(word_labels)

        # map sources/targets
        for song_idx, (song, wordcount) in enumerate(self.data['wordcount'].items()):
            top_words = wordcount.most_common(k)
            for word, count in top_words:
                # connection from song to word
                sources.append(song_idx)  # Index of the song
                target_idx = len(song_labels) + word_labels.index(word)  # Offset for word nodes
                targets.append(target_idx)
                values.append(count)

        # create Sankey diagram!!!
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=20,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=labels
            ),
            link=dict(
                source=sources,
                target=targets,
                value=values,
                hoverinfo="all",  # Show details on hover
            )
        )])
        fig.update_layout(
            title_text="Sankey Diagram: Songs and Top Words",
            font=dict(size=12),
            width=1200,
            height=800,
            title_x=0.5
        )
        fig.write_image("hw6_sankey.png")
        fig.show()

    def sentiment_overlay(self):
        """overlay sentiment analysis results in bar format"""
        sentiments = {label: TextBlob(text).sentiment.polarity
                      for label, text in self.data['cleaned_text'].items()}

        colors = ['green' if score > 0 else 'red' if score < 0 else 'gray' for score in sentiments.values()]
        plt.bar(sentiments.keys(), sentiments.values(), color=colors)
        plt.axhline(0, color='black', linewidth=0.5)

        # text labels for sentiment values
        for idx, (label, score) in enumerate(sentiments.items()):
            plt.text(idx, score, f"{score:.2f}", ha='center', va='bottom' if score > 0 else 'top')

        plt.title("Sentiment Analysis: Polarity")
        plt.ylabel("Sentiment Polarity")
        plt.xlabel("Texts")
        plt.xticks(rotation=45)
        plt.savefig("hw6_sentiment", dpi=300)
        plt.show()

