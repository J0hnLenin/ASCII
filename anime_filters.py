import cv2
import numpy as np
from abc import ABC, abstractmethod

def get_filter(config):
    if config.anime_style == 1:
        return KawaiiAnimeFilter()
    if config.anime_style == 2:
        return CartoonAnimeFilter()

class BaseAnimeFilter(ABC):
    """Абстрактный базовый класс для аниме-фильтров"""

    @abstractmethod
    def apply(self, frame):
        """Применяет фильтр к кадру"""
        pass

    def process_frame(self, frame):
        """Основной метод обработки кадра"""
        return self.apply(frame)


class SimpleAnimeFilter(BaseAnimeFilter):
    """Простой аниме-фильтр с настройками"""

    def __init__(self, saturation=1.5, brightness=1.1, posterize_levels=8,
                 edge_strength=0.3, blur_radius=3):
        """
        Инициализация фильтра

        Args:
            saturation: Насыщенность (1.0 - оригинал)
            brightness: Яркость (1.0 - оригинал)
            posterize_levels: Уровни постеризации
            edge_strength: Сила выделения краев (0-1)
            blur_radius: Радиус размытия для сглаживания
        """
        self.saturation = saturation
        self.brightness = brightness
        self.posterize_levels = max(2, posterize_levels)
        self.edge_strength = edge_strength
        self.blur_radius = blur_radius

    def apply(self, frame):
        # Копируем кадр
        result = frame.copy()

        # 1. Настройка насыщенности и яркости
        if self.saturation != 1.0 or self.brightness != 1.0:
            hsv = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
            hsv = hsv.astype(np.float32)
            hsv[:, :, 1] = np.clip(hsv[:, :, 1] * self.saturation, 0, 255)
            hsv[:, :, 2] = np.clip(hsv[:, :, 2] * self.brightness, 0, 255)
            hsv = np.clip(hsv, 0, 255).astype(np.uint8)
            result = cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

        # 2. Постеризация (упрощение цветов)
        if self.posterize_levels < 256:
            div = 256 // self.posterize_levels
            posterized = (result // div) * div + div // 2
            # Смешиваем с оригиналом для плавности
            alpha = 0.7
            # Явно конвертируем в float32 для умножения
            posterized_f = posterized.astype(np.float32)
            result_f = result.astype(np.float32)
            blended = cv2.addWeighted(posterized_f, alpha, result_f, 1 - alpha, 0)
            result = np.clip(blended, 0, 255).astype(np.uint8)

        # 3. Выделение краев (аниме-контуры)
        if self.edge_strength > 0:
            gray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)

            # Разные методы выделения краев
            edges1 = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
            edges2 = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
            edges = np.sqrt(edges1 ** 2 + edges2 ** 2)
            edges = np.uint8(np.clip(edges * self.edge_strength * 10, 0, 255))

            # Инвертируем и делаем белые контуры на черном фоне
            edges = 255 - edges
            edges_color = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

            # Наложение контуров (темный режим - умножение)
            # Явно указываем тип выходного массива
            result_f = result.astype(np.float32)
            edges_f = edges_color.astype(np.float32) / 255.0

            # Умножение с явным указанием типа
            multiplied = cv2.multiply(result_f, edges_f)
            result = np.clip(multiplied, 0, 255).astype(np.uint8)

        # 4. Сглаживание (опционально)
        if self.blur_radius > 0:
            result = cv2.bilateralFilter(result,
                                         d=self.blur_radius * 2 + 1,
                                         sigmaColor=75,
                                         sigmaSpace=75)

        return result


