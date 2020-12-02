from flask import Flask, render_template, request
import os

import io
from base64 import encodebytes
from PIL import Image

from compress import Compress

app = Flask(__name__, static_url_path = "/")
app.config['SECRET_KEY'] = 'dcdfbdgdvscdvfbdvs'
app.config['uploads'] = "static/uploads"
app.config['compress_path'] = "static/compressed"


@app.route('/')
def index():
	return render_template('index.html')

@app.route('/compress/', methods = ["POST", "GET"])
def compress():
  if request.method == "POST":
    if request.files:
      content_type = request.mimetype
      image = request.files['image']
      image.save(os.path.join(app.config['uploads'], image.filename))

      path = Compress(os.path.join(app.config['uploads'], image.filename),1)
      encoded_img = get_response_image(os.path.join(app.config['compress_path'], path))
      response = {"message": "saved", "encoded_img": encoded_img}
      return response, 200

def get_response_image(image_path):
  pil_img = Image.open(image_path, mode='r') # reads the PIL image
  byte_arr = io.BytesIO()
  pil_img.save(byte_arr, format='PNG') # convert the PIL image to byte array
  encoded_img = encodebytes(byte_arr.getvalue()).decode('ascii') # encode as base64
  return encoded_img


if __name__ == '__main__':
	app.run(host="0.0.0.0", debug = True)