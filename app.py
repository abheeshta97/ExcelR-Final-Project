# -*- coding: utf-8 -*-
"""
Created By: ExcelR Group 1
"""

import re
import subprocess
import requests   # Importing requests to extract content from a url
from bs4 import BeautifulSoup as bs
import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.multiclass import OneVsRestClassifier
from imblearn.over_sampling import RandomOverSampler, SMOTE
from sklearn.model_selection import train_test_split
from sklearn import model_selection, preprocessing, svm, metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import recall_score, accuracy_score, classification_report, confusion_matrix
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from flask import Flask, render_template, url_for, request, redirect
import datetime
from datetime import date, timedelta
import pickle
import joblib
from dateutil import parser as dateparser
import matplotlib as mpl
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.style as style
style.use('fivethirtyeight')

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

today = date.today().strftime("%d %B %Y")
amazon_DF = pd.read_csv("Induction_Data_New.csv")
amazon_DF.dropna(axis = 0, inplace = True)
amazon_DF_clean = amazon_DF.copy()

stop_words = stopwords.words("english")
model = joblib.load('final_model.pkl')
count_vect = joblib.load('vector.pkl')

def date_convert(input_date):
    format = "%d %B %Y"
    output_date = datetime.datetime.strptime(input_date, format)
    return output_date

# THIS SECTION RETRIEVES THE LATEST DATE AND
# SAVES THE DATE OF THE WEEK BEFORE
today_dt = date_convert(today)
print("Today = ", today)
amazon_DF_clean["Dates"] = amazon_DF_clean["Dates"].apply(lambda x: date_convert(x))
week_prior = today_dt - timedelta(weeks = 1)

# RETRIEVING THE LATEST WEEK OF REVIEWS
DF_latest = amazon_DF_clean[amazon_DF_clean['Dates'] >= week_prior].reset_index(drop = True)
new_reviews = DF_latest.shape[0]

# If there are less than or equal to 10 reviews, show the 20 latest reviews
if new_reviews <= 10:
    DF_latest = amazon_DF_clean.sort_values(by = ['Dates'], ascending = False).head(20)

# SORTING DATES IN DESCENDING ORDER
DF_latest = DF_latest.sort_values(by = ['Dates'], ascending = False).reset_index(drop = True)

###--- CLEANING THE DATA ---### 
def clean(s):
    s = s.lower()                   #Converting to lower case
    s = re.sub(r'[^\w\s]', ' ', s)  #Removing punctuation
    s = re.sub(r'[\d+]', ' ', s)    #Removing Numbers
    s = s.strip()                   #Removing trailing spaces
    s = re.sub(' +', ' ', s)        #Removing extra whitespaces
    return s
    
###--- DATA PREPARATION AND PREDICTION ---###
def pred_result(rev):
    temp = ""
    temp = rev
    temp = clean(temp)
    temp_tokens = word_tokenize(temp)
    temp_final = (" ").join([word for word in temp_tokens if not word in stop_words])
    temp_final = [temp_final]
    vect = count_vect.transform(temp_final).toarray()
    temp_pred = model.predict(vect)
    return temp_pred[0]

###--- CHANGING URL (USER INPUT REVIEWS) ---###
def url_change(link):
    url_list = link.split('/')
    print(url_list)

    if url_list[-1].startswith('ref'):
        del url_list[-1]
    elif '?' in url_list[-1]:
        url_list[-1] = url_list[-1].split('?')[0]
    
    if 'product' in url_list:
        url_list.remove('product')
        
    url_list = ['product-reviews' if item == 'dp' or item == 'gp' else item for item in url_list]
    url_new = "/".join(url_list)
    return url_new
    

@app.route('/')

#####---- HOME PAGE ----#####
@app.route('/home', methods = ['GET', 'POST']) 
def home():
    return render_template('home.html', today = today)

#####---- SHOW LATEST PREDICTIONS FOR LATEST REVIEWS OF PRESTIGE COOKER ----#####

@app.route('/result', methods = ['GET', 'POST']) 
def result():
    DF_latest["Reviews_Clean"] = DF_latest["Reviews"].apply(lambda x: clean(x))
    DF_latest['Label'] = DF_latest["Reviews_Clean"].apply(lambda x: pred_result(x))
    DF_latest_show = DF_latest[["Reviews", "Dates", "Label"]]
    return render_template('result.html', today = today, new_reviews = new_reviews, tables = [DF_latest_show.to_html(classes = 'data', header = "true")])


######--------- REVIEW EXTRACTION ---------#######

