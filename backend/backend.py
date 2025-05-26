from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import json
import os
import time
from datetime import datetime
from picamera2 import Picamera2  # NEW

app = Flask(__name__)
CORS(app)

# Load the model and class names
model = tf.keras.models.load_model('pokedex_model.h5')
with open('class_names.txt', 'r') as f:
    class_names = [line.strip() for line in f.readlines()]

# Load Pokédex data
with open('pokedex_data.json', 'r') as f:
    pokedex_data = json.load(f)

# Ensure static directory exists
os.makedirs('static', exist_ok=True)

# Initialize favorites list
FAVORITES_FILE = 'favorites.json'
if not os.path.exists(FAVORITES_FILE):
    with open(FAVORITES_FILE, 'w') as f:
        json.dump({'collection': []}, f)

def load_favorites():
    with open(FAVORITES_FILE, 'r') as f:
        return json.load(f)

def save_favorites(favorites):
    with open(FAVORITES_FILE, 'w') as f:
        json.dump(favorites, f)

@app.route('/capture', methods=['POST'])
def capture():
    try:
        IMAGE_PATH = os.path.join("static", "latest.jpg")
        picam2 = Picamera2()
        picam2.configure(picam2.create_still_configuration())
        picam2.start()
        time.sleep(1)  # allow camera to warm up
        picam2.capture_file(IMAGE_PATH)
        picam2.close()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': f'Camera error: {str(e)}'}), 500

@app.route('/predict', methods=['GET'])
def predict():
    try:
        img = Image.open('static/latest.jpg')
        img = img.resize((224, 224))
        img_array = np.array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)

        predictions = model.predict(img_array)
        predicted_class = class_names[np.argmax(predictions[0])]
        confidence = float(predictions[0][np.argmax(predictions[0])])

        pokemon_info = pokedex_data.get(predicted_class, {})

        return jsonify({
            'name': predicted_class,
            'confidence': confidence,
            'type': pokemon_info.get('type', 'Unknown'),
            'hp': pokemon_info.get('hp', 0),
            'evolves_to': pokemon_info.get('evolves_to', 'None'),
            'attacks': pokemon_info.get('attacks', []),
            'desc': pokemon_info.get('desc', 'No description available')
        })
    except Exception as e:
        import traceback
        print("Error in predict endpoint:")
        print(traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@app.route('/favorite', methods=['POST'])
def favorite():
    try:
        favorites = load_favorites()
        pokemon_name = request.json.get('name')

        if not pokemon_name:
            return jsonify({'error': 'No Pokémon name provided'}), 400

        if pokemon_name not in favorites['collection']:
            favorites['collection'].append(pokemon_name)
            save_favorites(favorites)

        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/collection', methods=['GET'])
def collection():
    try:
        favorites = load_favorites()
        return jsonify(favorites)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/latest.jpg')
def latest_image():
    return send_from_directory('static', 'latest.jpg')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)