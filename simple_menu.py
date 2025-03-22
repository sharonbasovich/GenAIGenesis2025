import google.generativeai as genai
import PIL.Image  # For image handling

GEMINI_API_KEY = "AIzaSyDaNd1nu-hc4tibF9wEd5MyE6yUByk5zt8"
genai.configure(api_key=GEMINI_API_KEY)


model = genai.GenerativeModel('models/gemini-2.0-flash')
chat = model.start_chat(history=[])
def load_image(image_path):

    img = PIL.Image.open(image_path)
    return img
image_path = './menus/menu2.jpg' #pictures of user takes
image = load_image(image_path)
language = "English" #change depending on user's selection
prompt = '1.translate the menu to ' + language + '.\n'
prompt += '2.if the dish does not contain ingredients, just translate the name of the dish to phrase that is easy to understand.\n'

response = chat.send_message([prompt, image])


print(response.text)


