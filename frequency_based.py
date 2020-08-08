import nltk
import pandas as pd
import numpy as np
from urllib import request
from nltk import *
import math
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from bs4 import BeautifulSoup as bs
import re
from boilerpy3 import extractors


#nltk.download('punkt')
#nltk.download('stopwords')
#download above 2 first

stop_words=set(stopwords.words('english')) 

#####trying ends rn rh ###############



url ="https://timesofindia.indiatimes.com/pcpaathshala/parents/parents-articles/managing-stress-in-the-new-normal/Intelshow/76957466.cms"

def get_data_bs(url):
  html = request.urlopen(url).read()
  soup =bs(html,'html.parser')
  cont=soup.findAll('p')
  content=''
  for para in cont:
    content+=para.text

  cleaned_content=re.sub(r'\[[0-9]*\]',' ',content)
  cleaned_content_final=re.sub(r'\s+',' ',cleaned_content)
  return cleaned_content_final

def get_data_b4(url):
    
  extractor = extractors.ArticleExtractor()
  content = extractor.get_content_from_url(url)
  return content

#####trying ends rn rh ###############

def word_tokenize(file):
  words=nltk.word_tokenize(file)
  word=[w for w in words if not w in stop_words]
  filtered_words=[w for w in word if len(w)>1]
  return filtered_words

def freq_dist(file):
  filtered_words=word_tokenize(file)
  x=FreqDist(filtered_words)
  c={k: v for k, v in x.items()}
  return c

def sent_tokenizing(file):
  sentences=nltk.sent_tokenize(file)
  return sentences


def sent_cost(sentences,freq_table):
  sen_val=dict()
  for sen in sentences:
    len_of_sent=len(nltk.word_tokenize(sen))
    for w in freq_table:
      if w in sen.lower():
        if sen in sen_val:
          sen_val[sen]+=freq_table[w]
        else:
          sen_val[sen]=freq_table[w]
    #print(sen_val[sen],len_of_sent)
    sen_val[sen]=math.floor(sen_val[sen]/len_of_sent)
  return sen_val

  
def average_len(sen_val):
  av=0
  for val in sen_val:
    av+=sen_val[val]
  av=math.floor(av/len(sen_val))
  return av


def get_summary(sen_val,av):
  summary=""
  for val in sen_val:
    tmp=int(sen_val[val])
    if(tmp>av):
      summary+=val
      summary+='\n'
  return summary

def headline(sen_val):
  sorted_sen_val={k:v for k, v in sorted(sen_val.items(), key=lambda item: item[1],reverse =True)}
  res = list(sorted_sen_val.keys())
  return res[0]

  
def main():
  url=input("enter the url")
  type_=input("reply with summary or headline")

  content=get_data_bs(url)
  sentences=sent_tokenizing(content)
  freq_table=freq_dist(content)
  sen_val=sent_cost(sentences,freq_table)
  av=average_len(sen_val)
  if(type_.lower()=='headline'):
    print(headline(sen_val))
  else:
    print(get_summary(sen_val,av))
  

