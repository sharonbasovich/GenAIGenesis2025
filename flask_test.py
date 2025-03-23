from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import PIL.Image
import settings
# Configure the API
genai.configure(api_key="YOUR_API_KEY")
model = genai.GenerativeModel('gemini-2.0-flash')

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/translate_menu', methods=['POST'])
def translate_menu():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    image_file = request.files['image']
    language = request.form.get('language', 'English')
    
    try:
        # Save the uploaded image temporarily
        image_path = './temp_menu.jpg'
        image_file.save(image_path)
        
        # Load the image
        image = PIL.Image.open(image_path)
        
        # Create chat and send message with image
        chat = model.start_chat(history=[])
        prompt = f'1.translate the dishes in the picture to {language}.\n'
        prompt += '2.if the dish does not contain ingredients, just translate the name of the dish to phrase that contains the main ingredients.\n'
        prompt += '3.if the ingredients are too complex, use simplier terms.\n'
        prompt += '4.return the result in json file with the following format: {"dish_name": "translated name of the dish", "original_description": "translated original description", "simplified_description": "translated simplified description"}.\n'
        
        response = chat.send_message([prompt, image])
        
        return jsonify({'translation': response.text})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/analyze_text', methods=['POST'])
def analyze_text():
    data = request.json
    text = data.get('text', '')
    
    language = settings.language_options(text)
    allergies = settings.allergies_options(text)
    dietary = settings.dietary_options(text)
    culture = settings.culture_options(text)
    
    return jsonify({
        'language': language,
        'allergies': allergies,
        'dietary_restrictions': dietary,
        'culture': culture
    })

@app.route('/suggest_dish', methods=['POST'])
def suggest_dish():
    data = request.json
    culture = data.get('culture', '')
    target_dish = data.get('target_dish', '')
    allergies = data.get('allergies', '')
    dietary_restrictions = data.get('dietary_restrictions', '')
    priority = data.get('priority', 'price')
    
    prompt = f"Find a dish similar to {target_dish} in {culture} cuisine. The dish should avoid {allergies}, respect {dietary_restrictions}, and prioritize {priority}."
    response = model.generate(prompt)
    
    return jsonify({'suggestion': response.text})

if __name__ == '__main__':
    app.run(debug=True)
