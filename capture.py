import cv2
import pyvirtualcam
from processor import process_frame

KEY_ESC = 27

def capture_camera(config):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Ошибка: не удалось открыть камеру")
        return
    
    if not config.use_virtual_camera:
        while True:
            ret, frame = cap.read()

            if not ret:
                print("Не удалось получить кадр (конец потока?)")
                break
            
            result_frame = process_frame(config, frame)
            cv2.imshow('Video Capture', result_frame)

            need_exit = key_catch(config)
            if need_exit:
                break

    else:
        ret, frame = cap.read()

        if not ret:
            print("Не удалось получить кадр (конец потока?)")
            return

        with pyvirtualcam.Camera(width=frame.shape[1], height=frame.shape[0], fps=20) as cam:
            while True:
                ret, frame = cap.read()

                if not ret:
                    print("Не удалось получить кадр (конец потока?)")
                    break
                
                result_frame = process_frame(config, frame)

                cam.send(result_frame)
                cam.sleep_until_next_frame()

                need_exit = key_catch(config)
                if need_exit:
                    break

    cap.release()
    cv2.destroyAllWindows()

def key_catch(config):
    key = cv2.waitKey(1) & 0xFF

    if key == KEY_ESC:
        return True
    elif key == ord('1'):
        config.anime_on = not config.anime_on
    elif key == ord('2'):
        config.ascii_on = not config.ascii_on
    elif key == ord('3'):
        config.median_blur_on = not config.median_blur_on
    
    if config.anime_on:
        if key == ord('q') and config.anime_style < 2:
            config.anime_style += 1
        elif key == ord('a') and config.anime_style > 1:
            config.anime_style -= 1
        
    if config.ascii_on:
        if key == ord('w'):
            config.ascii_size += 1
        elif key == ord('s') and config.ascii_size > 4:
            config.ascii_size -= 1

    if config.median_blur_on:
        if key == ord('e') and config.median_blur_size < 15:
            config.median_blur_size += 2
        elif key == ord('d') and config.median_blur_size > 3:
            config.median_blur_size -= 2

    return False
