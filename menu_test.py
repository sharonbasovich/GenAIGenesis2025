import os
import sys
import argparse
from PIL import Image
import pytesseract
import google.generativeai as genai
import re
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from PIL import Image, ImageTk

class MenuAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Menu Analyzer")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Configure Gemini API
        self.configure_gemini()


        # Create UI elements
        self.create_widgets()
    
    def configure_gemini(self):
        """Configure the Gemini API with the API key"""
        try:
            GEMINI_API_KEY = "AIzaSyDaNd1nu-hc4tibF9wEd5MyE6yUByk5zt8"
            if not GEMINI_API_KEY:
                messagebox.showerror("API Key Error", 
                                     "Gemini API key not found. Please set the GEMINI_API_KEY environment variable.")
            genai.configure(api_key=GEMINI_API_KEY)
        except Exception as e:
            messagebox.showerror("API Configuration Error", str(e))
    
    def create_widgets(self):
        """Create all UI widgets"""
        # Top frame for image selection
        top_frame = tk.Frame(self.root, bg="#f0f0f0")
        top_frame.pack(fill=tk.X, padx=20, pady=20)
        
        # Button to select image
        self.select_btn = tk.Button(
            top_frame, 
            text="Select Menu Image", 
            command=self.select_image,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 12),
            padx=10,
            pady=5
        )
        self.select_btn.pack(side=tk.LEFT, padx=5)
        
        # Label to show selected file
        self.file_label = tk.Label(
            top_frame, 
            text="No file selected", 
            bg="#f0f0f0",
            font=("Arial", 10)
        )
        self.file_label.pack(side=tk.LEFT, padx=10)
        
        # Middle frame for image preview
        self.preview_frame = tk.Frame(self.root, bg="#f0f0f0")
        self.preview_frame.pack(fill=tk.X, padx=20, pady=10)
        
        self.image_label = tk.Label(self.preview_frame, bg="#f0f0f0")
        self.image_label.pack()
        
        # Analyze button
        self.analyze_btn = tk.Button(
            self.root,
            text="Analyze Menu",
            command=self.analyze_menu,
            bg="#2196F3",
            fg="white",
            font=("Arial", 12),
            padx=10,
            pady=5,
            state=tk.DISABLED
        )
        self.analyze_btn.pack(pady=10)
        
        # Results area
        result_frame = tk.Frame(self.root, bg="#f0f0f0")
        result_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        result_label = tk.Label(
            result_frame, 
            text="Analysis Results:", 
            bg="#f0f0f0",
            font=("Arial", 12, "bold")
        )
        result_label.pack(anchor=tk.W)
        
        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            wrap=tk.WORD,
            width=80,
            height=15,
            font=("Arial", 11)
        )
        self.result_text.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(
            self.root, 
            textvariable=self.status_var, 
            bd=1, 
            relief=tk.SUNKEN, 
            anchor=tk.W
        )
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Store the image path
        self.image_path = None
    
    def select_image(self):
        """Open file dialog to select an image"""
        file_types = [
            ("menus\menu2.jpg", "*.jpg *.jpeg *.png *.bmp *.tiff")
        ]
        
        file_path = filedialog.askopenfilename(
            title="Select Menu Image",
            filetypes=file_types
        )
        
        if file_path:
            self.image_path = file_path
            self.file_label.config(text=os.path.basename(file_path))
            self.analyze_btn.config(state=tk.NORMAL)
            self.display_image_preview(file_path)
            self.status_var.set(f"Selected: {os.path.basename(file_path)}")
    
    def display_image_preview(self, image_path):
        """Display a preview of the selected image"""
        try:
            img = Image.open(image_path)
            
            # Resize image to fit in the UI
            max_width = 400
            max_height = 200
            
            width, height = img.size
            ratio = min(max_width/width, max_height/height)
            new_size = (int(width * ratio), int(height * ratio))
            
            img = img.resize(new_size, Image.LANCZOS)
            
            # Convert to PhotoImage for tkinter
            photo = ImageTk.PhotoImage(img)
            
            # Update image label
            self.image_label.config(image=photo)
            self.image_label.image = photo  # Keep a reference
        except Exception as e:
            messagebox.showerror("Image Preview Error", str(e))
    
    def extract_text_from_image(self, image_path):
        """Extract text from an image using OCR"""
        try:
            self.status_var.set("Extracting text from image...")
            self.root.update()
            
            image = Image.open(image_path)
            text = pytesseract.image_to_string(image)
            return text
        except Exception as e:
            messagebox.showerror("OCR Error", f"Error extracting text from image: {e}")
            return None
    
    def analyze_menu(self):
        """Process the menu image and display results"""
        if not self.image_path:
            messagebox.showerror("Error", "No image selected")
            return
        
        # Clear previous results
        self.result_text.delete(1.0, tk.END)
        
        # Extract text from image
        menu_text = self.extract_text_from_image(self.image_path)
        if not menu_text:
            self.status_var.set("Failed to extract text from image")
            return
        
        # Analyze with Gemini
        self.status_var.set("Analyzing menu with Gemini AI...")
        self.root.update()
        
        try:
            # Initialize Gemini model
            model = genai.GenerativeModel('gemini-pro')
            
            # Create prompt for Gemini
            prompt = f"""
            Analyze this menu text and list all dishes with their ingredients.
            Format your response as a structured list with dish names and their ingredients:

            {menu_text}
            """
            
            # Generate response
            response = model.generate_content(prompt)
            
            # Display results
            self.display_results(response.text)
            self.status_var.set("Analysis complete")
        except Exception as e:
            messagebox.showerror("Analysis Error", f"Error analyzing menu: {e}")
            self.status_var.set("Analysis failed")
    
    def display_results(self, ai_response):
        """Display the AI analysis results in the text area"""
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, ai_response)

def main():
    # Check for Gemini API key
    if not os.environ.get("GEMINI_API_KEY"):
        print("Warning: GEMINI_API_KEY environment variable not set.")
        print("Please set it before running the application.")
        print("Example: export GEMINI_API_KEY='your_api_key_here'")
    
    # Create and run the app
    root = tk.Tk()
    app = MenuAnalyzerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

