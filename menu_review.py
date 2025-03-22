import google.generativeai as genai
import PIL.Image  

class MenuReviewer:
    def __init__(self, api_key, task, language):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.0-flash')
        self.chat = self.model.start_chat(history=[])
        self.task = task
        self.languages = language
    
    def load_image(self, image_path):
        """Loads an image from the given path."""
        return PIL.Image.open(image_path)
    
    def generate_review(self, image_path):
        """Generates a restaurant menu review based on the provided image and selected language."""

        image = self.load_image(image_path)
        
        prompt = return_prompt(self.task, self.languages)
        response = self.chat.send_message([prompt, image])
        return response.text


def return_prompt(task, language):
    if task == 'summarize':
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

    if task == 'simple_menu':
        prompt = f"""
        '1.translate the dishes in the picture to ' + {language} .
        2.if the dish does not contain ingredients, just translate the name of the dish to phrase that is easy to understand.'
        3.if the ingredients are too complex, use simplier terms.'
        """
    return prompt
