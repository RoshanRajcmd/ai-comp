import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import os, time
from voice_functions import listen_and_transcribe, speak_text 
# from ollama_interface import get_ollama_response
from constants import WINDOW_SIZE, IMAGE_SIZE, ASSETS_DIR, INIT_EXPRESSION

class AICompanionApp:
    def __init__(self, master):
        self.master = master
        master.title("AI Companion")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        # Set initial window size
        master.geometry(WINDOW_SIZE)
        master.grid_columnconfigure(0, weight=2)
        master.grid_columnconfigure(1, weight=1)
        self.master.grid_rowconfigure(0, weight=5) # Main avatar space
        self.master.grid_rowconfigure(1, weight=1) # Button space
        
        # Load all avatar images at startup
        self.avatars = self._load_avatars()
        
        # --- UI Setup ---
        
        # 1. Avatar Display
        self.current_avatar_image = self.avatars.get(INIT_EXPRESSION)
        self.avatar_label = tk.Label(master, image=self.current_avatar_image)
        # place the button in row and column of the grid
        self.avatar_label.grid(row=0, column=0, sticky="nsew") 
        
        # 2. Control Button
        self.listen_button = tk.Button(
            master, 
            text="Hold to Speak", 
            command=self.start_conversation_sequence,
            font=('Arial', 16, 'bold'),
            bg='#4CAF50', # Green color
            fg='white',
            padx=20,
            pady=10
        )
        # place the button in row and column of the grid
        self.listen_button.grid(row=1, column=0, pady=20)
        
        # 3. Console/Log Section
        tk.Label(master, text="Console Log:").grid(row=0, column=1)
        self.console = scrolledtext.ScrolledText(master, wrap=tk.WORD, width=50, height=10, font=('Courier', 10))
        # place the console to grid and make use of the entire column
        self.console.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)
        self.log_message("System: Application started. Ready for conversation.")
        self.copy_button = tk.Button(
            master, 
            text="Copy log", 
            font=('Arial', 16, 'bold'),
            bg='#4CAF50', # Green color
            fg='white',
            padx=20,
            pady=10
        )
        # place the button in row and column of the grid
        self.copy_button.grid(row=2, column=1, pady=20)

    # Loads and converts all avatar images from the assets directory and return it in a dictionary
    def _load_avatars(self):
        avatars = {}
        expression_list = ["neutral", "happy", "excited", "angry", "sad", "unpleasant", "proud"]
        
        for expr in expression_list:
            try:
                file_path = os.path.join(ASSETS_DIR, f"{expr}.png")
                img_pil = Image.open(file_path).resize(IMAGE_SIZE)
                # Tkinter requires a persistent PhotoImage object
                avatars[expr.lower()] = ImageTk.PhotoImage(img_pil) 
            except FileNotFoundError:
                self.log_message(f"ERROR: Image file not found for {expr}.png")
                # Use a placeholder if necessary
        return avatars

    # Prints given message to the console text area.
    def log_message(self, message):
        self.console.insert(tk.END, f"\n[{self._get_time()}] {message}")
        # Auto-scroll to the bottom
        self.console.see(tk.END)

    def _get_time(self):
        import datetime
        return datetime.datetime.now().strftime("%H:%M:%S")

    def update_avatar(self, expression_tag):
        """Switches the displayed avatar image."""
        tag = expression_tag.lower()
        if tag in self.avatars:
            self.avatar_label.configure(image=self.avatars[tag])
            self.current_avatar_image = self.avatars[tag] # Important: Keep reference
            self.master.update() # Force UI update immediately
        else:
            self.log_message(f"Warning: Unknown expression tag '{expression_tag}', defaulting to neutral.")
            self.update_avatar("neutral")


    def start_conversation_sequence(self):
        """
        The main handler for the conversation flow.
        (This is where you integrate your Ollama/Whisper/Piper logic)
        """
        self.log_message("User: Button pressed. Listening...")
        
        try:
            # 1. Listen (STT) - Placeholder for listen_and_transcribe()
            # user_text = listen_and_transcribe() 
            user_text = "Hello, what's the weather like today?" # Placeholder response
            
            if not user_text:
                self.log_message("User: No speech detected.")
                return

            self.log_message(f"User Transcribed: {user_text}")

            # 2. Get LLM Response - Placeholder for Ollama call
            # llm_response = get_ollama_response(user_text) 
            llm_response = "[PROUD] I'm happy to report perfect weather for a brilliant mind like yours." # Simulated LLM response
            
            # 3. Process LLM Output (Split Tag and Dialogue)
            try:
                # Find tag, assumes format [TAG] Dialogue
                tag_end = llm_response.find(']')
                expression_tag = llm_response[1:tag_end].strip()
                dialogue_text = llm_response[tag_end+1:].strip()
            except Exception:
                expression_tag = "neutral"
                dialogue_text = "I seem to have a momentary glitch."

            # 4. Update Avatar (Show the emotion)
            self.update_avatar(expression_tag)
            self.log_message(f"Companion: Expression set to **{expression_tag}**")
            time.sleep(3)

            # 5. Speak (TTS) - Placeholder for speak_text()
            # speak_text(dialogue_text) 
            self.log_message(f"Companion Responce: {dialogue_text}")
            
        except Exception as e:
            self.log_message(f"CRITICAL ERROR: {e}")
            self.update_avatar("unpleasant") # Show a shocked face on error

        # 6. Reset Avatar to neutral after conversation sequence
        self.update_avatar(INIT_EXPRESSION)

    # Handles graceful shutdown, cleaning up any resources (threads, audio streams).
    def on_closing(self):
        self.log_message("System: Starting graceful shutdown...")
        
        # --- CRITICAL CLEANUP STEPS ---
        
        # 1. Stop any background threads or processes used by voice functions.
        #    If your 'listen' or 'speak' functions are running in background threads, 
        #    you must stop them here. (Placeholder logic)
        # if self.listening_thread and self.listening_thread.is_alive():
        #     # Example: Set a flag to stop the thread gracefully
        #     self.listening_flag = False 
        
        # 2. Specifically clean up audio resources (for libraries like sounddevice/Piper)
        #    Although sounddevice often cleans up well, explicitly stopping any active 
        #    streams or devices is the safest way to prevent semaphore leaks.
        try:
            import sounddevice as sd
            sd.stop() # Stops all active sounddevice streams
        except ImportError:
            pass # Ignore if sounddevice isn't imported here
        
        self.log_message("System: Cleanup complete. Destroying window.")        
        # Destroy the Tkinter window
        self.master.destroy()