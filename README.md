# mandelbrot
A compilation of programs I've written to generate images of the Mandelbrot set. 

<img src="https://raw.githubusercontent.com/yilmaz-kaan/mandelbrot/main/images/mandelbrot_metal_inv.png" width="400">

## background
The Mandelbrot set, like many fractals, is created using a generating function applied to points in the complex plane.

<img src="https://raw.githubusercontent.com/yilmaz-kaan/mandelbrot/main/images/gen_func.png" width="100" class="center">

For each point *c* in the complex plane, the function f(z) = z^2 + c is applied to itself infinitely many times with starting value z=0 (i.e. ...f(f(f(f(....(f(0)))))) ). If this process is bounded, the point *c* is inside the Mandelbrot set. This simple process creates a shape with stunning detail, which I have taken it upon myself to approximate.

## real computation
The exact Mandelbrot set deals with a lot of infinity. The generating function is applied infinitely many times to an infinite continuous plane of complex numbers. This is unfortunately far outside the capibilities of any computer. Instead we must approximate. Iterate the function a finite number of times over a finite mesh of points in complex space. Furthermore, since the complex plane is isomorphic to real 2-D vectors, we can ignore the *complexity* of the problem quite easily (get it??) 

## solving my skill issues
I first made an attempt at this project about a year and a half ago (as of February 2025), with a script not dissimilar to [mandelbrot_basic](/scripts/mandelbrot_basic.py). This version was pretty poor, and used numpy's complex128 data type. Additionally, I was much more constrained on hardware back then, which I'll discuss more later on in this README.

Each pixel in the Mandelbrot set is indepdendent, and depends only on the point in the complex point it is assigned to. This is a class of problem I am told is called "embarrassingly parallel." The logic next step to a single threaded rendering pipeline is of course multithreading, which is the next script I wrote in [mandelbrot_parallel](/scripts/mandelbrot_parallel.py). It uses the **multiprocessing** library to very easily pass function execution to different processes. CPU pipelines often include a couple of ALU's, letting me use about 40-50 (Very rough estimate) for my render. This is certainly not nothing, but any computer with a dedicated GPU will have a couple thousand more sitting around doing nothing while your CPU speeds along. This leads to the logical conclusion of rendering approximations of the Mandelbrot set, GPU acceleration. 

All of the code given here was written and run on an Apple M4 Pro (14C/20). For this reason, I chose to accelerate my rendering using the Metal API. This is a pretty different ballgame to my previous experiences, and so I had to do some learning first. The highly parallel nature of this problem makes writing a GPU kernel pretty easy, and mainly involved translating my original python script to C++/MSL, though the kernel computes a single pixel rather than a column in this implementation I aptly named [mandelbrot_metal](/scripts/mandelbrot_metal.py). In hindsight, OpenCL would have been a good idea to make the code cross-platform, but its too late now :-). 


## render times
Each step up very noticeably sped up how long it took to render the images, though encoding them into a PNG file remained a bottleneck for each version. I wrote a little script to compare render times for each implementation to find out exactly how much faster each version was.
<img src="https://raw.githubusercontent.com/yilmaz-kaan/mandelbrot/main/images/compute_times.png" width="800">

