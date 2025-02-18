from time import time as now
from array import array
import metalcompute as mc
from PIL.Image import frombuffer

#------------------- WARNING --------------------
# This code will only work on Apple Silicon computers!
# For GPU acceleration with other hardware, 
# adapt this code to CUDA or HIP or OpenCL or something else idk

def render_mandelbrot_metal(width, height, iterations=50, device_index=-1, output_file="mandelbrot_metal.png", timing = False):
    """
    Render the Mandelbrot set using Metal API and measure the computation time.
    
    Args:
        width (int): Width of the image.
        height (int): Height of the image.
        iterations (int): Number of iterations for Mandelbrot computation.
        device_index (int): Metal device index (-1 for default device).
        output_file (str): Output filename for the rendered image.
    
    Returns:
        tuple: (render_time, write_time, total_time)
    """
    inner_iter = 16
    outer_iter = iterations // inner_iter
    iterations = inner_iter * outer_iter

    kernel_code = """
    #include <metal_stdlib>
    using namespace metal;

    kernel void mandelbrot(const device float *uniform [[ buffer(0) ]],
                           device uchar4 *out [[ buffer(1) ]],
                           uint id [[ thread_position_in_grid ]]) {
        float width = uniform[0];
        float height = uniform[1];

        float2 c = 2.5 * (float2((id % int(width)) / width - 0.5, 
                                 0.5 - (id / int(width)) / height));
        c.x -= 0.7;
        float2 z = c;
        float done = 0.0, steps = 1.0, az = 0.0;

        float maxiter = 100;
        for (int iter = 256; iter > 0; iter--) {
            for (int i = 0; i < 16; i++) {
                z = float2((z.x * z.x) - (z.y * z.y) + c.x, (2.0 * z.x * z.y) + c.y);
                az = (z.x * z.x) + (z.y * z.y);
                done = az >= 4.0 ? 1.0 : 0.0;
                if (done > 0.0) break;
                steps += 1.0;
            }
            if (done > 0.0) break;
        }

        if (done == 0.0) {
            steps = maxiter;
        }

        if (az > 1.0) {
            steps -= log(log(sqrt(az))) / log(2.0);
        }

        float brightness = (steps / maxiter) * 255.0;
        uchar color = uchar(brightness);

        out[id] = uchar4(color, color, color, 255);
    }
    """

    dev = mc.Device(device_index)
    render_fn = dev.kernel(kernel_code).function("mandelbrot")
    image = dev.buffer(height * width * 4)
    args_buf = array('f', [width, height])

    if timing:
        start_render = now()

    render_fn(width * height, args_buf, image)

    if timing:
        end_render = now()

    image_buf = frombuffer("RGBA", (width, height), data=image)
    if output_file.lower().endswith("jpg"):
        image_buf = image_buf.convert('RGB')

    if timing:
        start_write = now()

    image_buf.save(output_file)
    
    if timing:
        end_write = now()

        total_time = end_write - start_render
        render_time = end_render - start_render
        write_time = end_write - start_write
        print(f"Render took {render_time:.6f}s")
        print(f"Image encoding took {write_time:.6f}s")
        print(f"Total processing time: {total_time:.6f}s")

        return image, render_time, write_time, total_time

    
    return image_buf, None, None, None


def benchmark_metal():
    """Runs a benchmark for Mandelbrot rendering at different sizes."""
    sizes = [2 ** k for k in range(5, 15)]
    times = []
    tot_times = []
    
    for size in sizes:
        print(f"\nRunning Mandelbrot Metal Render for {size}x{size}")
        _, render_time, write_time, total_time = render_mandelbrot_metal(size, size, timing=True)
        times.append((size, render_time, write_time, total_time))
        tot_times.append(total_time)

    print("\nBenchmark Results:")
    for size, render_time, write_time, total_time in times:
        print(f"Size: {size}x{size} | Render: {render_time:.6f}s | Write: {write_time:.6f}s | Total: {total_time:.6f}s")
    
    return times

if __name__ == "__main__":
    render_mandelbrot_metal(2 ** 10 - 1, 2 ** 10 - 1, iterations=1000, device_index=-1, output_file="mandelbrot_metal.png")




