import google.generativeai as genai
import PIL.Image  # For image handling

genai.configure(api_key="YOUR_API_KEY")

model = genai.GenerativeModel('gemini-2.0-flash')
chat = model.start_chat(history=[])
def load_image(image_path):

    img = PIL.Image.open(image_path)
    return img
image_path = './menus/menu3.jpg' #pictures of user takes
image = load_image(image_path)
language = "Chinese" #change depending on user's selection
prompt = f'1.translate the dishes in the picture to {language}.\n'
prompt += '2.if the dish does not contain ingredients, just translate the name of the dish to phrase that contains the main ingredients.\n'
prompt += '3.if the ingredients are too complex, use simplier terms.\n'
prompt += '4.return the result in json file with the following format: {"dish_name": "translated name of the dish", "original_description": "translated original description", "simplified_description": "translated simplified description"}.\n'

response = chat.send_message([prompt, image])


print(response.text)


