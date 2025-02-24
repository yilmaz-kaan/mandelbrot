from mandelbrot_metal import render_mandelbrot_metal #place in same directory
import tkinter as tk
from PIL import Image, ImageTk
from collections import deque

class MandelbrotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Mandelbrot Zoom")

        # Initial settings
        self.width, self.height = 884, 884  # Square image
        self.x_min, self.x_max = -2.0, 0.5
        self.y_min, self.y_max = -1.25, 1.25
        self.max_iter = 50  # Initial iteration count

        # Stack for undo functionality
        self.history = deque(maxlen=10)  # Store last 10 zoom levels

        # Render initial Mandelbrot set
        self.image, _, _, _ = self.render_mandelbrot()
        self.tk_image = ImageTk.PhotoImage(self.image)

        # Create main frame
        main_frame = tk.Frame(root)
        main_frame.pack()

        # Create canvas
        self.canvas = tk.Canvas(main_frame, width=self.width, height=self.height)
        self.canvas.pack(side=tk.LEFT)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

        # Mouse events for zoom selection
        self.canvas.bind("<ButtonPress-1>", self.start_selection)
        self.canvas.bind("<B1-Motion>", self.update_selection)
        self.canvas.bind("<ButtonRelease-1>", self.finish_selection)

        # Buttons for controls
        button_frame = tk.Frame(main_frame)
        button_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)

        self.undo_button = tk.Button(button_frame, text="Undo", command=self.undo_zoom)
        self.undo_button.pack(pady=5)

        self.increase_iter_button = tk.Button(button_frame, text="More Detail", command=self.increase_iterations)
        self.increase_iter_button.pack(pady=5)

        self.decrease_iter_button = tk.Button(button_frame, text="Less Detail", command=self.decrease_iterations)
        self.decrease_iter_button.pack(pady=5)

        self.start_x = self.start_y = None
        self.rect = None

    def render_mandelbrot(self):
        """Call the Metal-based Mandelbrot function with the current max_iter."""
        return render_mandelbrot_metal(
            self.width, self.height, self.x_min, self.x_max, self.y_min, self.y_max, self.max_iter
        )

    def start_selection(self, event):
        """Start selecting a zoom area."""
        self.start_x, self.start_y = event.x, event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline="red")

    def update_selection(self, event):
        """Restrict selection to a square while dragging."""
        size = min(abs(event.x - self.start_x), abs(event.y - self.start_y))
        x2 = self.start_x + size * (1 if event.x > self.start_x else -1)
        y2 = self.start_y + size * (1 if event.y > self.start_y else -1)
        self.canvas.coords(self.rect, self.start_x, self.start_y, x2, y2)

    def finish_selection(self, event):
        """Compute new Mandelbrot bounds and re-render the image."""
        x1, y1, x2, y2 = self.canvas.coords(self.rect)
        if x1 == x2 or y1 == y2:
            return  # Ignore clicks without dragging

        # Save current state for undo
        self.history.append((self.x_min, self.x_max, self.y_min, self.y_max, self.max_iter))

        # Convert pixel coordinates to Mandelbrot coordinates
        new_x_min = self.x_min + (x1 / self.width) * (self.x_max - self.x_min)
        new_x_max = self.x_min + (x2 / self.width) * (self.x_max - self.x_min)
        new_y_min = self.y_min + (y1 / self.height) * (self.y_max - self.y_min)
        new_y_max = self.y_min + (y2 / self.height) * (self.y_max - self.y_min)

        # Update bounds and re-render
        self.x_min, self.x_max, self.y_min, self.y_max = new_x_min, new_x_max, new_y_min, new_y_max
        self.image, _, _, _ = self.render_mandelbrot()
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def undo_zoom(self):
        """Revert to the previous zoom level."""
        if self.history:
            self.x_min, self.x_max, self.y_min, self.y_max, self.max_iter = self.history.pop()
            self.image, _, _, _ = self.render_mandelbrot()
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def increase_iterations(self):
        """Double the max_iter value and re-render."""
        self.max_iter *= 2
        self.image, _, _, _ = self.render_mandelbrot()
        self.tk_image = ImageTk.PhotoImage(self.image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

    def decrease_iterations(self):
        """Halve the max_iter value (minimum 10) and re-render."""
        if self.max_iter > 10:
            self.max_iter //= 2
            self.image, _, _, _ = self.render_mandelbrot()
            self.tk_image = ImageTk.PhotoImage(self.image)
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.tk_image)

if __name__ == "__main__":
    root = tk.Tk()
    app = MandelbrotGUI(root)
    root.mainloop()
