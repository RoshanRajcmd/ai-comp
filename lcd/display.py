import os
import time
import threading
from pathlib import Path
from PIL import Image
from constants import LCD_ENABLED, EXPRESSIONS

try:
    from luma.oled.device import ssd1306
    from luma.core.interface.serial import i2c
    from luma.core.render import canvas
    LUMA_AVAILABLE = True
except ImportError:
    LUMA_AVAILABLE = False

DISPLAY_WIDTH = 128
DISPLAY_HEIGHT = 64
FACES_DIR = "assets/faces/"

class LCDDisplay:
    def __init__(self):
        self.device = None
        self.current_expression = "neutral"
        self._running = False
        self._thread = None

        if LCD_ENABLED and LUMA_AVAILABLE:
            try:
                serial = i2c(port=1, address=0x3C)
                self.device = ssd1306.SSD1306(serial, width=DISPLAY_WIDTH, height=DISPLAY_HEIGHT)
                self.device.contrast(200)
            except Exception as e:
                print(f"LCD init failed: {e}")
                self.device = None

    def set_expression(self, emotion: str):
        if emotion not in EXPRESSIONS:
            emotion = "neutral"
        self.current_expression = emotion
        self._show_frame(emotion)

    def _show_frame(self, emotion: str):
        if not self.device:
            return

        image_name = EXPRESSIONS.get(emotion, "neutral.png")
        image_path = os.path.join(FACES_DIR, image_name)

        if not os.path.exist(image_path):
            with canvas(self.device) as draw:
                draw.text((10, 25), emotion.upper(), fill="white")
            return

        img = Image.open(image_path)
        img = img.convert("1") # Convert to 1-bit monochrome
        img = img.resize((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        self.device.display(img)

    def start_animation(self, emotion: str, frame_dir: str=None):
        # Animate PBM/PNG frame sequence for an expression
        self._running = True
        self._thread = threading.Thread(target=self._animate_loop, args=(emotion, frame_dir), daemon=True)
        self._thread.start()

    def stop_animation(self):
        self._running = False
        if self._thread:
            self._thread.join(timeout=1)

    def _animation_loop(self, emotion: str, frame_dir: str = None):
        if not self.device:
            return

        if not frame_dir:
            frame_dir = os.path.join(FACES_DIR, emotion)

        if not os.path.isdir(frame_dir):
            self._show_frame(emotion)
            return

        frames = sorted(Path(frame_dir).glob("*.png"))
        if not frames:
            frames = sorted(Path(frame_dir).glob("*.pbm"))
        if not frames:
            self._show_frame(emotion)
            return

        while self._running:
            for frame_path in frames:
                if not self._running:
                    break
                img = Image.open(frame_path)
                img = img.convert("1")
                img = img.resize((DISPLAY_WIDTH, DISPLAY_HEIGHT))
                self.device.display(img)
                time.sleep(0.05)

    def clear(self):
        if self.device:
            self.device.clear()

# Singleton
_lcd = None

def get_lcd() -> LCDDisplay:
    global _lcd
    if _lcd is None:
        _lcd = LCDDisplay()
    return _lcd