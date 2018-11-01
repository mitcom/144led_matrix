from PIL import Image

def read_image(filename):
    image = Image.open(filename)
    image = image.convert('RGB')
    return iterable_image_interface(image)

def iterable_image_interface(image):
    def pixel_iterator(row_number):
        for x in range(image.width):
            yield image.getpixel((x, row_number))

    for y in range(image.height):
        yield pixel_iterator(y)
