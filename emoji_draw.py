from PIL import Image, ImageDraw, ImageFont
import numpy as np
import random
import emoji
import cv2

class RisingEmoji:
    def __init__(self, emoji, speed):
        self.emoji = emoji
        self.x = random.randint(20, 600)
        self.y = 480
        self.speed = speed * random.uniform(0.8, 1.2) 
        self.size = random.uniform(0.8, 1.5)
        self.color = (random.randint(100, 255), 
                     random.randint(100, 255), 
                     random.randint(100, 255))

    def draw(self, frame):
        """Добавляет эмодзи используя PIL для лучшей поддержки Unicode"""
        
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)
        
        font_size = 50 * self.size
        font_path = "seguiemj-1.45-3d.ttf"
        try:
            font = ImageFont.truetype(font_path, font_size, encoding="unic")
        except IOError:
            print(f"Font file not found: {font_path}. Using default font.")
            font = ImageFont.load_default()

        draw.text((self.x, self.y), self.emoji, font=font, fill=self.color)

        cv2_image_result = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        return cv2_image_result

def draw_emojis(frame, emojis):
    to_delete = []

    for i, emoji in enumerate(emojis):
        emoji.y -= emoji.speed
        if emoji.y < -emoji.size:
            to_delete.append(i)
            continue

        frame = emoji.draw(frame)
    
    for i in to_delete[::-1]:
        emojis.pop(i)
    
    return frame

def get_emojis():
    return {
        "sad": "😔",
        "disgust": "🤢",
        "angry": "😡",
        "neutral": "😐",
        "fear": "😨",
        "surprise": "😲",
        "happy": "😀",
    }