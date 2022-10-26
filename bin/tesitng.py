from image_converter import *

color = (12, 75, 165)
error = [0, 0, 0]
for i in range(16):
    col = get_color(*color, error)
    error = get_error(col, color)
    print(col)
    print(error)
    print()
