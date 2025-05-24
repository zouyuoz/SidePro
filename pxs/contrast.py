import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance
import sys

class ContrastAdjuster:
    def __init__(self, root):
        self.root = root
        self.root.title("Real-Time Contrast Adjuster")

        # 載入圖片
        self.original_image = Image.open("pics/"+FILE_NAME).convert("L")
        self.display_image = self.original_image.copy()

        # 顯示圖片的 Label
        self.image_label = tk.Label(self.root)
        self.image_label.pack()

        # 對比度調整拉桿 (0.1 ~ 3.0)
        self.scale = tk.Scale(self.root, from_=0.1, to=4.0, resolution=0.1,
                              orient="horizontal", label="Contrast Factor",
                              command=self.update_contrast)
        self.scale.set(1.0)  # 預設值
        self.scale.pack()

        self.update_image_display(self.display_image)

    def update_contrast(self, value):
        factor = float(value)
        enhancer = ImageEnhance.Contrast(self.original_image)
        self.display_image = enhancer.enhance(factor)
        self.update_image_display(self.display_image)

    def update_image_display(self, img):
        max_size = 800
        width, height = img.size
        scale = min(max_size/width, max_size/height)
        new_width = int(width*scale)
        new_height = int(height*scale)
        
        tk_image = ImageTk.PhotoImage(img.resize((new_width, new_height)))
        self.image_label.configure(image=tk_image)
        self.image_label.image = tk_image

# 主程式
if __name__ == "__main__":
    FILE_NAME = sys.argv[1]
    root = tk.Tk()
    app = ContrastAdjuster(root)
    root.mainloop()
