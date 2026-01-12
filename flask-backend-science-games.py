# app.py

import base64
from flask import Flask, request, render_template, jsonify
from openai import OpenAI
from logic import validate_and_process

app = Flask(__name__)
client = OpenAI()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    user_input = request.form["future"].lower()
    date_answer = request.form["time"].lower()

    result, error = validate_and_process(user_input, date_answer)
    if error:
        return jsonify(error=error)

    key_words, TIME = result

    prompt = (
        f"A family-friendly, artistic illustration of humans "
        f"{TIME} years in the future, influenced by the following conditions: "
        f"{key_words}. Make it family friendly."
    )

    image = client.images.generate(
        model="gpt-image-1",
        prompt=prompt,
        size="1024x1024"
    )

    image_base64 = image.data[0].b64_json
    return jsonify(image=image_base64)

if __name__ == "__main__":
    app.run(debug=True)
