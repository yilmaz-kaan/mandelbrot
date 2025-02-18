from PIL import Image
import numpy as np
import multiprocessing
from time import time as now

def compute_col(args):
    i, width, height, x_min, x_max, y_min, y_max, max_iter = args
    row = np.zeros((height // 2, 3), dtype=np.uint8)
    
    for j in range(height // 2):
        x0 = x_min + (i / width) * (x_max - x_min)
        y0 = y_max - (j / height) * (y_max - y_min)
        
        x, y = 0, 0
        iteration = 0
        
        while x*x + y*y < 4 and iteration < max_iter:
            x_temp = x*x - y*y + x0
            y = 2*x*y + y0
            x = x_temp
            iteration += 1
        
        color = int(255 * iteration / max_iter)  # Grayscale mapping
        row[j] = (color, color, color)
    
    return i, row

def mandelbrot_parallel(width, height, x_min, x_max, y_min, y_max, max_iter, timing=False):
    """
    Generates the Mandelbrot set using multiprocessing for increased speed.
    If timing=True, returns the computation time.
    """
    image_data = np.zeros((height, width, 3), dtype=np.uint8)

    if timing:
        start = now()

    with multiprocessing.Pool() as pool:
        args_list = [(i, width, height, x_min, x_max, y_min, y_max, max_iter) for i in range(width)]
        results = pool.map(compute_col, args_list, chunksize=10)
    
    for i, row in results:
        image_data[:height // 2, i] = row
        image_data[height // 2:, i] = row[::-1]  # Reflect the top half to the bottom

    im = Image.fromarray(image_data)

    if timing:
        end = now()
        return im, (end - start)

    return im, None

if __name__ == "__main__":
    # All multithreaded computation must be performed inside a __main__ block like this one
    # Parameters
    x_min, x_max = -2, 1
    y_min, y_max = -1.5, 1.5
    max_iter = 50
    par_times = []

    # Generate and save image
    for k in range(5, 15):
        size = 2 ** k
        _, time = mandelbrot_parallel(size, size, x_min, x_max, y_min, y_max, max_iter, timing=True)
        par_times.append(time)
        print(f'Size: {size}x{size}, Time: {time} seconds')

    print(par_times)
    # image.save(f"mandebrot{width}x{height}.png")
