"""
Text processing module for NLP operations
"""
import re
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import spacy

class TextProcessor:
    def __init__(self):
        """Initialize the text processor with NLP models"""
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            print("Warning: spaCy model 'en_core_web_sm' not found. Please install with: python -m spacy download en_core_web_sm")
            self.nlp = None
        
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        from nltk.corpus import stopwords
        from nltk.tokenize import word_tokenize
        self.stop_words = set(stopwords.words('english'))
        self.word_tokenize = word_tokenize
    
    def preprocess_text(self, text):
        """Clean and preprocess text"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Tokenize and remove stopwords
        tokens = self.word_tokenize(text)
        tokens = [token for token in tokens if token not in self.stop_words]
        
        return ' '.join(tokens)
    
    def extract_keywords(self, text, num_keywords=10):
        """Extract important keywords from text"""
        if not text or not self.nlp:
            return []
        
        doc = self.nlp(text)
        keywords = []
        
        # Extract nouns and proper nouns as keywords
        for token in doc:
            if token.pos_ in ['NOUN', 'PROPN'] and not token.is_stop and len(token.text) > 2:
                keywords.append(token.lemma_)
        
        # Extract noun phrases
        for chunk in doc.noun_chunks:
            if len(chunk.text.split()) > 1:
                keywords.append(chunk.text)
        
        # Return unique keywords
        return list(set(keywords))[:num_keywords]
    
    def calculate_similarity(self, text1, text2):
        """Calculate similarity between two texts using TF-IDF and cosine similarity"""
        # Preprocess texts
        processed_text1 = self.preprocess_text(text1)
        processed_text2 = self.preprocess_text(text2)
        
        if not processed_text1 or not processed_text2:
            return 0.0
        
        # Vectorize texts
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([processed_text1, processed_text2])
        
        # Calculate cosine similarity
        similarity = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])
        return similarity[0][0]
    
    def extract_entities(self, text):
        """Extract named entities from text"""
        if not text or not self.nlp:
            return {}
        
        doc = self.nlp(text)
        entities = {}
        
        for ent in doc.ents:
            if ent.label_ not in entities:
                entities[ent.label_] = []
            entities[ent.label_].append(ent.text)
        
        return entities