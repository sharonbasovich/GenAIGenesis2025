import google.generativeai as genai
import PIL.Image  # For image handling

GEMINI_API_KEY = "AIzaSyDaNd1nu-hc4tibF9wEd5MyE6yUByk5zt8"
genai.configure(api_key=GEMINI_API_KEY)


model = genai.GenerativeModel('models/gemini-2.0-flash')
chat = model.start_chat(history=[])
def load_image(image_path):

    img = PIL.Image.open(image_path)
    return img
image_path = './menus/menu3.jpg' #pictures of user takes
image = load_image(image_path)
language = "English" #change depending on user's selection
prompt = '1.summerize the menu to ' + language + '.\n'
prompt += '2.if shown, tell the user the average price of the dishes.\n'
prompt += '3.tell the user what ingredients mainly used in this menu.\n'

response = chat.send_message([prompt, image])


print(response.text)