import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class PolygonClipperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Лабораторная работа")

        self.create_widgets()

    def create_widgets(self):
        input_frame = tk.Frame(self.root, padx=10, pady=10)
        input_frame.pack(side=tk.TOP, fill=tk.X)

        tk.Label(input_frame, text="Polygon Vertices").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.poly_entry = tk.Entry(input_frame, width=50)
        self.poly_entry.grid(row=0, column=1, pady=5, padx=5)
        self.poly_entry.insert(0, "100, 200, 300, 400, 500, 300, 400, 100, 200, 100")

        tk.Label(input_frame, text="Clipping Window:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.clip_entry = tk.Entry(input_frame, width=50)
        self.clip_entry.grid(row=1, column=1, pady=5, padx=5)
        self.clip_entry.insert(0, "150, 150, 450, 150, 450, 350, 150, 350")

        button_frame = tk.Frame(input_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        tk.Button(button_frame, text="Clip Polygon", command=self.clip_polygon).grid(row=0, column=0, padx=5)
        tk.Button(button_frame, text="Save Image", command=self.save_image).grid(row=0, column=1, padx=5)

        self.canvas_frame = tk.Frame(self.root, bg='white')
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)

    def clip_polygon(self):
        poly_coords = list(map(int, self.poly_entry.get().split(',')))
        clip_coords = list(map(int, self.clip_entry.get().split(',')))

        polygon = np.array(poly_coords).reshape(-1, 2)
        clipping_window = np.array(clip_coords).reshape(-1, 2)

        fig, ax = plt.subplots(figsize=(6, 6))
        ax.set_xlim(0, 600)
        ax.set_ylim(0, 600)
        ax.set_facecolor('white')


        clip_path = Polygon(clipping_window, closed=True, fill=False, edgecolor='red', ls='--')
        ax.add_patch(clip_path)

        clipped_polygon = self.sutherland_hodgman(polygon, clipping_window)

        poly_patch = Polygon(polygon, closed=True, fill=False, edgecolor='blue', lw=1.5)
        ax.add_patch(poly_patch)

        if clipped_polygon.size > 0:
            clipped_patch = Polygon(clipped_polygon, closed=True, color='green', alpha=0.5)
            ax.add_patch(clipped_patch)

        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        
        self.canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        self.canvas.draw()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def sutherland_hodgman(self, subjectPolygon, clipPolygon):
        def inside(p, cp1, cp2):
            return (cp2[0] - cp1[0]) * (p[1] - cp1[1]) > (cp2[1] - cp1[1]) * (p[0] - cp1[0])

        def intersection(cp1, cp2, s, e):
            dc = [cp1[0] - cp2[0], cp1[1] - cp2[1]]
            dp = [s[0] - e[0], s[1] - e[1]]
            n1 = cp1[0] * cp2[1] - cp1[1] * cp2[0]
            n2 = s[0] * e[1] - s[1] * e[0]
            n3 = 1.0 / (dc[0] * dp[1] - dc[1] * dp[0])
            return [(n1 * dp[0] - n2 * dc[0]) * n3, (n1 * dp[1] - n2 * dc[1]) * n3]

        outputList = subjectPolygon
        cp1 = clipPolygon[-1]

        for cp2 in clipPolygon:
            inputList = outputList
            outputList = []
            if len(inputList) == 0:
                break
            s = inputList[-1]

            for e in inputList:
                if inside(e, cp1, cp2):
                    if not inside(s, cp1, cp2):
                        outputList.append(intersection(cp1, cp2, s, e))
                    outputList.append(e)
                elif inside(s, cp1, cp2):
                    outputList.append(intersection(cp1, cp2, s, e))
                s = e
            cp1 = cp2
        return np.array(outputList)

    def save_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
        if file_path:
            self.canvas.print_png(file_path)

if __name__ == "__main__":
    root = tk.Tk()
    app = PolygonClipperApp(root)
    root.mainloop()