class KawaiiAnimeFilter(SimpleAnimeFilter):
    """Кавайный аниме-фильтр с эффектами для лиц"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Инициализация детектора лиц
        try:
            self.face_cascade = cv2.CascadeClassifier(
                cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
            )
        except:
            self.face_cascade = None
            print("Предупреждение: Не удалось загрузить детектор лиц")

        # Параметры эффектов
        self.blush_color = (180, 105, 255)  # Розовый (BGR)
        self.eye_scale = 1.2  # Увеличение глаз

    def apply_face_effects(self, frame, faces):
        """Добавляет аниме-эффекты к лицам"""
        result = frame.copy()
        h, w = frame.shape[:2]

        for (x, y, width, height) in faces:
            # 1. Румянец (делаем более прозрачным)
            cheek_w = width // 4
            cheek_h = height // 8
            cheek_y = y + height // 2

            # Создаем маску для румянца
            blush_mask = np.zeros((h, w, 3), dtype=np.uint8)

            # Левый румянец
            cv2.ellipse(blush_mask,
                        (x + width // 4, cheek_y),
                        (cheek_w, cheek_h), 0, 0, 360,
                        self.blush_color, -1, cv2.LINE_AA)

            # Правый румянец
            cv2.ellipse(blush_mask,
                        (x + width * 3 // 4, cheek_y),
                        (cheek_w, cheek_h), 0, 0, 360,
                        self.blush_color, -1, cv2.LINE_AA)

            # Смешиваем с оригиналом
            alpha = 0.3  # Прозрачность румянца
            result = cv2.addWeighted(result, 1.0, blush_mask, alpha, 0)

            # 2. Блеск в глазах
            eye_y = y + height // 3
            eye_radius = max(2, width // 20)

            # Блеск в левом глазу
            cv2.circle(result,
                       (x + width // 3, eye_y),
                       eye_radius, (255, 255, 255), -1, cv2.LINE_AA)
            cv2.circle(result,
                       (x + width // 3, eye_y),
                       eye_radius, (0, 0, 0), 1, cv2.LINE_AA)  # Обводка

            # Блеск в правом глазу
            cv2.circle(result,
                       (x + width * 2 // 3, eye_y),
                       eye_radius, (255, 255, 255), -1, cv2.LINE_AA)
            cv2.circle(result,
                       (x + width * 2 // 3, eye_y),
                       eye_radius, (0, 0, 0), 1, cv2.LINE_AA)  # Обводка

        return result

    def apply(self, frame):
        # Сначала применяем базовый фильтр
        result = super().apply(frame)

        # Затем добавляем эффекты для лиц
        if self.face_cascade is not None:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self.face_cascade.detectMultiScale(
                gray, scaleFactor=1.1, minNeighbors=5,
                minSize=(30, 30)
            )

            if len(faces) > 0:
                result = self.apply_face_effects(result, faces)

        return result


class CartoonAnimeFilter(BaseAnimeFilter):
    """Фильтр в стиле мультфильма"""

    def __init__(self, num_color_levels=8, edge_threshold=10):
        self.num_color_levels = num_color_levels
        self.edge_threshold = edge_threshold

    def apply(self, frame):
        # 1. Упрощение цветов
        div = 256 // self.num_color_levels
        quantized = (frame // div) * div

        # 2. Выделение краев
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.medianBlur(gray, 7)
        edges = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C,
            cv2.THRESH_BINARY, 9, self.edge_threshold
        )

        # 3. Преобразуем края в цветное изображение
        edges_color = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)

        # 4. Объединяем с квантованным изображением (умножение)
        # Явно конвертируем в float32
        quantized_f = quantized.astype(np.float32) / 255.0
        edges_f = edges_color.astype(np.float32) / 255.0

        cartoon = cv2.multiply(quantized_f, edges_f)
        cartoon = np.clip(cartoon * 255, 0, 255).astype(np.uint8)

        return cartoon


class MaskAnimeFilter(BaseAnimeFilter):
    """Фильтр с применением внешней PNG-маски"""

    def __init__(self, mask_path, filter_strength=1.0):
        """
        Инициализация фильтра с маской

        Args:
            mask_path: Путь к PNG-маске (с альфа-каналом)
            filter_strength: Сила применения фильтра (0-1)
        """
        self.mask = self.load_mask(mask_path)
        self.filter_strength = max(0.0, min(1.0, filter_strength))
        self.base_filter = SimpleAnimeFilter()

    def load_mask(self, mask_path):
        """Загружает PNG-маску с альфа-каналом"""
        mask = cv2.imread(mask_path, cv2.IMREAD_UNCHANGED)

        if mask is None:
            raise FileNotFoundError(f"Маска не найдена: {mask_path}")

        # Если маска без альфа-канала, создаем его
        if mask.shape[2] == 3:
            # Создаем альфа-канал из яркости
            gray = cv2.cvtColor(mask, cv2.COLOR_BGR2GRAY)
            mask = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGRA)
            mask[:, :, 3] = gray  # Альфа-канал = яркость

        return mask

    def apply(self, frame):
        # Применяем базовый фильтр
        filtered = self.base_filter.apply(frame)

        # Изменяем размер маски под кадр
        h, w = frame.shape[:2]
        mask_resized = cv2.resize(self.mask, (w, h))

        # Если маска с альфа-каналом, разделяем
        if mask_resized.shape[2] == 4:
            mask_bgr = mask_resized[:, :, :3]
            mask_alpha = mask_resized[:, :, 3] / 255.0
        else:
            mask_bgr = mask_resized
            mask_alpha = np.ones((h, w), dtype=np.float32)

        # Учитываем силу фильтра
        mask_alpha = mask_alpha * self.filter_strength

        # Применяем маску через смешивание
        result = frame.copy()

        # Конвертируем в float для точных вычислений
        result_f = result.astype(np.float32)
        filtered_f = filtered.astype(np.float32)

        # Расширяем маску альфа для 3 каналов
        mask_alpha_3d = np.repeat(mask_alpha[:, :, np.newaxis], 3, axis=2)

        # Смешивание с маской: result = (1 - alpha) * original + alpha * filtered
        blended = cv2.addWeighted(result_f, 1.0 - mask_alpha_3d,
                                  filtered_f, mask_alpha_3d, 0)

        result = np.clip(blended, 0, 255).astype(np.uint8)

        return result