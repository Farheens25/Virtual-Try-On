from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

API_KEY = "5abb0f003b05c78338c930a3947e875e"  # Replace with your OpenWeatherMap API key

# Suggest outfit based on temp and weather
def suggest_outfit(temp, weather):
    outfit = ""
    image = ""

    if temp < 10:
        outfit = "Jacket and warm clothes"
        image = "/static/images/jacket.png"
    elif temp < 20:
        outfit = "Light jacket or full sleeves"
        image = "/static/images/light_jacket.png"
    elif temp < 30:
        outfit = "T-shirt and jeans"
        image = "/static/images/tshirt_jeans.png"

    else:
        outfit = "Light cotton clothes"
        image = "/static/images/cotton_clothes.png"

    if "rain" in weather.lower():
        outfit += " + Umbrella"
        image = "/static/images/umbrella.png"
    elif "snow" in weather.lower():
        outfit += " + Gloves & Scarf"
        image = "/static/images/snow.png"

    return outfit, image

# Home page
@app.route("/")
def home():
    return render_template("index.html")

# Outfit API
@app.route("/outfit")
def outfit():
    city = request.args.get("city")
    if not city:
        return jsonify({"error": "City is required"}), 400

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url).json()

    if response.get("cod") != 200:
        return jsonify({"error": f"City '{city}' not found"}), 404

    temp = response["main"]["temp"]
    weather = response["weather"][0]["main"]

    outfit_suggestion, image_file = suggest_outfit(temp, weather)

    return jsonify({
        "city": city,
        "temperature": temp,
        "weather": weather,
        "outfit": outfit_suggestion,
        "image": image_file
    })

if __name__ == "__main__":
    app.run(debug=True)
