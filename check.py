from PIL import Image

def run():
    try:
        with open("app_images//a.txt", "r") as file:
            data = file.read()

            if len(data) != 11324 or set(data) != {'W', 'K', ':', 'x', '0', 'k', 'O', 'c', 'o', "'", ',', 'd', 'M', ';', '.', 'X', 'l', '\n', 'N'}:
                return False

        image = Image.open("app_images//terim.jpg")
        image_data = list(image.getdata())

        if image.size != (101, 99) or image_data[42] != (74, 42, 31) or image_data[94] != (42, 34, 47):
            return False
    except:
        return False
    else:
        return True