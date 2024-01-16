import tkinter as tk
from tkinter import filedialog, messagebox


class PixelArtEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Pixel Art Editor")
        self.root.geometry("300x140")
        self.root.resizable(width=False, height=False)

        self.open_menu()

    def open_menu(self):
        menu_frame = tk.Frame(self.root)
        menu_frame.pack(pady=20)

        width_label = tk.Label(menu_frame, text="Width:")
        width_label.grid(row=0, column=0, padx=5, pady=5)
        self.width_entry = tk.Entry(menu_frame)
        self.width_entry.grid(row=0, column=1, padx=5, pady=5)

        height_label = tk.Label(menu_frame, text="Height:")
        height_label.grid(row=1, column=0, padx=5, pady=5)
        self.height_entry = tk.Entry(menu_frame)
        self.height_entry.grid(row=1, column=1, padx=5, pady=5)

        continue_button = tk.Button(menu_frame, text="Continue", command=self.open_canvas_with_palette)
        continue_button.grid(row=2, column=0, columnspan=2, pady=10)

    def open_canvas_with_palette(self):
        width_str = self.width_entry.get()
        height_str = self.height_entry.get()

        if not width_str or not height_str:
            messagebox.showerror("Error", "Please enter the width and height of the canvas.")
            return

        width = int(width_str)
        height = int(height_str)

        self.root.destroy()

        self.root = tk.Tk()
        self.root.title("Pixel Art Editor")
        self.root.resizable(width=False, height=False)

        self.canvas_size = (width, height)
        self.current_color = "black"
        self.transparent_color = (0, 0, 0, 0)
        self.palette = ["#000000", "#FFFFFF", "#FF0000", "#00FF00", "#0000FF", "#FFFF00", "#800080", "#00FFFF", "#FFA500", "#FFC0CB", "#A52A2A", "#808080"]

        self.canvas = tk.Canvas(self.root, width=self.canvas_size[0] * 20, height=self.canvas_size[1] * 20, bg="#2F4F4F", highlightthickness=0)
        self.canvas.pack()

        self.palette_window = tk.Toplevel(self.root)
        self.palette_window.title("Palette")
        self.palette_window.resizable(width=False, height=False)

        self.palette_canvas = tk.Canvas(self.palette_window)
        self.palette_canvas.pack()

        menu_bar = tk.Menu(self.root)
        self.root.config(menu=menu_bar)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        menu_bar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Save", command=self.save_image)
        file_menu.add_command(label="Load Palette", command=self.load_palette)
        file_menu.add_command(label="Save Palette", command=self.save_palette)

        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.draw)
        self.canvas.bind("<ButtonRelease-3>", self.erase)
        self.canvas.bind("<B3-Motion>", self.erase)
        self.canvas.bind("<Button-2>", self.copy_color)
        self.palette_canvas.bind("<Button-1>", self.select_color)

        self.update_palette()

    def draw(self, event):
        x, y = event.x // 20, event.y // 20
        self.canvas.create_rectangle(x * 20, y * 20, (x + 1) * 20, (y + 1) * 20, fill=self.current_color, outline='')

    def erase(self, event):
        x, y = event.x // 20, event.y // 20
        items = self.canvas.find_overlapping(x * 20, y * 20, (x + 1) * 20, (y + 1) * 20)
        for item in items:
            self.canvas.delete(item)

    def copy_color(self, event):
        x, y = event.x // 20, event.y // 20
        pixel_color = self.canvas.itemcget(self.canvas.find_closest(event.x, event.y)[0], "fill")
        self.current_color = pixel_color

    def select_color(self, event):
        pixel_color = self.palette_canvas.itemcget(self.palette_canvas.find_closest(event.x, event.y)[0], "fill")
        self.current_color = pixel_color

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            image = tk.PhotoImage(width=self.canvas_size[0], height=self.canvas_size[1])

            for item in self.canvas.find_all():
                coords = self.canvas.coords(item)
                x, y = int(max(coords[0] // 20, 0)), int(max(coords[1] // 20, 0))
                color = self.canvas.itemcget(item, "fill")
                image.put(color, (x, y))

            image.write(file_path, format="png")

    def load_palette(self):
        file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "r") as file:
                self.palette = [line.strip() for line in file.readlines()]
            self.update_palette()

    def save_palette(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if file_path:
            with open(file_path, "w") as file:
                file.write("\n".join(self.palette))

    def update_palette(self):
        self.palette_canvas.delete("all")

        colors_per_row = 6
        num_rows = (len(self.palette) + colors_per_row - 1) // colors_per_row

        palette_width = min(colors_per_row, len(self.palette)) * 40
        palette_height = num_rows * 40

        self.palette_window.geometry(f"{palette_width}x{palette_height}")

        for i, color in enumerate(self.palette):
            row = i // colors_per_row
            col = i % colors_per_row
            self.palette_canvas.create_rectangle(col * 40, row * 40, (col + 1) * 40, (row + 1) * 40, fill=color, outline='')

        if len(self.palette) % colors_per_row != 0:
            last_color = self.palette[-1]
            for col in range(len(self.palette) % colors_per_row, colors_per_row):
                self.palette_canvas.create_rectangle(col * 40, row * 40, (col + 1) * 40, (row + 1) * 40, fill=last_color, outline='')

if __name__ == "__main__":
    root = tk.Tk()
    app = PixelArtEditor(root)
    root.mainloop()
