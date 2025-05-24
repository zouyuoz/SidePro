from PIL import Image, ImageTk
import numpy as np
import tkinter as tk
import sys

def generate_bayer_matrix(n):
    if n == 2:
        return np.array([[0,2],[3,1]])
    # else:
    smaller_matrix = generate_bayer_matrix(n // 2)
    return np.block([
        [4 * smaller_matrix, 4 * smaller_matrix + 2],
        [4 * smaller_matrix + 3, 4 * smaller_matrix + 1]
    ])

# 生成 16x16 Bayer 矩陣
BAYER_16X16 = generate_bayer_matrix(16)/256.

def new_w_and_h(old_w, old_h, value):
    if IS_WIDTH:
        new_width = value
        new_height = int(old_h * new_width / old_w)
        return (new_width, new_height)
    # else
    new_height = value
    new_width = int(old_w * new_height / old_h)
    return (new_width, new_height)

def shrink_image(image, char_length):
    # 讀取圖片 計算每個新 pixel 對應原圖的區塊大小
    width, height = image.size
    resized_image = image.resize(new_w_and_h(width, height, char_length))
    
	# 將調整大小後的圖片轉換為 numpy 陣列
    pixels = np.array(resized_image, dtype=np.float32)
    return pixels

def adjust_pic(image_path, new_width):
    image = Image.open(image_path).convert("L")
    resized = shrink_image(image, new_width)
    resized /= 255.
    return resized

def const_threshold(input_array, threshold):
    h, w = input_array.shape
    threshold_map = np.full((h, w), threshold, dtype=np.float32)
    return input_array > threshold_map

def ordered_dither(input_array):
    h, w = input_array.shape
    threshold_map = np.tile(BAYER_16X16, (h // 16 + 1, w // 16 + 1))[:h, :w]
    return input_array > threshold_map

def blue_noise_mask(input_array):
    h, w = input_array.shape
    blue_noise_matrix = adjust_pic("C:/Users/zyqio/source/repos/SidePro/pics/BlueNoise64.png", 64)
    threshold_map = np.tile(blue_noise_matrix, (h // 64 + 1, w // 64 + 1))[:h, :w]
    return input_array > threshold_map

def image_to_01px_3(image_path, char_length=128):
    img = adjust_pic(image_path, char_length)
    bool_np_array_const = const_threshold(img)
    bool_np_array_bayer = ordered_dither(img)
    bool_np_array_blue = blue_noise_mask(img)
    return genPixelJPG(bool_np_array_const), genPixelJPG(bool_np_array_bayer), genPixelJPG(bool_np_array_blue)

def str_to_bool(s):
    return s.lower() in ("true", "1", "yes", "y")

def genPixelJPG(bool_array):
    height, width = bool_array.shape # 取得尺寸
    img = Image.new('L', (width, height), color=255) # 建立白底圖片
    pixels = np.where(bool_array, 0, 255).astype(np.uint8) # 轉換為可寫入圖片的像素格式
    img.putdata(pixels.flatten()) # 寫入像素資料
    return img

def adjust_contrast(input_array, fix_point, factor):
    return np.clip(fix_point + factor * (input_array - fix_point), 0, 1)

class RealTimeProcessorSingle:
    def __init__(self, root, img):
        self.root = root
        self.root.title("Real-Time Image Processor")

        # 保存原始圖片矩陣
        self.original_img = img
        self.processed_img = img.copy()

        # 初始化對比度參數
        self.fix_point = 0.5
        self.factor = 1.0
        self.name = sys.argv[1][:len(sys.argv[1])-4]

        # 創建顯示區域
        self.image_label = tk.Label(self.root)
        self.image_label.pack(side="left")

        # 創建對比度調整輸入框
        tk.Label(self.root, text="Contrast Factor").pack()
        self.factor_entry = tk.Entry(self.root)
        self.factor_entry.insert(0, str(self.factor))
        self.factor_entry.pack()

        tk.Label(self.root, text="Fix Point").pack()
        self.fix_point_entry = tk.Entry(self.root)
        self.fix_point_entry.insert(0, str(self.fix_point))
        self.fix_point_entry.pack()

        # 創建更新按鈕
        self.update_button = tk.Button(self.root, text="Update", command=self.update_contrast)
        self.update_button.pack()
        
        # 創建保存按鈕
        tk.Label(self.root).pack()
        self.name_entry = tk.Entry(self.root)
        self.name_entry.insert(0, str(self.name))
        self.name_entry.pack()
        
        self.save_button = tk.Button(self.root, text="Save", command=self.save_image)
        self.save_button.pack()

        # 初始化顯示
        self.update_display()

    def update_contrast(self):
        self.name = self.name_entry.get()
        try:
            # 從輸入框獲取數值
            self.factor = float(self.factor_entry.get())
            self.fix_point = float(self.fix_point_entry.get())
        except ValueError:
            print("請輸入有效的數值")
            return

        # 調整對比度
        self.processed_img = adjust_contrast(self.original_img, self.fix_point, self.factor)
        self.update_display()

    def update_display(self):
        # 將處理後的矩陣傳入三個函數
        bool_np_array_bayer = blue_noise_mask(self.processed_img)

        # 更新顯示
        self.display_image(bool_np_array_bayer, self.image_label)

    def display_image(self, bool_array, label):
        # 將布林矩陣轉換為 PIL 圖片
        img = Image.fromarray((bool_array * 255).astype(np.uint8))

        # 調整圖片大小，保留比例
        max_size = 540
        width, height = img.size
        scale = min(max_size / width, max_size / height)
        new_width = int(width * scale)
        new_height = int(height * scale)
        resized_img = img.resize((new_width, new_height))

        # 更新到 Tkinter Label
        tk_image = ImageTk.PhotoImage(resized_img)
        label.configure(image=tk_image)
        label.image = tk_image
    
    def save_image(self):
        # 保存當前處理後的圖片
        bool_np_array_bayer = ordered_dither(self.processed_img)
        img = Image.fromarray((bool_np_array_bayer * 255).astype(np.uint8))

        # 根據 factor 和 fix_point 命名文件
        file_name = f"{self.name}_{self.factor}_{self.fix_point}.png"
        img.save(file_name)
        print(f"Image saved as {file_name}")

# 主程式
if __name__ == "__main__":
    file_name = "C:/Users/zyqio/source/repos/SidePro/pics/" + sys.argv[1]
    IS_WIDTH = sys.argv[3] == "w"
    pixels_length = int(sys.argv[2])

    # 生成浮點數矩陣
    img = adjust_pic(file_name, pixels_length)

    # 啟動 UI
    root = tk.Tk()
    app = RealTimeProcessorSingle(root, img)
    root.mainloop()