import requests
from flask import Flask, jsonify, request
from PIL import Image

app = Flask(__name__)

def count_black_pixels(image_url):
    response = requests.get(image_url, stream=True)
    response.raw.decode_content = True
    image = Image.open(response.raw)
    image = image.convert("RGB")
    pixels = image.load()
    width, height = image.size
    count = 0
    for y in range(height):
        for x in range(width):
            r, g, b = pixels[x, y]
            if r == 0 and g == 0 and b == 0:
                count += 1
    return count

@app.route('/', methods=['POST'])
def count_black_pixels_api():
    data = request.get_json()
    image_url = data.get('image_url')
    if not image_url:
        return jsonify(error='No image URL provided'), 400
    try:
        count = count_black_pixels(image_url)
        return jsonify(black_pixels=count)
    except Exception as e:
        return jsonify(error=str(e)), 500

if __name__ == '__main__':
    app.run()

