import json 
from datetime import datetime 
import re
import matplotlib.pyplot as plt
import numpy as np
import requests

currentDate = datetime.today().strftime("%d/%m/%Y")

defaultDateRange = currentDate.split("/")

defaultDateRange[0] = str(int(defaultDateRange[0]) - 7)

if (int(defaultDateRange[0]) < 10):
    defaultDateRange[0] = "0" + defaultDateRange[0]

# f = open("news.json")
# data = list(json.load(f))

info = open("settings.json")
infoData = dict(json.load(info))

subject = infoData["subject"]
region = infoData["region"]
source = infoData["newsOutlet"]
minimumDate = infoData["minimumDate"]
maximumDate = infoData["maximumDate"]

try:
    f = requests.get(f"http://127.0.0.1:5000/news?subject={subject}&region={region}&source={source}&minimumDate={minimumDate}&maximumDate={maximumDate}").json()
except:
    print("Could not reach the server")
    exit()

finalData = f

def sentimentAnalysis(): 
    outcomes = []
    positiveArticles = []
    negativeArticles = []
    neutralArticles = []

    for article in finalData:
        positivePoints = 0
        negativePoints = 0

        for word in article["content"].split(" "):
            with open("positive.txt") as file:
                contents = file.readlines()
                positiveWords = []
                for i in range(len(contents)):
                    positiveWords.append(contents[i].strip())
                
                if word in positiveWords:
                    #print(word + " is positive")
                    positivePoints += 1

            with open("negative.txt") as file:
                contents = file.readlines()
                negativeWords = []

                for i,v in enumerate(contents):
                    negativeWords.append(contents[i].strip())

                if word in negativeWords:
                    #print(word + " is negative")
                    negativePoints += 1

        if positivePoints > negativePoints:
            positiveArticles.append(article)
            outcomes.append("Positive")
        elif negativePoints > positivePoints:
            negativeArticles.append(article)
            outcomes.append("Negative")
        else:
            neutralArticles.append(article)
            outcomes.append("Neutral")

    #scores

    pos = 0
    neg = 0
    neutral = 0

    for i in outcomes:
        if i == "Positive":
            pos += 1
        elif i == "Negative":
            neg += 1
        elif i == "Neutral":
            neutral += 1

    positivePercent = round((pos / len(outcomes)) * 100)
    negativePercent = round((neg / len(outcomes)) * 100)
    neutralPercent = round((neutral / len(outcomes)) * 100)

    print("Positive percent - " + str(positivePercent))
    print("Negative percent - " + str(negativePercent))
    print("Neutral percent - " + str(neutralPercent))
    
    print("\nPositive Articles\n")

    if len(positiveArticles) > 1:
        for i in range(len(positiveArticles)):
            if i >= 2:
                break

            print(positiveArticles[i]["title"])
            print(positiveArticles[i]["publishDate"])
            print(positiveArticles[i]["source"])
    else:
        print("n/a")

    print("\nNegative Articles\n")

    if len(negativeArticles) > 1:
        for i in range(len(negativeArticles)):
            if i >= 2:
                break

            print(negativeArticles[i]["title"])
            print(negativeArticles[i]["publishDate"])
            print(negativeArticles[i]["source"])

        print("\nNeutral Articles\n")
    else:
        print("n/a")

    if len(neutralArticles) > 1:
        for i in range(len(neutralArticles)):
            if i >= 2:
                break

            print(neutralArticles[i]["title"])
            print(neutralArticles[i]["publishDate"])
            print(neutralArticles[i]["source"])
    else:
        print("n/a")

    #plotting graph

    arr = []
    labels = []
    colors = []

    for i,v in enumerate([positivePercent, negativePercent, neutralPercent]):
        if v != 0:
            if i == 0:
                labels.append("Positive Articles")
                colors.append("#4CAF50")
            elif i == 1:
                labels.append("Negative Articles")
                colors.append("#DA2222")
            elif i == 2:
                labels.append("Neutral articles")
                colors.append("hotpink")
            arr.append(v)

    print(arr)
    y = np.array(arr)

    plt.pie(y, labels=labels, autopct="%1.1f%%", colors=colors)
    plt.title("Article Sentiment Analysis", fontsize=20)
    plt.show()

sentimentAnalysis()