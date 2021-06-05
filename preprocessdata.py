import json
import re
import pandas as pd
from nltk.tokenize import word_tokenize
import string
import csv
import time


x = []
y = []
k = []
final_tweets=[]
some_milby = []
tweets_data = []
def getData(dataIn):
    print("=========== Read from file ===========")
    fileRead = open(dataIn, "r")
    for i in fileRead:
        try:    
            tweets = json.loads(i)
            tweets_data.append(tweets)
        except:
            continue
    print("\n=========== Read complete ===========")
    processData()

def processData():
    print("\n=========== Processing data ===========")
    remove_emoji = re.compile('[\U00010000-\U0010ffff]', flags = re.UNICODE)
    for i in range (len(tweets_data)):
        user_tweets = tweets_data[i]['text']
        user_id = tweets_data[i]['id_str']
        user_tweets = remove_emoji.sub(r'', user_tweets)
        user_tweets = re.sub(r'@[A-Za-z0-9_]+', '', user_tweets)   ##remove mentions
        user_tweets = re.sub(r'#', '', user_tweets)                ## remove hashtags
        user_tweets = re.sub(r'RT : ','',user_tweets)               ##remove retweets
        user_tweets = re.sub(r'https?:\/\/[A-Za-z0-9\.\/]+', '', user_tweets) ##remove URLs
        x.append(user_tweets)
        k.append(user_id)
        
    print("\n=========== Processing complete ===========")

def readDict(dictIn):
    dictionary = open(dictIn, "r")
    readCSV = csv.reader(dictionary, delimiter='\t')
    for line in readCSV:
        p = []
        p.append(line[2])                                       ##the dictionary word
        p.append(line[5])                                       ##the polarity of the word
        y.append(p)                                             ##dictionary data list

    print("\n=========== Reading from dictionary complete =========== ")
    labelData()

def labelData():
    print("\n=========== Labelling the data ===========")
    counter = 0
    for i in x:
        tweet_token = i
        token = word_tokenize(tweet_token)
        sum_num =0
        sum_word =0
        for t in token:
            for p in y:
                if t == p[0]:
                    sentiment = p[1]
                    if (sentiment== "positive"):
                        sum_word += 1
                        sum_num += 1
                    elif(sentiment=="negative"):
                        sum_word += 1
                        sum_num += -1
                    else:
                        sum_word += 1
                        sum_num += 0

                    break
        if (sum_word !=0):
            sum_more = sum_num / sum_word
            if(sum_more >= 0.2):
                sum_more = 1
            elif(sum_more <0.2 and sum_more> -0.5):
                sum_more =0
            elif (sum_more <= -0.5):
                sum_more = -1
            else:
                print("****")

        var = []
        var_id = k[counter]
        var.append(var_id)
        var.append(i)
        var.append(sum_more)
        some_milby.append(var)
        counter+=1
    
    print("\n=========== Labelling completed ===========")
    saveToCSV()

def saveToCSV():
    df = pd.DataFrame(some_milby)
    df.to_excel('processed_data/output1.xlsx', header=("id","Tweet","sentiment"), index=False)
    print("\n=========== Data saved ===========")               
    
if __name__== "__main__":
    getData('data/tweetData.txt')
    readDict('data/dictionary.tsv')
