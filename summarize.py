import google.generativeai as genai
import PIL.Image  # For image handling

genai.configure(api_key="AIzaSyCCTK90t4X7SVmmFHHbwRtI8u5sk_b7DZE")

model = genai.GenerativeModel('gemini-2.0-flash')
chat = model.start_chat(history=[])
def load_image(image_path):

    img = PIL.Image.open(image_path)
    return img
image_path = './menus/menu2.jpg' #pictures of user takes
image = load_image(image_path)
language = "English" #change depending on user's selection
prompt = '1.translate the menu to ' + language + '.\n'
prompt += '2.if the dish does not contain ingredients, just translate the name of the dish to phrase that is easy to understand.\n'


prompt = """" \
Summarize this restaurant's menu,  \
So that the user can decide whether to eat here or not. \
You may highlight the main food categories and provide consideratins including the price and menu.
"""

response = chat.send_message([prompt, image])

print(response.text)


