from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Replace these with your actual Google API credentials
API_KEY = "your_google_api_key"  # Get from Google Cloud Console
CX = "your_custom_search_engine_id"  # Get from Google Programmable Search

def get_plant_images(plant_name):
    """ Fetches images from .org, .net, and .edu domains. """
    url = f"https://www.googleapis.com/customsearch/v1?q={plant_name}&searchType=image&siteSearchFilter=i&siteSearch=.org|.net|.edu&key={API_KEY}&cx={CX}"
    response = requests.get(url).json()
    images = [item['link'] for item in response.get("items", [])]
    return images[:3]  # Return top 3 images

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json()
    plant_name = req["queryResult"]["parameters"].get("plant_name", "")

    if not plant_name:
        return jsonify({"fulfillmentText": "I couldn't find that plant. Please try again."})

    images = get_plant_images(plant_name)
    if not images:
        return jsonify({"fulfillmentText": "No images found for this plant."})

    response_text = f"Here are images of {plant_name}: \n" + "\n".join(images)
    return jsonify({"fulfillmentText": response_text})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
