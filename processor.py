import sys
import cv2
import numpy as np
import ascii_filters
import anime_filters
 
def process_frame(config, frame):
    if config.anime_on:
        anime_filter = anime_filters.get_filter(config)
        frame = anime_filter.apply(frame)

    if config.ascii_on:
        new_height, new_width = ascii_filters.get_new_shape(config, frame.shape)
        result_frame = ascii_filters.resize(frame, new_height, new_width)
        result_frame = ascii_filters.enhance(result_frame)
        result_frame = ascii_filters.create_pixel_ascii_image(config, result_frame)
        frame = result_frame
        
    if config.median_blur_on:
        frame = cv2.medianBlur(frame, config.median_blur_size)

    return frame