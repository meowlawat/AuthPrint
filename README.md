# ✨ AuthPrint: Identity Mismatch Engine

> **First Dollar Builder Track Submission** > *Moderating authenticity by checking the identity, not just the text.*

## 🚨 The Problem
First Dollar relies on authentic creator influence, but the bounty platform is losing value to AI-generated spam. Existing moderation tools (like GPTZero) analyze text in a vacuum. They ask: *"Did an AI write this?"* Because of this, they are easily bypassed. A user simply prompts an LLM to "write in a messy, casual tone with lowercase letters," and the generic AI detector passes it as human. 

## 💡 Our Solution: Behavioral Fingerprinting
AuthPrint abandons generic AI detection and introduces **Identity-Based Moderation**. 

Instead of looking for robotic text, our engine asks: ***"Does this submission match the established, mathematical writing habits of this specific creator?"***

Even if an LLM mimics tone perfectly, it struggles to replicate the consistent character-level and statistical micro-habits of a real human across multiple signals.

## ⚙️ How It Works (The Architecture)
AuthPrint is a multi-signal anomaly detection system built entirely from scratch. It utilizes a 3-layer deterministic engine:

1. **Stylometric Variance:** Calculates statistical drift in average sentence length, punctuation density, and casing ratios between the user's history and the new tweet.
2. **Character N-Gram Fingerprinting:** Uses TF-IDF Vectorization (`ngram_range=(3,5)`) to map a user's unconscious writing habits (spacing, suffix patterns, spelling quirks) entirely independent of the topic.
3. **Unified Anomaly Scoring:** A custom, 100% offline mathematical algorithm that calculates cosine similarity and stylistic drift, outputting a decisive **Identity Risk Score (0-100)**.

## 🚀 Why It Wins
* **Bypass-Resistant:** You can prompt an LLM to sound "casual," but you cannot prompt it to perfectly match a TF-IDF N-Gram matrix of a user's historical keystroke habits.
* **100% Offline & Deterministic:** No API wrappers. No rate limits. No Wi-Fi dependencies. It runs on pure Scikit-learn math and executes in milliseconds.
* **Scalable:** Designed to be easily integrated into First Dollar's backend submission pipeline.

## 💻 Run the Demo Locally

**1. Clone the repository:**
```bash
git clone [https://github.com/YOUR_USERNAME/authprint.git](https://github.com/YOUR_USERNAME/authprint.git)
cd authprint
