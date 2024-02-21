from flask import Flask, request, render_template
import requests


app = Flask(__name__)


# By default, a Flask route is set to respond to only GET requests
@app.route("/")
def home():
    """Called when navigating to the home page"""
    return render_template("home.html")


@app.route("/fetch-api", methods=["POST"])
def fetch_api():
    # This function will only run if a POST request is sent to Flask
    if request.method == "POST":
        api_url = request.form["api-url"]

        # API call using requests library and get method
        try:
            raw_resp = requests.get(api_url)
            raw_resp.raise_for_status()
        except:
            return {"error": "Ensure your URL and API key is correct."}

        # Read API response into a Python dictionary
        resp = raw_resp.json()

        # If the caller is outside Python, Flask will return this Python dictionary
        # as a serialized JSON string.
        # This will be useful, for example, for Javascript code calling this endpoint
        return resp
