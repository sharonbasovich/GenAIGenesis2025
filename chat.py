import google.generativeai as genai

genai.configure(api_key="AIzaSyCCTK90t4X7SVmmFHHbwRtI8u5sk_b7DZE")

model = genai.GenerativeModel('gemini-2.0-flash')
chat = model.start_chat(history=[])

print("Welcome to the Gemini Chatbot!")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    try:
        response = chat.send_message(user_input)
        print("Bot:", response.text)
    except Exception as e:
        print(f"An error occurred: {e}")

print("Chat ended.")