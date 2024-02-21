from flask import Flask, render_template
from requests.exceptions import HTTPError
import requests

app = Flask(__name__)

# Replace YOUR-API-KEY with your API key in order for the API call to work
key_header = {"x-api-key": "YOUR-API-KEY"}

# The API url that you are calling
# For more info, see https://developers.thecatapi.com/view-account/ylX4blBYT9FaoVd6OhvR?report=bOoHBz-8t
api_url = "https://api.thecatapi.com/v1/images/search?has_breeds=1"


@app.route("/")
def home():
    """Called when navigating to the home page"""
    # Try to call API and return an error message if any errors occur
    try:
        cat_info = acquire_cat()
    except HTTPError as err:
        return err.response.text

    # Returns a rendered html file with the name, description, and img_url args
    # The args are used for the Jinja templating in home.html
    return render_template(
        "home.html",
        name=cat_info["name"],
        description=cat_info["description"],
        img_url=cat_info["img_url"],
    )


@app.route("/acquire-cat")
def acquire_cat():
    # API call using requests library and get method
    raw_resp = requests.get(
        api_url,
        headers=key_header,
    )
    raw_resp.raise_for_status()

    # Read API response into a Python dictionary
    resp = raw_resp.json()

    # Extract exact dictionary from API response
    cat_info = resp[0]["breeds"][0]

    # If the caller is outside Python, Flask will return this Python dictionary
    # as a serialized JSON string.
    # This will be useful, for example, for Javascript code calling this endpoint
    return {
        "name": cat_info["name"],
        "description": cat_info["description"],
        "img_url": resp[0]["url"],
    }
