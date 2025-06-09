import customtkinter as ctk
import tkinter as tk
import google.generativeai as genai
import os

class Chatbot:
    def __init__(self, root_window):
        self.root_window = root_window
        # Configure Gemini API
        # IMPORTANT: Replace "YOUR_GEMINI_API_KEY" with your actual Gemini API key.
        # You can get one from Google AI Studio: https://aistudio.google.com/
        # It's recommended to load this from an environment variable for security.
        # Example: os.environ.get("GEMINI_API_KEY")
        genai.configure(api_key="AIzaSyDaU3v_-sM5dQqoiWZzr7gTRIDpQaUGz4E") # Đã cập nhật API Key của Gemini
        self.model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
        self.chat = self.model.start_chat(history=[])
        self.chat.send_message("Bạn là một trợ lý chatbot thân thiện và hữu ích. Hãy luôn trả lời bằng tiếng Việt.")

    def create_chatbot_window(self):
        self.window = ctk.CTkToplevel(self.root_window)
        self.window.title("🤖 Chatbot AI")
        self.window.geometry("600x700")
        self.window.transient(self.root_window) # Make it transient to the main app window
        self.window.grab_set()
        self.window.focus_force()
        self.create_widgets()
        self.display_message("Chatbot", "Chào bạn, tôi có thể giúp gì được cho bạn?", "🤖")

    def create_widgets(self):
        # Chat history display
        self.chat_history_frame = ctk.CTkScrollableFrame(self.window, corner_radius=0)
        self.chat_history_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.chat_history_label = ctk.CTkLabel(self.chat_history_frame, text="", wraplength=550, justify=tk.LEFT)
        self.chat_history_label.pack(fill=tk.X, anchor=tk.NW, pady=5)

        # Input frame
        input_frame = ctk.CTkFrame(self.window)
        input_frame.pack(fill=tk.X, padx=10, pady=10)

        self.message_entry = ctk.CTkEntry(input_frame, placeholder_text="Nhập tin nhắn của bạn...", width=450)
        self.message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.message_entry.bind("<Return>", self.send_message_event) # Bind Enter key

        self.send_button = ctk.CTkButton(input_frame, text="Gửi 🚀", command=self.send_message)
        self.send_button.pack(side=tk.RIGHT)

    def display_message(self, sender, message, emoji):
        current_text = self.chat_history_label.cget("text")
        new_text = f"{current_text}\n{emoji} {sender}: {message}"
        self.chat_history_label.configure(text=new_text)
        self.chat_history_frame._parent_canvas.yview_moveto(1.0) # Scroll to bottom

    def send_message_event(self, event=None):
        self.send_message()

    def send_message(self):
        user_message = self.message_entry.get().strip()
        if not user_message:
            return

        self.display_message("Bạn", user_message, "🙋‍♂️")
        self.message_entry.delete(0, tk.END)

        try:
            response = self.chat.send_message(user_message)
            bot_response = response.text
            self.display_message("Chatbot", bot_response, "🤖")
        except Exception as e:
            self.display_message("Chatbot", f"Xin lỗi, có lỗi xảy ra: {e}", "🚨") 