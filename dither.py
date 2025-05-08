import numpy as np
import sys
from PIL import Image
import bisect
import random
import numpy as np

def ordered_dither(input_array):
    # 4x4 Bayer matrix normalized to [0, 1)
    bayer = np.array([
        [0, 8, 2, 10],
        [12, 4, 14, 6],
        [3, 11, 1, 9],
        [15, 7, 13, 5]
    ]) / 16.0
    
    h, w = input_array.shape
    threshold_map = np.tile(bayer, (h // 4 + 1, w // 4 + 1))[:h, :w]
    return input_array > threshold_map

ascii_list = " -;+lH@"
lightness = [255.0000, 230.8713, 188.9039, 174.7664, 139.5745, 89.1327, 0.0]

def block_average_downsample(image, new_width, font_bbox_ratio):
    # 讀取圖片
    width, height = image.size
    pixels = np.array(image, dtype=np.float32)

    # 計算每個新 pixel 對應原圖的區塊大小
    aspect_ratio = height / width
    new_height = int(aspect_ratio * new_width * font_bbox_ratio)
    block_w = width / new_width
    block_h = height / new_height

    # 初始化輸出陣列
    downsampled = np.zeros((new_height, new_width), dtype=np.float32)

    for y in range(new_height):
        for x in range(new_width):
            # 對應的原圖區塊範圍
            x_start = int(x * block_w)
            x_end = int((x + 1) * block_w)
            y_start = int(y * block_h)
            y_end = int((y + 1) * block_h)

            block = pixels[y_start:y_end, x_start:x_end]
            downsampled[y, x] = np.mean(block)

    return downsampled  # 每個值為 float 灰階 0~255

def find_light_index(value, lightness_list):
    if value in lightness_list: return lightness_list.index(value)
    
    reversed_lightness = list(reversed(lightness_list))
    index = bisect.bisect_left(reversed_lightness, value)
    lower = reversed_lightness[index - 1]
    upper = reversed_lightness[index]
    
    prob = (upper - value) / (upper - lower)
    LEN = len(lightness_list) - 1
    return LEN - (index - 1) if random.random() < prob else LEN - index

def gray_to_ascii(value, ascii_list, inv):
    # 將 0~255 映射到 0~(num_chars-1) 的浮點數
    if (inv): value = 255 - value
    value /= 255.
    return ascii_list[find_light_index(value, lightness)]

def str_to_bool(s):
    return s.lower() in ("true", "1", "yes", "y")

# =============
# program start
# =============

# 載入圖片
file_name = sys.argv[1]
vscode = str_to_bool(sys.argv[2])
image = Image.open("pics/" + file_name).convert("L")

# 調整尺寸
new_width = 128
font_bbox_ratio = 0.455 if vscode else 0.48
resized = block_average_downsample(image, new_width, font_bbox_ratio)
resized /= 255.
if not vscode: resized = 1 - resized

# 轉換為 ASCII 字串
# 假設 resized 是 2D: resized[y][x] = 0~255 float
result = ordered_dither(resized)
ascii_img = []
for line in result:
    ascii_img.append(''.join("*" if c else " " for c in line))

# print(ascii_img)
# 或寫入文字檔
with open('ascii_art.txt', 'w') as f:
    for line in ascii_img:
        f.write(line + "\n")

print("ascii art generated successfully.")