@app.route('/scraper', methods = ['GET', 'POST'])
def scraper():
    
    subprocess.call([r'auto-scrape.bat'])
    message = "Data Has Been Updated!"
    return render_template('scraper.html', message = message, today = today)

######--------- USER ENTERS TEXT  ---------#######

@app.route('/input_text', methods = ['GET', 'POST'])
def input_text():
    prediction = ""
    message_by_user = ""
    if request.method == 'POST':
        data = request.form['message']
        message_by_user = data
        data_clean = clean(data)
        prediction = pred_result(data_clean)
        
    return render_template('input.html', today = today, prediction = prediction, message_by_user = message_by_user)


######--------- USER ENTERS URL  ---------#######

@app.route('/input_url', methods = ['GET', 'POST'])
def input_url():
    data = ""
    if request.method == 'POST':
        global url_by_user
        url_by_user = request.form['user_url']
        return redirect(url_for('user_url_scrape'))
    return render_template('input_url.html', today = today)


######--------- USER ENTERED URL GETS SCRAPED  ---------#######    

@app.route('/user_url_scrape', methods = ['GET', 'POST'])
def user_url_scrape():
    url_add_1 = "/ref=cm_cr_getr_d_paging_btm_next_"
    url_add_2 = "?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber="
    user_url = url_by_user
    user_url = url_change(user_url)
    Total_reviews=[]
    dates_list=[]

    ### Extracting reviews from Amazon website ################

    i=1
    while i: 
        rev=[]
        dates=[]
        print(i)
        url= user_url + url_add_1 + str(i) + url_add_2 + str(i)
        header={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'}
        response = requests.get(url)  #, headers=header
        if response.status_code == 503:
            continue
        
        soup = bs(response.content,"html.parser")# creating soup object to iterate over the extracted content 
        reviews = soup.findAll("h3",attrs={"data-hook":re.compile("arp-local-reviews-header")}) #to detect the last page of reviews
        # if len(reviews)==0:
        #     continue
        
        #f=re.search('^([0-9]+)[,]?([0-9]+)?\s\w+\s\w+\s\|\s([0-9]+)[,]?([0-9]+)?',reviews)
        if len(reviews)!=0:
            reviews1 = soup.findAll("span",attrs={"class","a-size-base review-text review-text-content"})  
            dates1 = soup.findAll("span",attrs={"data-hook":re.compile("review-date")})
    
    
        # Extracting the content under specific tags 
            for l in range(len(reviews1)):
                review_comment =reviews1[l].text
                review_comment=review_comment.strip()
             
                #print(review_comment)
                rev.append(review_comment)  
            for m in range(len(dates1)):
                dates_val=dates1[m].text
                dates_val=dates_val.strip()
                dates_val=dates_val.strip("Reviewed in India on ")
                dates.append(dates_val)
            
            dates_list=dates_list+dates    
            Total_reviews=Total_reviews+rev  # adding the reviews of one page to empty list which in future contains all the reviews
            i=i+1       
        else:
            break
        
    review_dict={'Reviews':Total_reviews,'Dates':dates_list}    
    user_data = pd.DataFrame(review_dict)
    user_data.dropna(axis = 0, inplace = True)
    user_data_clean = user_data.copy()  
    user_data_clean["Dates"] = user_data_clean["Dates"].apply(lambda x: date_convert(x))
    user_data_clean = user_data_clean.sort_values(by = ['Dates'], ascending = False)
    user_data_clean.to_csv('User_Product.csv',index = False)  
    user_data_total = user_data_clean.shape[0]
    user_data_clean["Reviews_Clean"] = user_data_clean["Reviews"].apply(lambda x: clean(x))
    user_data_clean["Label"] = user_data_clean["Reviews_Clean"].apply(lambda x: pred_result(x))
    user_data_final = user_data_clean[["Reviews", "Dates", "Label"]]
    
    try:
        pos = user_data_final["Label"].value_counts()['Positive']
    except:
        pos = 0
        
    try:
        neg = user_data_final["Label"].value_counts()['Negative']
    except:
        neg = 0
        
    try:
        neu = user_data_final["Label"].value_counts()['Neutral']
    except:
        neu = 0
        
    user_data_show = user_data_final.head(30).reset_index(drop=True)
    
    return render_template('user_url_scrape.html', today = today, url_by_user = url_by_user, total = user_data_total, pos = pos, neg = neg, neu = neu, tables = [user_data_show.to_html(classes = 'data', header = "true")])



if __name__ == '__main__':
	app.run(debug=True, threaded = 'True')

