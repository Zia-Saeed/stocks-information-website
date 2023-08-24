import requests
from flask import Flask, render_template, request, redirect, url_for, flash
import random
import os


app = Flask(__name__)
app.config["SECRET_KEY"] = "12kjhwsjkdhf02u3jhsdkjfh923ihskd"


@app.route("/", methods=["POST", "GET"])
def home():
    header_companies_data = {
        "Microsoft Corporation (MSFT)": "",
        "Apple Inc. (AAPL)": "",
        "Tesla, Inc.(TSLA)": "",
        "Amazon.com Inc.(AMZN)": "",
    }
    params = {
        "access_key": os.getenv("api_key"),
        "symbols": "MSFT,AAPL,TSLA,AMZN"
    }
    api_result = requests.get("http://api.marketstack.com/v1/eod/latest", params)
    api_response = api_result.json()
    head_data = api_response['data']
    index = 0
    for key in header_companies_data:
        header_companies_data[key] = head_data[index]
        index += 1

    if request.method == "GET":
        company_list = ["MSFT", "AAPL", "TSLA", "GOOGL", "SSNLF", "AMZN", "NVDA", "AMD", "INTC"]
        rand_comp = random.choice(company_list)
        demo_data = []

        params = {
            'access_key': os.getenv("api_key"),
            "symbols": f"{rand_comp}"
        }

        api_result = requests.get('http://api.marketstack.com/v1/intraday', params)
        api_response = api_result.json()
        data = api_response['data']

        for dat in range(10):
            demo_data.append(data[dat])

        return render_template("index.html", rand_data=demo_data, head_dat=header_companies_data)

    if request.method == "POST":
        company = request.form.get("company-name")
        params = {
            'access_key': os.getenv("api_key"),
            "symbols": f"{company}"
        }

        api_result = requests.get('http://api.marketstack.com/v1/intraday', params)
        api_response = api_result.json()

        try:
            data = api_response["data"]
            return render_template("index.html", data=data, head_dat=header_companies_data)

        except Exception:
            flash("Invalid Stock Name! Stock Name should be like TSLA for (Tesla, inc).")
            return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)




