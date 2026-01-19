from flask import Flask, request, send_file
import requests
from io import BytesIO
from PIL import Image
import os

app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def index():
    with open(os.path.join(BASE_DIR, "index.html"), encoding="utf-8") as f:
        return f.read()

@app.route("/merge")
def merge():
    img_url = request.args.get("url")
    race = request.args.get("race", "normal").lower().strip()

    # white == normal
    if race == "white":
        race = "normal"

    glicksman_files = {
        "normal": "normal.png",
        "asian": "asian.png",
        "black": "black.png",
        "indian": "indian.png",
        "hispanic": "hispanic.png",
        "israeli": "israeli.png",
        "british": "british.png"
    }

    # Fetch background image (server-side → no CORS)
    response = requests.get(img_url, timeout=15)
    response.raise_for_status()

    bg = Image.open(BytesIO(response.content)).convert("RGBA")

    glicks_path = os.path.join(
        BASE_DIR,
        glicksman_files.get(race, "normal.png")
    )
    glicks = Image.open(glicks_path).convert("RGBA")

    # Resize Glicksman
    size = min(bg.width, bg.height) // 2
    glicks = glicks.resize((size, size), Image.LANCZOS)

    # Center placement
    x = (bg.width - size) // 2
    y = (bg.height - size) // 2

    bg.paste(glicks, (x, y), glicks)

    output = BytesIO()
    bg.save(output, format="PNG")
    output.seek(0)

    return send_file(output, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)