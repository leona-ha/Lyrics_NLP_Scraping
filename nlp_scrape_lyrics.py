''' Web-Scrape Lyrics from lyrics.com '''
import re
import requests
from bs4 import BeautifulSoup as bs# import beautiful soup = bs
import pandas as pd
import spacy
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

NLP = spacy.load('en_core_web_sm')

### 1. Get lyrics from lyrics.com  ###

def get_artists_link(url, artist):
    '''Creates a list of complete URL's '''
    links = []
    titles = []
    baselink = 'https://www.lyrics.com'

    soup = bs(requests.get(url).text, features="lxml")

    for i in soup.find_all(class_='tal qx'):
        try:
            link = i.a.get('href')
            link_art = link.split('/')[-2]

            if artist in link_art:
                links.append(baselink+ link)
                titles.append(i.string)
        except:
            pass

    return links, titles

### 2. Tokenize and Lemmatize strings and remove stop words. Insert custom stop words optionally ###

def spacify_my_text(lyrics_text, custom_stop=None):
    ''' Loops through list of lyrics, tokenizes and lemmatizes words and removes stop words.
        Returns lemmatized list of words'''

    spacyfied = []
    original = list(NLP.Defaults.stop_words)

    if custom_stop:
        for i in custom_stop:
            if i not in original:
                original.append(i)

    for sentence in lyrics_text:

        parsed_sentence = NLP(sentence.lower())
        treated_sentence = ''

        for token in parsed_sentence:

            if str(token) not in original:
                treated_sentence += str(token.lemma_) + ' '
        spacyfied.append(treated_sentence.strip())

    return spacyfied

### 3. Create list with Sentiment Analysis ###

def lyrics_sentiment(lylist):
    ''' Analyzes valence of lyrics '''
    comp = []
    for i in lylist:
        sid_obj = SentimentIntensityAnalyzer()
        sentiment_dict = sid_obj.polarity_scores(i)
        if sentiment_dict['compound'] >= 0.05 :
            comp.append("Positive")

        elif sentiment_dict['compound'] <= - 0.05 :
            comp.append("Negative")

        else :
            comp.append("Neutral")

    return comp

### 4. Scrape lyrics from web and append them to dataframe/textfile ###

def get_lyrics(linklist, titles, artist, stoplist=None, totext=False):
    ''' Scrapes lyrics from list of links '''
    title_clean = []
    lyric_list = []
    for i, j in zip(linklist, titles):

        if not any(re.findall(r'\(|\[|/|Intro|Outro', str(j), re.IGNORECASE)):
            lyric = bs(requests.get(i).text, 'html.parser').body.find(id='lyric-body-text').text
            lyric = re.sub(r"\r|\n|\\\\|\W", " ", lyric)
            lyric_list.append(lyric)
            title_clean.append(str(j))
            spacyf = spacify_my_text(lyric_list, custom_stop=stoplist)
            sentim = lyrics_sentiment(lyric_list)
        if totext:
            with open('{}_{}.txt'.format(artist, str(j)), 'w') as lyrics:
                lyrics.write("%s " % lyric)

    title_lyrics = pd.DataFrame(zip(title_clean, lyric_list, [artist]*len(title_clean),
                                spacyf, sentim),
                                columns=['title', 'lyrics', 'artist', 'spacified_lyric', 'sentiment_comp']).drop_duplicates()

    return title_lyrics, lyric_list, spacyf
