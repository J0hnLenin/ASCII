import cv2
import pyvirtualcam
from processor import process_frame
from emotion_classifier import predict_emotion
from emoji_draw import RisingEmoji, draw_emojis, get_emojis

KEY_ESC = 27

def capture_camera(config):
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Ошибка: не удалось открыть камеру")
        return
    
    print_navigation_info()

    frame_number = 0
    emojis = get_emojis()
    emojis_on_frame = []

    if not config.use_virtual_camera:
        while True:
            frame_number += 1
            ret, frame = cap.read()

            if not ret:
                print("Не удалось получить кадр (конец потока?)")
                break
            
            if config.emoji_on and frame_number % config.prediction_num == 0:
                emotion = predict_emotion(frame, config.emoji_threshold)
                if emotion is not None:
                    emojis_on_frame.append(RisingEmoji(emojis[emotion], config.emoji_speed))

            result_frame = process_frame(config, frame)

            if config.emoji_on:
                result_frame = draw_emojis(result_frame, emojis_on_frame)
            else:
                emojis_on_frame = []

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
                frame_number += 1
                ret, frame = cap.read()

                if not ret:
                    print("Не удалось получить кадр (конец потока?)")
                    break
                
                if config.emoji_on and frame_number % config.prediction_num == 0:
                    emotion = predict_emotion(frame, config.emoji_threshold)
                    if emotion is not None:
                        emojis_on_frame.append(RisingEmoji(emojis[emotion], config.emoji_speed))

                result_frame = process_frame(config, frame)

                if config.emoji_on:
                    result_frame = draw_emojis(result_frame, emojis_on_frame)
                else:
                    emojis_on_frame = []

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
    elif key == ord('4'):
        config.emoji_on = not config.emoji_on
    
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
    
    if config.emoji_on:
        if key == ord('r') and config.emoji_speed < 5:
            config.emoji_speed += 1
        elif key == ord('f') and config.emoji_speed > 1:
            config.emoji_speed -= 1

    return False

def print_navigation_info():
    print()
    print("Запущено приложение фильтрации видеопотока с веб-камеры")
    print()
    print("┌──────────────────────────────────────────────────┐")
    print("│ 'ESC' - выход                                    │")
    print("├─────────┬────────┬───────┬───────────┬───────────┤")
    print("│ Фильтр  │ Аниме  │ ASCII │ Медианный │ Смайлики  │")
    print("├─────────┼────────┼───────┼───────────┼───────────┤")
    print("│   ВКЛ   │  '1'   │  '2'  │    '3'    │    '4'    │")
    print("├─────────┼────────┼───────┼───────────┼───────────┤")
    print("│    ↑    │  'Q'   │  'W'  │    'E'    │    'R'    │")
    print("├─────────┼────────┼───────┼───────────┼───────────┤")
    print("│    ↓    │  'A'   │  'S'  │    'D'    │    'F'    │")
    print("└─────────┴────────┴───────┴───────────┴───────────┘")