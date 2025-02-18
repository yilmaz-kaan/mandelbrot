import numpy as np
from PIL import Image
import time

width = 800
height = 800
xmin, xmax = -2, 1
ymin, ymax = -1.5, 1.5
max_iter = 50

"""
My first attempt at rendering approximations of the Mandelbrot set
In hindsight a naive approach but it does use symmetry to double computation speed so thats pretty neat

"""

args = (width, height, xmin, xmax, ymin, ymax, max_iter)

def compute_col(i, width, height, x_min, x_max, y_min, y_max, max_iter):
    col = np.zeros((height, 3), dtype=np.uint8)

    half_height = height // 2
    for j in range(half_height):
        x0 = x_min + (i / width) * (x_max - x_min)
        y0 = y_max - (j / height) * (y_max - y_min)
        
        x, y = 0, 0
        iteration = 0
        
        while x*x + y*y < 4 and iteration < max_iter:
            x_temp = x*x - y*y + x0
            y = 2*x*y + y0
            x = x_temp
            iteration += 1
        
        # Grayscale color mapping
        color = int(255 * iteration / max_iter)
        col[j] = (color, color, color)
        col[height - j - 1] = (color, color, color)  # Mirror symmetry
    return col

def mandelbrot(args, timing = False):
    if timing:
        start = now()
    
    width, height, x_min, x_max, y_min, y_max, max_iter = args
    im = np.zeros((height, width, 3), dtype=np.uint8)

    for i in range(width):
        im[:, i, :] = compute_col(i, width, height, x_min, x_max, y_min, y_max, max_iter)
    
    out = Image.fromarray(im)

    if timing:
        end = now()

    return out

# Generate and display
test = mandelbrot(args)
test.show()
