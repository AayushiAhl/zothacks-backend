import ast

from google.cloud import vision
import google.generativeai as genai
import os
import base64
from PIL import Image
import math


def get_labels(image_path) -> vision.EntityAnnotation:
    """Provides a quick start example for Cloud Vision."""

    # Instantiates a client
    client = vision.ImageAnnotatorClient()

    # Decode the base64 string
    image_data = base64.b64decode(image_path)
    dict_str = image_data.decode("UTF-8")
    mydata = ast.literal_eval(dict_str)

    # Create an Image object from the binary data
    image = vision.Image(content=mydata)

    # Performs label detection on the image file
    label_response = client.label_detection(image=image)
    #object_response = client.object_detection(image=image)
    labels = label_response.label_annotations
    #objects = object_response.object_annotations

    '''
    print("Labels:")
    for label in labels:
        print(label.description)
    '''
    #for object in objects:
    #    print(object.description)

    return labels

def image_classifier(image_path):
    labels = get_labels(image_path)
    output = []
    for index in range(len(labels)):
        print(labels[index])
        output.append(labels[index].description.lower())
    if 'food' in output:
        return food_classifier(output, image_path)
    elif 'clothing' in output:
        return clothing_classifier(output, image_path)
    else:
        return other_classifier(output, image_path)



def other_classifier(labels, image_path):
    isDonatable = ask_gemini("Yes or No: You are a quality analyzer. Can this item be donated?", image_path)
    message = f"Your item wasn't classified as a food or clothing but was classified as {labels[0]}."

    print(isDonatable, f"{message} Your item is {'donatable' if isDonatable else "not donatable"}.", "other")

    return isDonatable, f"{message} Your item is {'donatable' if isDonatable else "not donatable"}.", "other"

def food_classifier(labels: list[str], image_path) -> (str, bool):
    if {'fruit', 'produce', 'natural foods', 'vegetable', 'plant'}.intersection(labels):
        return (False, "Your item is identified as fresh produce, and thus isn't suitable for donation due to it's perishability.", "food")
    elif {'canned packaged goods', 'canned goods'}.intersection(labels):
        isDonatable = ask_gemini("Yes or No: Is this canned food unopened and is it in a condition to be donated?")
        if not isDonatable:
            message = "However, it was detected that your canned good is open, and thus isn't in a condition that can be donated"
        else:
            message = "Your canned good is in a condition that can be donated!"
        return (isDonatable, f"Your item is identified as a canned food. {message}", "food")
    else:
        isDonatable = ask_gemini("Yes or No: Is this food in a condition to be donated to a shelter?")
        if not isDonatable:
            message = "However, it was detected that your food item cannot be donated."
        else:
            message = "Your food item can be donated!"
        return isDonatable, f"Your food wasn't identified in a specific category but is classified as {labels[0]}. {message}", "food"


def clothing_classifier(labels: list[int], image_path) -> (str, bool):
    clothing_item = None
    if {"top", "shirt", "dress shirt", "t-shirt", "crop top", "blouse", "tank top", "tank", "jacket", "sweater", "hoodie", "sweatshirt"}.intersection(labels):
        clothing_item = "top"
    elif {"active pants", "pants", "jeans", "cargo pants", "leggings", "sweatpants"}.intersection(labels):
        clothing_item = "bottom"
    else:
        clothing_item = "couldn't identify"
    isDonatable = ask_gemini("Yes or No: Is this clothing in wearable condition?")

    print(isDonatable, f"Your {clothing_item} is {'donatable' if isDonatable else "not donatable"}.", "clothing")

    return isDonatable, f"Your {clothing_item} is {'donatable' if isDonatable else "not donatable"}.", "clothing"


def ask_gemini(prompt: str, image_path):
    genai.configure(api_key="AIzaSyBoo4j8X8MD0k9zQK9JFvgAphKjVTbOmSE")

    model = genai.GenerativeModel("gemini-1.5-flash")

    img = Image.open("/Users/jisharajala/Desktop/Screenshot 2024-11-02 at 7.48.40 PM.png")
    # Generate response with the encoded image
    response = model.generate_content(
        [
            prompt,
            img
        ]
    )

    print(response.text)
    return ('Yes' == response.text[:3])


ask_gemini("Yes or No. You are a quality analyzer. Can this item be donated?")

image_classifier(get_labels())