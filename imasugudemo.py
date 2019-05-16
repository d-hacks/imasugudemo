# coding: utf-8

from flask import Flask, render_template, request, Response
import json

app = Flask(__name__)

@app.route("/")
def index():
   return render_template('index.html')

@app.route('/show_input_text', methods=['POST'])
def show_input_text():
    input_text = request.json['input_text']
    return Response(json.dumps({ 'text': input_text }))

@app.route('/show_input_image', methods=['POST'])
def show_input_image():
    input_image_file = request.files['file']
    image_filename = "input_image.png"
    image_save_path = "./static/img/" + image_filename
    input_image_file.save(image_save_path)
    return Response(json.dumps({ 'image_filename': image_filename }))


if __name__ == "__main__":
    # app.run(debug=True)
    app.run(host='0.0.0.0')
