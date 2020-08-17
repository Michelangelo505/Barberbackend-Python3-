from PIL import Image

def CompressImage(path_to, width, height):
    """
    Данный метод сжимает картинку без потери качества
    с указанием максимальной возможной выстоты и ширины,
    сохраняет при этом соотношение сторон.

    :param path_to: Путь к загруженной картинке
    :param width: Требуемая максимальная ширина картинки
    :param height: Требуемая максимальная высота картинки
    :return: False - Если была ошибка в обработке, иначе True

    Author: Поздняков М.А.
    email: garrys505@gmail.com
    """
    max_size = (width, height)
    try:
        with Image.open(path_to) as original_img:
            original_img.thumbnail(max_size, Image.ANTIALIAS)

            original_img.save(path_to)

            return True

    except:
        return False
