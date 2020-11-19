import re
import nltk
from nltk.stem.wordnet import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances

class Chatter:
    def __init__(self, data):
        self.lemmatizer = WordNetLemmatizer()
        self.vectorizer = TfidfVectorizer()
        self.data = data

        normalizedDataCommands = list(map(lambda datum: self.normalizeAndLemmatize(datum[0]), self.data))
        self.counts = self.vectorizer.fit_transform(normalizedDataCommands)

    def chat(self, query):
        tf = self.vectorizer.transform([self.normalizeAndLemmatize(query)]).toarray()
        cos = 1 - pairwise_distances(self.counts, tf, metric='cosine')
        return self.data[cos.argmax()]

    def normalizeAndLemmatize(self, text):
        lowerCaseText = str(text).lower()
        noSpecialCharacters = re.sub(r'[^ a-z]', '', lowerCaseText)
        tokens = nltk.word_tokenize(noSpecialCharacters)

        partOfSpeechTags = nltk.pos_tag(tokens)
        lemmatizedWords = []
        for token, tag in partOfSpeechTags:
            if tag.startswith('V'):     # Verb
                partOfSpeech = 'v'
            elif tag.startswith('J'):   # Adjective
                partOfSpeech = 'a'
            elif tag.startswith('R'):   # Adverb
                partOfSpeech = 'r'
            else:                       # Noun
                partOfSpeech = 'n'
            lemmatizedWords.append(self.lemmatizer.lemmatize(token, partOfSpeech))

        return ' '.join(lemmatizedWords)