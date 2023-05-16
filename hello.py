from flask import Flask, request
import json
from datetime import datetime

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test")
def test_endpoint():
    return "Flask app is working!"

def filter(infoData, data):

    currentDate = datetime.today().strftime("%d/%m/%Y")

    defaultDateRange = currentDate.split("/")

    defaultDateRange[0] = str(int(defaultDateRange[0]) - 7)

    if (int(defaultDateRange[0]) < 10):
        defaultDateRange[0] = "0" + defaultDateRange[0]

    subjectData = []

    if "subject" in infoData:
        subject = infoData["subject"]
    else:
        subject = ""
    
    if "region" in infoData:
        region = infoData["region"]
    else:
        region = ""
    
    if "source" in infoData:
        newsOutlet = infoData["source"]
    else:
        newsOutlet = ""

    if infoData["minimumDate"] != "" and infoData["maximumDate"] != "":
        minimumDate = infoData["minimumDate"]
        maximumDate = infoData["maximumDate"]
    else:
        minimumDate = "/".join(defaultDateRange)
        maximumDate = currentDate

    for article in data:
        if (article["subject"].lower() == subject.lower()) or subject == "":
            subjectData.append(article)

    finalData = []

    for article in subjectData:
        publishDate = article["publishDate"].split("/")

        min = minimumDate.split("/")
        max = maximumDate.split("/")

        if int(publishDate[0]) in range(int(min[0]), int(max[0])):
            if ((article["region"] == region or region == "") and (article["source"] == newsOutlet or newsOutlet == "")):
                finalData.append(article)

    return finalData

@app.route("/news")
def get_news():

    args = request.args

    f = open("news.json")
    data = list(json.load(f))

    return filter(args, data) 

if __name__ == "__main__":
    app.run(debug=True)