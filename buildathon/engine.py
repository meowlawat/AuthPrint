import string
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_stylometry(text):
    if not text:
        return {"avg_word_len": 0, "punct_ratio": 0, "upper_ratio": 0}
    words = text.split()
    chars = len(text)
    if len(words) == 0:
        return {"avg_word_len": 0, "punct_ratio": 0, "upper_ratio": 0}
    
    avg_word_len = sum(len(w) for w in words) / len(words)
    punct_count = sum(1 for c in text if c in string.punctuation)
    upper_count = sum(1 for c in text if c.isupper())
    
    return {
        "avg_word_len": round(avg_word_len, 2),
        "punct_ratio": round(punct_count / chars, 3) if chars > 0 else 0,
        "upper_ratio": round(upper_count / chars, 3) if chars > 0 else 0
    }

def get_fingerprint_similarity(history, new_text):
    vectorizer = TfidfVectorizer(analyzer='char', ngram_range=(3, 5))
    try:
        tfidf_matrix = vectorizer.fit_transform([" ".join(history), new_text])
        sim_score = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0]
        return round(sim_score, 3)
    except Exception:
        return 0.0

def evaluate_anomaly(history_stats, new_stats, sim_score):
    word_len_drift = abs(history_stats['avg_word_len'] - new_stats['avg_word_len']) / (history_stats['avg_word_len'] + 0.001)
    punct_drift = abs(history_stats['punct_ratio'] - new_stats['punct_ratio']) * 100
    upper_drift = abs(history_stats['upper_ratio'] - new_stats['upper_ratio']) * 100
    
    sim_penalty = (1.0 - sim_score) * 60 
    drift_penalty = (word_len_drift * 10) + punct_drift + upper_drift
    
    raw_score = sim_penalty + drift_penalty
    anomaly_score = min(int(raw_score), 100)
    
    flagged = anomaly_score > 60
    if flagged:
        reasoning = f"High Deviation: {anomaly_score}% statistical drift from baseline N-Gram footprint."
    else:
        reasoning = "Stable: Submission aligns with established stylometric variance."
        
    return {"anomaly_score": anomaly_score, "flagged": flagged, "reasoning": reasoning}