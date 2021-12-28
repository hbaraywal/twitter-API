#this code generates and collects 3000 tweets that mentions 'Afghanistan' in it since August 15, 2021, the day when the Afghanistan government collapsed.

import tweepy
from tweepy import *
 
import pandas as pd
import csv
import re 
import string
import preprocessor as p
 
consumer_key = ""
consumer_secret = ""
access_key= ""
access_secret = ""
 
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
 
api = tweepy.API(auth,wait_on_rate_limit=True)
 
csvFile = open('file-name', 'a')
csvWriter = csv.writer(csvFile)
 
search_words = "#Afghanistan"      # enter your words
new_search = search_words + " -filter:retweets"

def keyword_to_csv(keyword,recent):
    try:
        tweets = tweepy.Cursor(api.search,q=keyword).items(recent) #creates query method
        tweets_list = [[tweet.text] for tweet in tweets] 
#pulls text information from tweets
        df = pd.DataFrame(tweets_list,columns=['Text']) 
#creates a pandas dataframe
        df.to_csv('{}.csv'.format(keyword), sep=',', index = False) 
 #creates a csv from data frame
    except BaseException as e:
        print('failed on_status,',str(e))
        time.sleep(3)

     keyword = '#Afghanistan'+ " -filter:retweets" #excludes retweets
recent  = 3000
keyword_to_csv(keyword, recent)

df = pd.read_csv("#Afghanistan -filter:retweets.csv") #loads csv file into pandas dataframe
pd.options.display.max_colwidth = 200 
df.head() #prints out first few columns in a dataframe

df.shape #prints the shape of dataframe

a = df.to_string() #loads the row from dataframe

regex_pattern = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
        u"\U00002500-\U00002BEF"
        u"\U00002702-\U000027B0"
        u"\U00002702-\U000027B0"
        u"\U000024C2-\U0001F251"
        u"\U0001f926-\U0001f937"
        u"\U00010000-\U0010ffff"
        u"\u2640-\u2642"
        u"\u2600-\u2B55"
        u"\u200d"
        u"\u23cf"
        u"\u23e9"
        u"\u231a"
        u"\ufe0f"  # dingbats
        u"\u3030"
                           "]+", flags = re.UNICODE)
match = re.sub(regex_pattern,'',a) #replaces pattern with ''
#print(match)

a = df.to_string()
#print(a)

pattern = re.compile(r'(https?://)?(www\.)?(\w+\.)?(\w+)(\.\w+)(/.+)?')
match = re.sub(pattern,'',a)
#print(match)

#The following block removes @mentions and hashes from the text.
re_list = ['@[A-Za-z0–9_]+', '#','http', '//', 'https', '\n', '/','"\"', 's:t']
combined_re = re.compile( '|'.join( re_list) )
match = re.sub(combined_re,'',a)
#print(match)

from bs4 import BeautifulSoup
a = df.to_string()
#print(a)

del_amp = BeautifulSoup(a, 'lxml')
del_amp_text = del_amp.get_text()
#print(del_amp_text)

from bs4 import BeautifulSoup
from nltk.tokenize import WordPunctTokenizer
token = WordPunctTokenizer()
def cleaning_tweets(t):
    del_amp = BeautifulSoup(t, 'lxml')
    del_amp_text = del_amp.get_text()
    del_link_mentions = re.sub(combined_re, '', del_amp_text)
    del_emoticons = re.sub(regex_pattern, '', del_link_mentions)
    lower_case = del_emoticons.lower()
    words = token.tokenize(lower_case)
    result_words = [x for x in words if len(x) > 2]
    return (" ".join(result_words)).strip()

print("Cleaning the tweets...\n")
cleaned_tweets = []
for i in range(0,3000): #3000 columns in our dataframe
    if( (i+1)%100 == 0 ):
        print("Tweets {} of {} have ben processed".format(i+1,3000))                                                                  
    cleaned_tweets.append(cleaning_tweets((df.Text[i])))
    
#print(cleaned_tweets)

#Next we will use pandas.Series.str.cat() to concatenate the strings in the list cleaned_tweets 
#separated by ‘ ‘.
string = pd.Series(cleaned_tweets).str.cat(sep=' ')
#print(string)

text_file = open("Output.txt", "w")

text_file.write(string)

text_file.close()
from collections import Counter
def word_count(fname):
        with open(fname) as f:
                return Counter(f.read().split())

print("Number of words in the file :",word_count("Output.txt"))

#Generating Word Cloud:
from wordcloud import WordCloud, STOPWORDS
import matplotlib.pyplot as plt
words = set(STOPWORDS)
words.update(["0", "تاریخ یوه بدرنګه مفسده شرموونکې لاسپوڅې څهره بیا ځينې پوهه اګاه خلک وايي اشرف غني امارت بېر",
             "پارون نورستان", "ನದಲ ಕಮಕ ರಗಳಲ ಗಳಲ", "تعدادی مسولین قبلی جمله وکلای پارلمان کارمندان حکومتی رهبران جامعه مدنی فساد غرق نوع استفاده",
             "غنی","فاسد", "افغانستان", "حکومت", "will", "ksanimal", "said", "say", "der", "ګ", "long","طا",
             "طالبان","بان","les", "via", "...", "toda", "epaperjobz","one", "please","وزارت", "میں", "امر", "کابل",
             "های", "طالبانو", "پاکستان", "اور", "برای", "زنان", "افغان", "این", "سفر","این","خان", "است","أفغانستان",
             "امارت"]) #adding our own stopwords
#print(words)

from PIL import Image
import numpy as np
mask = np.array(Image.open('./afg.png'))
wordcloud = WordCloud(width=mask.shape[1],
               height=mask.shape[0],
               mask=mask, background_color="white", stopwords=words,
                      max_font_size=200,max_words=1000, collocations=False, mode='RGBA').generate(string)
plt.figure(figsize=(40,30))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.show()
plt.savefig("afgcloud.png", format = "png")
