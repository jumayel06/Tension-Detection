import nltk, string
from sklearn.feature_extraction.text import TfidfVectorizer

class Similarity:
    def __init__(self):
        self.stemmer = nltk.stem.porter.PorterStemmer()
        self.remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)

    def stem_tokens(self, tokens):
        return [self.stemmer.stem(item) for item in tokens]
    
    def normalize(self, text):
        return self.stem_tokens(nltk.word_tokenize(text.lower().translate(self.remove_punctuation_map)))
    
    def cosine_sim(self, text1, text2):
        vectorizer = TfidfVectorizer(tokenizer = self.normalize, stop_words = 'english')
        tfidf = vectorizer.fit_transform([text1, text2])
        return ((tfidf * tfidf.T).A)[0,1]
