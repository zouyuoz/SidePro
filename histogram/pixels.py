from PIL import Image, ImageTk
import numpy as np
import tkinter as tk
import sys
from skimage import exposure



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
BAYER_16X16 = generate_bayer_matrix(16)





# below are main HE & CLAHE function:

def histogram_equalization_2d(arr):
    flat = arr.flatten()
    
    # 轉為整數 bins（0~255）做 histogram 分類
    hist, bins = np.histogram(flat, bins=256, range=(0, 255))
    cdf = hist.cumsum()
    cdf_normalized = cdf / cdf[-1]  # Normalize to [0,1]

    # 建立映射表
    equalized_map = np.interp(flat, bins[:-1], cdf_normalized * 255)

    # reshape 回原來形狀
    return equalized_map.reshape(arr.shape)

def clip_limit_adaptive_histogram_equalization(arr):
    print("using clahe.")
    float_0_1 = arr / 255.
    clahe_img = exposure.equalize_adapthist(float_0_1, clip_limit=0.015)
    clahe_img = (clahe_img * 255).astype(np.uint8)
    return clahe_img

# above are main HE & CLAHE function:





def new_w_and_h(old_w, old_h, value):
    if IS_WIDTH:
        new_width = value
        new_height = int(old_h  * new_width / old_w)
        return (new_width, new_height)
    # else
    new_height = value
    new_width = int(old_w * new_height / old_h)
    return (new_width, new_height)

def adjust_pic(image_path, new_width):
    # 讀取圖片
    image = Image.open(image_path).convert("L")
    width, height = image.size
    resized = image.resize(new_w_and_h(width, height, new_width), Image.Resampling.BOX)
    # 將調整大小後的圖片轉換為 numpy 陣列
    float_array = np.array(resized, dtype=np.float32)
    return float_array



def const_threshold(input_array, threshold=140):
    h, w = input_array.shape
    threshold_map = np.full((h, w), threshold, dtype=np.float32)
    return input_array < threshold_map

def ordered_dither(input_array):
    h, w = input_array.shape
    threshold_map = np.tile(BAYER_16X16, (h // 16 + 1, w // 16 + 1))[:h, :w]
    return input_array < threshold_map

def blue_noise_mask(input_array):
    h, w = input_array.shape
    blue_noise_matrix = adjust_pic("C:/Users/zyqio/source/repos/SidePro/pics/BlueNoise64.png", 64)
    threshold_map = np.tile(blue_noise_matrix, (h // 64 + 1, w // 64 + 1))[:h, :w]
    return input_array < threshold_map



def str_to_bool(s):
    return s.lower() in ("true", "1", "yes", "y")

def genPixelJPG(bool_array):
    height, width = bool_array.shape # 取得尺寸
    img = Image.new('L', (width, height), color=255) # 建立白底圖片
    pixels = np.where(bool_array, 0, 255).astype(np.uint8) # 轉換為可寫入圖片的像素格式
    img.putdata(pixels.flatten()) # 寫入像素資料
    return img





file_name = "C:/Users/zyqio/source/repos/SidePro/pics/" + sys.argv[1]
pixels_length = int(sys.argv[2])
IS_WIDTH = sys.argv[3] == "w"

USING_CLAHE = 0

float_0_255 = adjust_pic(file_name, pixels_length)

he = histogram_equalization_2d(float_0_255)
if USING_CLAHE: he = clip_limit_adaptive_histogram_equalization(float_0_255)
bool_image = genPixelJPG(blue_noise_mask(he))

# true_count, false_count = 0, 0
# for row in AAAA:
#     print(row)
#     for pixels in row:
#         if pixels: true_count += 1
#         else: false_count += 1
# print(true_count, false_count)

bool_image.save("output.png")