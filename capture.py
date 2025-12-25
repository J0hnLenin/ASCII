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

            key = cv2.waitKey(1) & 0xFF
            print(key)
            if key == KEY_ESC:
                break
            elif key == ord('1'):
                config.ascii_on = not config.ascii_on
            elif key == ord('2'):
                config.anime_on = not config.anime_on
            elif key == ord('+'):
                config.ascii_size += 1
            elif key == ord('-')  and config.ascii_size > 4:
                config.ascii_size -= 1


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

    cap.release()
    cv2.destroyAllWindows()