import cv2
import pyvirtualcam
from processor import process_frame

def capture_camera():
    use_virtual_camera = True
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Ошибка: не удалось открыть камеру")
    else:
        if not use_virtual_camera:
            while True:
                ret, frame = cap.read()

                if not ret:
                    print("Не удалось получить кадр (конец потока?)")
                    break

                result_frame = process_frame(frame)
                cv2.imshow('Video Capture', result_frame)

                # Выход по нажатию 'esc'
                if cv2.waitKey(1) & 0xFF == 27:
                    break

        if use_virtual_camera:
            with pyvirtualcam.Camera(width=1000, height=750, fps=20) as cam:
                while True:
                    ret, frame = cap.read()

                    if not ret:
                        print("Не удалось получить кадр (конец потока?)")
                        break
                    
                    result_frame = process_frame(frame)

                    cam.send(result_frame)
                    cam.sleep_until_next_frame()

        cap.release()
        cv2.destroyAllWindows()