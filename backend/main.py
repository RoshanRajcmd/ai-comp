import tkinter as tk
from constants import ASSETS_DIR
import os
from AICompanionApp import AICompanionApp

if __name__ == "__main__":
    # Ensure the assets directory exists for the image loading to work
    if not os.path.isdir(ASSETS_DIR):
        print(f"Error: The '{ASSETS_DIR}' directory not found in application runing directory")
    else:
        root = tk.Tk()
        app = AICompanionApp(root)
        root.mainloop()