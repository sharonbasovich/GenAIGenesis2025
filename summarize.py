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


prompt = f"""
You are a helpful restaurant reviewer. Summarize this restaurant's menu with the goal of helping a user decide whether to eat here or not. 
Generate your review in {language} The user uses {language}.

Please provide:

1.  A very brief overview of the types of dishes offered.
2.  Key considerations regarding the menu, such as variety, specific culinary styles, and any unique or signature items.
3.  An assessment of the general price range (e.g., budget-friendly, mid-range, expensive).
4.  Information about any dietary accommodations (e.g., vegetarian, vegan, gluten-free) considering the menu.
5.  A brief description of the type of dining experience the menu suggests (e.g., casual, fine dining, family-friendly).
6.  A short conclusion stating what type of person or group would likely enjoy dining at this establishment.
"""
response = chat.send_message([prompt, image])

print(response.text)


