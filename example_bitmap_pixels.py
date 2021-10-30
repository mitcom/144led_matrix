from matrix import (
    Matrix,
    MatrixBigPixels,
    MatrixBigPixelsWithGaps,
    MatrixLargerPixelsWithGaps,
    MatrixSmallPixelsWithGaps,
    MatrixWithGaps,
    BLACK,
)
from bitmap import read_image

print("Matrix:")
m = Matrix(16, 12, auto_show=True, fill=BLACK)
m.set_pixels(read_image("./mario.bmp"))

print("MatrixWithGaps:")
m = MatrixWithGaps(16, 12, auto_show=True, fill=BLACK)
m.set_pixels(read_image("./mario.bmp"))

print("MatrixLargerPixelsWithGaps:")
m = MatrixLargerPixelsWithGaps(16, 12, auto_show=True, fill=BLACK)
m.set_pixels(read_image("./mario.bmp"))

print("MatrixSmallPixelsWithGaps:")
m = MatrixSmallPixelsWithGaps(16, 12, auto_show=True, fill=BLACK)
m.set_pixels(read_image("./mario.bmp"))

print("MatrixBigPixelsWithGaps:")
m = MatrixBigPixelsWithGaps(16, 12, auto_show=True, fill=BLACK)
m.set_pixels(read_image("./mario.bmp"))

print("MatrixBigPixels:")
m = MatrixBigPixels(16, 12, auto_show=True, fill=BLACK)
m.set_pixels(read_image("./mario.bmp"))
