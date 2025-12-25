import sys
import cv2
import numpy as np
import filter_ascii
import filter_anime
 
def process_frame(config, frame):
    if config.anime_on:
        result_frame = filter_anime.apply(frame)
        result_frame = cv2.medianBlur(result_frame, 11)
        result_frame = cv2.detailEnhance(result_frame, sigma_s=10, sigma_r=0.15)
        frame = result_frame
    
    if config.ascii_on:
        new_height, new_width = filter_ascii.get_new_shape(config, frame.shape)
        result_frame = filter_ascii.resize(frame, new_height, new_width)
        result_frame = filter_ascii.enhance(result_frame)
        result_frame = filter_ascii.create_pixel_ascii_image(config, result_frame)
        frame = result_frame

    return result_frame
