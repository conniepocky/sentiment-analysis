from flask import Flask, request
import json
from datetime import datetime
from flask_cors import CORS, cross_origin
from flask import jsonify

app = Flask(__name__)

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
        if "/" not in infoData["minimumDate"] or "/" not in infoData["maximumDate"] or any(i.isalpha() for i in infoData["maximumDate"]) or any(i.isalpha() for i in infoData["minimumDate"]):
            return "Please input the dates in the format DD/MM/YY"
        else:
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
            if ((article["region"].lower() == region.lower() or region == "") and (article["source"].lower() == newsOutlet.lower() or newsOutlet == "")):
                finalData.append(article)

    return finalData

@app.route("/news", methods=["GET"])
def get_news():

    args = request.args

    f = open("news.json")
    data = list(json.load(f))

    data = filter(args, data) 

    response = jsonify(data)
    response.headers.add("Access-Control-Allow-Origin", "*")

    return response

if __name__ == "__main__":
    app.run(debug=True)