import sys
import cv2

def process_frame(frame):
    print(frame_to_ascii(frame))
    return frame

def frame_to_ascii(frame):
    width=100

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Изменяем размер (сохраняем пропорции)
    height, original_width = gray.shape
    aspect_ratio = height / original_width
    new_height = int(width * aspect_ratio * 0.55)  # 0.55 учитывает соотношение сторон символов
    
    # Ресайзим
    resized = cv2.resize(gray, (width, new_height), interpolation=cv2.INTER_AREA)
    
    ascii_str = ""
    for row in resized:
        for pixel in row:
            ascii_str += get_ascii(pixel)
        ascii_str += "\n"
    return ascii_str

def get_ascii(pixel):
    pixel = int(pixel)
    chars = list("@%#*+=-:.. ")
    index = (pixel * (len(chars) - 1)) // 255
    return chars[index]
