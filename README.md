# ExcelR Project: Review Analysis for a Given Product on Amazon
# Objective
Analyzing customer reviews of a given default product on Amazon and building a model to classify reviews according to sentiment (Positive, Negative or Neutral). The reviews should be automatically updated every week. The default product here is the [Prestige PIC 20 Induction Cooktop](https://www.amazon.in/Prestige-PIC-20-Induction-Cooktop/dp/B00YMJ0OI8).
# Tools/Tech Used
This program has been built using the following tools:
  * Python 3.6+
  * Flask
  * HTML/CSS
  * Windows Task Scheduler
# Features
  * The user can view the predictions of sentiments of reviews that were posted in the current week.
  * The user can enter a body of text and the prediction model will predict the sentiment of the entered text.
  * The user can enter the URL of any product on Amazon India. The reviews for this product will be scraped and the 30 latest reviews, along with their predictions, will be displayed.
  * The user can manually update the dataset for the default product.
# About The Files/Folders
  ## [app.py](https://github.com/abheeshta97/ExcelR-Final-Project/blob/main/app.py)
  This is the main Python program that runs the Flask application.
  ## [extractreview_v3.py](https://github.com/abheeshta97/ExcelR-Final-Project/blob/main/extractreview_v3.py)
  This program is responsible for scraping the Amazon reviews for the default product.
  ## [auto-scrape.bat](https://github.com/abheeshta97/ExcelR-Final-Project/blob/main/auto-scrape.bat)
  This is a batch file, that runs "extractreview_v3.py". This batch file is automatically run by the Windows Task Scheduler every Friday at 3pm.
  ## [final_model.py](https://github.com/abheeshta97/ExcelR-Final-Project/blob/main/final_model.py)
  The ML model used here for prediction is Linear Support Vector Classifiers (SVC). It was able to achieve a test accuracy of almost 92%. The program also contains a Count Vectorizer, which is convert a collection of text documents to a vector of term counts [[SOURCE]](https://www.educative.io/edpresso/countvectorizer-in-python).
  ## [final_model.pkl](https://github.com/abheeshta97/ExcelR-Final-Project/blob/main/final_model.pkl)
  This is a serialized file that contains the pre-trained ML model mentioned earlier. Serialization is the process of converting structured data to a format that allows sharing or storage of the data in a form that allows recovery of its original structure [[SOURCE]](https://docs.python-guide.org/scenarios/serialization/). This serialized file makes it easier to load the pre-trained model in "app.py" when needed for predictions.
  ## [vector.pkl](https://github.com/abheeshta97/ExcelR-Final-Project/blob/main/vector.pkl)
  This is a serialized file that contains the Count Vectorizer and can be loaded in the "app.py".
  ## [Induction_Data_New.csv](https://github.com/abheeshta97/ExcelR-Final-Project/blob/main/Induction_Data_New.csv)
  This is a dataset that contains all the extracted reviews of the default product.
  ## [templates](https://github.com/abheeshta97/ExcelR-Final-Project/tree/main/templates)
  This folder contains the following HTML files.
  * [home.html](https://github.com/abheeshta97/ExcelR-Final-Project/blob/main/templates/home.html): Home page of the web application
  * [result.html](https://github.com/abheeshta97/ExcelR-Final-Project/blob/main/templates/result.html): Show the latest reviews for the default product, along with the model's predictions
  * [input.html](https://github.com/abheeshta97/ExcelR-Final-Project/blob/main/templates/input.html): This takes a body of text of the user's choice as an input and outputs the prediction of the sentiment of the input.
  * [input_url.html](https://github.com/abheeshta97/ExcelR-Final-Project/blob/main/templates/input_url.html): This takes an Amazon India product URL of the user's choice as an input. The reviews for the product will be extracted.
  * [user_url_scrape.html](https://github.com/abheeshta97/ExcelR-Final-Project/blob/main/templates/user_url_scrape.html): This outputs the 30 latest reviews for the user provided product along with their predictions.
  * [scraper.html](https://github.com/abheeshta97/ExcelR-Final-Project/blob/main/templates/scraper.html): This gives the user to manually update the data for the default product.
  ## [static](https://github.com/abheeshta97/ExcelR-Final-Project/tree/main/static)
  This folder contains "style.css". The CSS file helps in the formatting of the layout of the contents of a webpage.




   
    

