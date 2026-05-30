from flask import Flask, render_template, request
from phishing_engine import predict_email

import json

app = Flask(__name__)

# HOME ROUTE

@app.route("/", methods=["GET", "POST"])
def home():

    result = None
    email_text = ""


    # HANDLE PHISHING ANALYSIS

    if request.method == "POST":

        email_text = request.form.get("email_text")

        if email_text:
            result = predict_email(email_text)

    # LOAD ALERTS

    try:

        with open("alerts.json", "r") as file:
            alerts = json.load(file)

    except:
        alerts = []

    # RENDER DASHBOARD

    return render_template(
        "index.html",
        result=result,
        email_text=email_text,
        alerts=alerts
    )

# RUN FLASK APP

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5000
    )