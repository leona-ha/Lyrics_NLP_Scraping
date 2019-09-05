# Web Scraping and Natural Languace Processing on Lyrics

**Goal: Build a text classification model to predict the artist from a piece of text.**

**Steps:**

*Check nlp_scrape_lyrics.py for steps 1-3 and Lyrics_Scrape_Clean.ipynb for Step 4.*

1. **Scrape** lyrics from two or more artists on lyrics.com using BeautifulSoup and RegEx.
2. **Text Preprocessing**:  e.g. Tokenizing and Lemmatizing using Spacy
  - Tokenization: break your text document down into individual parts that have some semantic value (e.g. words, punctuation marks, numeric digits)
  - Lemmatization: Find the roots (=the first form variants) of words
3. Simple **Sentiment Analysis** using vaderSentiment
4. Build a **Text Classification Model** that uses CountVectorization, TFIDF-Transformation and a Multinomial Naïve Bayes Classifier to predict artists from song-lyrics.
  - scikit-learn CountVectorizer: Tokenize a document and form vocabulary list (fit). Encode a new document with vocabulary (transform). Returns a sparse representation of the counts.
  - tfidfVectorizer: Normalize the counts --> Scale down the impact of tokens that occur frequently are thus empirically less informative than features that occur in a small fraction of the training corpus.
  - Naive Bayes: a Simple and intuitive classifier that works well under small data 


<img width="427" alt="Bildschirmfoto 2019-09-04 um 16 14 37" src="https://user-images.githubusercontent.com/50407361/64263170-81d2d000-cf2f-11e9-8dd0-2401e9783cbe.png">

**Worcloud Quiz: Who's the Artist?**
