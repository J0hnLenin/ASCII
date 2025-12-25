import sys
import cv2
import numpy as np
import ascii_filters
import anime_filters
 
def process_frame(config, frame):
    if config.anime_on:
        anime_filter = anime_filters.KawaiiAnimeFilter()
        result_frame = anime_filter.apply(frame)
        result_frame = cv2.medianBlur(result_frame, 11)
        result_frame = cv2.detailEnhance(result_frame, sigma_s=10, sigma_r=0.15)
        frame = result_frame
    
    if config.ascii_on:
        new_height, new_width = ascii_filters.get_new_shape(config, frame.shape)
        result_frame = ascii_filters.resize(frame, new_height, new_width)
        result_frame = ascii_filters.enhance(result_frame)
        result_frame = ascii_filters.create_pixel_ascii_image(config, result_frame)
        frame = result_frame

    return frame
