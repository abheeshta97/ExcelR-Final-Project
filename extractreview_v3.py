# -*- coding: utf-8 -*-
"""
Created on Fri Aug 14 14:29:59 2020

@author: user-pc
"""
import re
import requests   # Importing requests to extract content from a url
from bs4 import BeautifulSoup as bs # Beautifulsoup is for web scrapping...used to scrap specific content 
import pandas as pan
from dateutil import parser as dateparser
Total_reviews=[]
dates_list=[]

### Extracting reviews from Amazon website ################


i=1
while i: 
    rev=[]
    dates=[]
    print(i)
    url="https://www.amazon.in/Prestige-PIC-20-Induction-Cooktop/product-reviews/B00YMJ0OI8/ref=cm_cr_getr_d_paging_btm_next_"+str(i)+"?ie=UTF8&reviewerType=all_reviews&sortBy=recent&pageNumber="+str(i)
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
data = pan.DataFrame(review_dict)
data.to_csv('Induction_Data_New.csv',index = False)        

    

    