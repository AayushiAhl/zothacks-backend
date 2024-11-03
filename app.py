from flask import Flask, request, render_template, json
import requests
from flask_cors import CORS  # Import CORS
import base64
from image_classification import get_labels, image_classifier

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# By default, a Flask route is set to respond to only GET requests
@app.route("/")
def home():
    """Called when navigating to the home page"""
    return render_template("home.html")

@app.route("/search", methods=['POST'])
def search_route():
    # result = classify_image()
    #
    # result[]

    # Get the radius parameter from the URL query string
    radius_miles = int(request.args.get('radius', 5))  # Default to 5 miles if not specified
    filter_food_bank = request.args.get('food_bank', 'false').lower() == 'true'
    filter_clothing = request.args.get('clothing', 'false').lower() == 'true'
    filter_goodwill = request.args.get('goodwill', 'false').lower() == 'true'

    data = request.json
    b64_image = data.get('image')  # Assuming the image is sent as 'image'

    foo = image_classifier(get_labels(b64_image))
    print(foo)

    # Remove the header if it exists
    if b64_image.startswith('data:image/png;base64,'):
        b64_image = b64_image.replace('data:image/png;base64,', '')

    image_data = base64.b64decode(b64_image)



    print(radius_miles)

    filtered_result = search(radius_miles, filter_food_bank=filter_food_bank, filter_clothing=filter_clothing,
                             filter_goodwill=filter_goodwill)  # Filtered results for all
    unfiltered_result = search(radius_miles, filter_food_bank=True, filter_clothing=True,
                               filter_goodwill=True)  # Results only filtered by location/radius

    result = {
        "filtered": [filtered_result],
        "unfiltered": [unfiltered_result]
    }

    return result

def search(radius_miles, filter_food_bank=False, filter_clothing=False, filter_goodwill=False):
    url = "https://api.yelp.com/v3/businesses/search"

    # Convert miles to meters (1 mile = 1609.34 meters)
    radius_options = {5: 5 * 1609, 10: 10 * 1609, 25: 24 * 1609}
    radius_meters = radius_options.get(radius_miles, 1609)  # Default to 1 mile if invalid input

    querystring = {"location": "irvine", "term": "donation center", "radius": radius_meters}

    payload = ""
    headers = {
        "User-Agent": "insomnia/10.1.1",
        "Authorization": "Bearer 4EPvJ1pOp009xRw3T3YVHqJtbdG3a1Iy_SxqeScFtjjhn3U_L3u7r6-6-H7DPjsWyEDzuKBxiYoILnt2M1bUQEfgP6yTwuK381fGRMjxGwIh3AbMOwj5E7cJIe4mZ3Yx"
    }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    # Parse the response as JSON
    data = response.json()

    # Filter results if the user wants only "food bank" donation centers
    if filter_food_bank:
        filtered_results = [
            business for business in data.get("businesses", [])
            if "food bank" in business.get("name", "").lower() or
               any("food bank" in category["title"].lower() for category in business.get("categories", [])) or
               "salvation" in business.get("name", "").lower() or
               any("salvation" in category["title"].lower() for category in business.get("categories", [])) or
               "food" in business.get("name", "").lower() or
               any("food" in category["title"].lower() for category in business.get("categories", []))
        ]
        print(json.dumps(filtered_results, indent=2))
        return json.dumps({"businesses": filtered_results})
    else:
        filtered_results = data.get("businesses", [])

    # Filter results if the user wants only "clothing" donation centers
    if filter_clothing:
        filtered_clothing_results = [
            business for business in data.get("businesses", [])
            if "clothing" in business.get("name", "").lower() or
                any("clothing" in category["title"].lower() for category in business.get("categories", [])) or
               "cloth" in business.get("name", "").lower() or
               any("cloth" in category["title"].lower() for category in business.get("categories", [])) or
               "thrift" in business.get("name", "").lower() or
               any("thrift" in category["title"].lower() for category in business.get("categories", []))
        ]
        print(json.dumps(filtered_clothing_results, indent=2))
        return json.dumps({"businesses": filtered_clothing_results})
    else:
        filtered_clothing_results = data.get("businesses", [])

    # If item miscellaneous (not food and not clothing) label miscellaneous and direct to Goodwill
    if filter_goodwill:
        filtered_goodwill_results = [
            business for business in data.get("businesses", [])
            if "goodwill" in business.get("name", "").lower()
        ]
        print(json.dumps(filtered_goodwill_results, indent=2))
        return json.dumps({"businesses": filtered_goodwill_results})
    else:
        filtered_goodwill_results = data.get("businesses", [])

@app.route("/fetch-api", methods=["POST"])
def fetch_api():
    if request.method == "POST":
        api_url = request.form["api-url"]

        try:
            raw_resp = requests.get(api_url)
            raw_resp.raise_for_status()
        except requests.exceptions.RequestException as e:
            return {
                "error": f"Ensure your URL and API key are correct. Error message: {e}"
            }

        resp = raw_resp.json()
        return resp