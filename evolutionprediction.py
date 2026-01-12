import base64
from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI

app = Flask(__name__)
client = OpenAI()

all_key_words = [
    "war", "plague", "pandemics", "natural disasters", "climate change",
    "pollution", "air pollution", "water pollution", "poverty", "hunger",
    "malnutrition", "clean water", "disease", "mental illness", "stress",
    "anxiety", "depression", "loneliness", "social isolation"
]

TIME_VALUES = {
    "year": 1,
    "century": 100,
    "centary": 100,
    "millennium": 1000,
    "millenium": 1000,
    "milenium": 1000,
    "millennia": 1000,
    "millenia": 1000,
    "milenia": 1000,
}

@app.route("/")
def serve_page():
    return send_from_directory(".", "evolution prediction.html")

@app.route("/generate", methods=["POST"])
def generate():
    future = request.form["future"].lower()
    time_input = request.form["time"].lower()

    key_words = [w for w in all_key_words if w in future]

    number = None
    unit = None
    for word in time_input.split():
        if word.isdigit():
            number = int(word)
        if word in TIME_VALUES:
            unit = word

    if not number or not unit:
        return jsonify(error="Please enter time like: 100 years")

    TIME = number * TIME_VALUES[unit]

    prompt = (
        f"A family-friendly, artistic illustration of humans "
        f"{TIME} years in the future, influenced by: {key_words}. "
        f"Make it family friendly."
    )

    image = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    return jsonify(image=image.data[0].b64_json), 

if __name__ == "__main__":
    app.run(debug=True)
