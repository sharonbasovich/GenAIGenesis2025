import google.generativeai as genai
import PIL.Image  # For image handling

genai.configure(api_key="AIzaSyCCTK90t4X7SVmmFHHbwRtI8u5sk_b7DZE")  # Replace with your actual API key

model = genai.GenerativeModel('models/gemini-2.0-flash')
chat = model.start_chat(history=[])

print("Welcome to the Gemini Vision Chatbot!")

def load_image(image_path):

    img = PIL.Image.open(image_path)
    return img

image_path = './menus/menu2.jpg'
img = load_image(image_path)

while True:
    user_input = input("You : ")

    try:
        response = chat.send_message([user_input, img])
        print("Bot:", response.text)

    except Exception as e:
        print(f"An error occurred: {e}")

