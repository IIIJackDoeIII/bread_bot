from PIL import Image, ImageFilter, ExifTags
def resize_with_background(image_path, size=(512, 512), color=(192, 192, 192), blur_radius=50):
    """
    Обрабатывает изображение: сохраняет ориентацию, добавляет размытие в качестве фона.
    """
    with Image.open(image_path) as img:
        # Поправка на ориентацию EXIF (если есть)
        try:
            for orientation in ExifTags.TAGS.keys():
                if ExifTags.TAGS[orientation] == 'Orientation':
                    break
            exif = img._getexif()
            if exif is not None:
                orientation_value = exif.get(orientation, None)
                if orientation_value == 3:
                    img = img.rotate(180, expand=True)
                elif orientation_value == 6:
                    img = img.rotate(270, expand=True)
                elif orientation_value == 8:
                    img = img.rotate(90, expand=True)
        except Exception as e:
            print(f"EXIF Orientation correction failed: {e}")

        # Определяем пропорции изображения и целевого размера
        img_ratio = img.width / img.height
        target_ratio = size[0] / size[1]

        if img_ratio > target_ratio:
            # Ширина изображения больше, чем у целевого размера – рамки сверху и снизу
            new_width = size[0]
            new_height = int(size[0] / img_ratio)
        else:
            # Высота изображения больше, чем у целевого размера – рамки слева и справа
            new_height = size[1]
            new_width = int(size[1] * img_ratio)

        # Масштабируем изображение
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        # Создаём размытую версию исходного изображения
        background = img.filter(ImageFilter.GaussianBlur(blur_radius))  # Больше размытия
        background = background.resize(size, Image.Resampling.LANCZOS)

        # Создаём новый холст и вставляем размытую картинку
        new_image = Image.new("RGB", size)
        new_image.paste(background, (0, 0))

        # Вставляем основное изображение в центр нового холста
        offset_x = (size[0] - new_width) // 2
        offset_y = (size[1] - new_height) // 2
        new_image.paste(img_resized, (offset_x, offset_y))

        # Сохраняем результат
        processed_path = image_path.replace(".", "_processed.")
        new_image.save(processed_path)
        return processed_path
