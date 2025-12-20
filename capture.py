import cv2
from processor import process_frame

def capture_camera():
    # 1. Создаем объект VideoCapture для захвата с веб-камеры (индекс 0)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Ошибка: не удалось открыть камеру")
    else:
        while True:
            # 2. Читаем кадр
            ret, frame = cap.read() # ret - True/False, frame - сам кадр

            if not ret:
                print("Не удалось получить кадр (конец потока?)")
                break

            # 3. Отображаем кадр
            cv2.imshow('Video Capture', process_frame(frame))

            # 4. Выход по нажатию 'esc'
            if cv2.waitKey(1) & 0xFF == 27:
                break

        # 5. Освобождаем ресурсы
        cap.release()
        cv2.destroyAllWindows()