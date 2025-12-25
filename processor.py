import sys
import cv2
import numpy as np

def process_frame(config, frame):
    if config.ascii_on:
        new_height, new_width = get_new_shape(config, frame.shape)
        resized = resize(frame, new_height, new_width)
        enhanced = enhance(resized)
        frame = create_pixel_ascii_image(config, enhanced)
    return frame

def get_new_shape(config, shape):
    original_height, original_width = shape[:2]
    aspect_ratio = original_height / original_width

    new_width = original_width // config.ascii_size 

    new_height = int(new_width * aspect_ratio)
    return new_height, new_width

def resize(frame, new_height, new_width):
    return cv2.resize(frame, (new_width, new_height), interpolation=cv2.INTER_AREA)

def create_pixel_ascii_image(config, frame):
    height, width = frame.shape[:2]
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    
    scale_factor = config.ascii_size
    result_h = height * scale_factor
    result_w = width * scale_factor
    result = np.zeros((result_h, result_w, 3), dtype=np.uint8)
    
    for y in range(height):
        for x in range(width):
            pixel_brightness = gray[y, x]
            char = get_ascii(pixel_brightness)
            
            y_pos = y * scale_factor
            x_pos = x * scale_factor
            
            cv2.putText(result, char, (x_pos, y_pos + scale_factor), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.3 + scale_factor/50, tuple(map(int, frame[y, x])), 1)
    
    return result

def get_ascii(pixel):
    pixel = int(pixel)
    chars = list("@80OXWMV%#pxo*+=-:.. ")
    index = (pixel * (len(chars) - 1)) // 255
    return chars[index]

def enhance(image):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    
    v_mean = np.mean(v)
    v_std = np.std(v)
    
    v_min = max(0, int(v_mean - 2*v_std))
    v_max = min(255, int(v_mean + 2.5*v_std))
    
    if v_max > v_min:
        v = np.clip(v, v_min, v_max)
        v = ((v - v_min) * (255.0 / (v_max - v_min))).astype(np.uint8)
    
    enhanced_hsv = cv2.merge([h, s, v])
    
    return cv2.cvtColor(enhanced_hsv, cv2.COLOR_HSV2RGB)