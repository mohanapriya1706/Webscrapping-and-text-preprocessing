# -*- coding: utf-8 -*-
"""Untitled5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VkFd-pFwAYwO_QPMz2geJdZK5oFZCmko
"""

pip install bs4 #package for scraping

from bs4 import BeautifulSoup as bs
import requests #sending request to access the content
from csv import writer # wirting it in csv format
import pandas as pd

websites = ['https://www.deccanherald.com/business/business-news/indian-crude-oil-exports-grow-as-eu-eliminates-russia-1199791.html',
            'https://www.eia.gov/energyexplained/oil-and-petroleum-products/',
            'https://blogs.worldbank.org/developmenttalk/what-triggered-oil-price-plunge-2014-2016-and-why-it-failed-deliver-economic-impetus-eight-charts']
headers_={'user-agent':'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.0)'}

with open('Topicmodelling_final.csv','w',encoding='utf8',newline='') as f:
  thewriter=writer(f)   
  header=['articles'] 
  thewriter.writerow(header)  
  for website in websites:
    response = requests.get(website)
    html = response.content
    soup = bs(html,'html.parser')
    paragraphs = soup.find_all('p')
    for p in paragraphs:
      para = p.text
      info=[para]
      thewriter.writerow(info)

df=pd.read_csv('Topicmodelling_final.csv')

df['lower1']=df['articles'].apply(lambda x: x.lower())

import string
def remove_punctuation(text):
    punc="".join([i for i in text if i not in string.punctuation])
    return punc
df['punc1']= df['lower1'].apply(lambda x:remove_punctuation(x))

#token
from nltk.tokenize import TweetTokenizer as tt
tokenizer = tt()      # instantiate the tokenizer class
df['token1'] = df['punc1'].apply(lambda x: tokenizer.tokenize(x))

#remove stopwords
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
stopword=stopwords.words('english')
def remove_stopwords(text):
    output= [i for i in text if i not in stopword]
    return output
df['stop1']= df['token1'].apply(lambda x:remove_stopwords(x))

from nltk.stem.porter import PorterStemmer
from nltk.stem import WordNetLemmatizer
#steming
stemmer = PorterStemmer()
def stemming(text):
    stem_text = [stemmer.stem(word) for word in text]
    return stem_text
df['stem1']=df['stop1'].apply(lambda x: stemming(x))


#lemma
nltk.download('wordnet')
nltk.download('omw-1.4')
lemma = WordNetLemmatizer()
def lemmatizer(text):
    lemm_text = [lemma.lemmatize(word) for word in text]
    return lemm_text
df['lemma1']=df['stem1'].apply(lambda x:lemmatizer(x))

df=df.drop(0,axis=0)
df['text']=df['lemma1'].apply(lambda x:' '.join(x))
df











































