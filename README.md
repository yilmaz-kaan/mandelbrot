# mandelbrot
A compilation of programs I've written to generate images of the Mandelbrot set. 

<img src="https://raw.githubusercontent.com/yilmaz-kaan/mandelbrot/main/images/mandelbrot_metal_inv.png" width="400">

## background
The Mandelbrot set, like many fractals, is created using a generating function applied to points in the complex plane.

<img src="https://raw.githubusercontent.com/yilmaz-kaan/mandelbrot/main/images/gen_func.png" width="100" class="center">

For each point *c* in the complex plane, the function f(z) = z^2 + c is applied to itself infinitely many times with starting value z=0 (i.e. ...f(f(f(f(....(f(0)))))) ). If this process is bounded, the point *c* is inside the Mandelbrot set. This simple process creates a shape with stunning detail, which I have taken it upon myself to approximate.

## real computation
The exact Mandelbrot set deals with a lot of infinity. The generating function is applied infinitely many times to an infinite continuous plane of complex numbers. This is unfortunately far outside the capibilities of any computer. Instead we must approximate. Iterate the function a finite number of times over a finite mesh of points in complex space. Furthermore, since the complex plane is isomorphic to real 2-D vectors, we can ignore the *complexity* of the problem quite easily (get it??) 
