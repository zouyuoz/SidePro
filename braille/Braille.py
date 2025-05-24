from PIL import Image
import numpy as np
import sys

bayer = np.array([
    [ 0,  8,  2, 10],
    [12,  4, 14,  6],
    [ 3, 11,  1,  9],
    [15,  7, 13,  5]
]) / 16.0

big_bayer = np.array([
    [ 0, 32,  8, 40,  2, 34, 10, 42],
    [48, 16, 56, 24, 50, 18, 58, 26],
    [12, 44,  4, 35, 14, 46,  6, 38],
    [60, 28, 52, 20, 62, 30, 54, 22],
    [ 3, 35, 11, 43,  1, 33,  9, 41],
    [51, 19, 59, 27, 49, 17, 57, 25],
    [15, 47,  7, 39, 13, 45,  5, 37],
    [63, 31, 55, 23, 61, 29, 53, 21]
]) / 64.

def new_w_and_h(old_w, old_h, value):
    if IS_WIDTH:
        new_width = value
        new_height = int(old_h * FONT_BBOX_RATIO * new_width / old_w)
        return (new_width, new_height)
    # else
    new_height = value
    new_width = int(old_w * new_height / (old_h * FONT_BBOX_RATIO))
    return (new_width, new_height)

def block_average_downsample(image, char_length):
    # 讀取圖片
    width, height = image.size
    pixels = np.array(image, dtype=np.float32)

    # 計算每個新 pixel 對應原圖的區塊大小
    new_width, new_height = new_w_and_h(width, height, char_length)
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

def adjust_pic(image_path, vscode, new_width):
    image = Image.open(image_path).convert("L")
    resized = block_average_downsample(image, new_width)
    resized /= 255.
    if not vscode: resized = 1 - resized
    return resized

def ordered_dither(input_array):
    h, w = input_array.shape
    threshold_map = np.tile(big_bayer, (h // 8 + 1, w // 8 + 1))[:h, :w]
    return input_array > threshold_map

def value_2x4(arr):
    ascii_lines = []
    width = 2
    height = 4
    
    h, w = arr.shape
    num_rows = h // height
    num_cols = w // width
    
    for row in range(num_rows):
        line = ""
        for col in range(num_cols):
            y_start = row * height
            y_end = (row + 1) * height
            x_start = col * width
            x_end = (col + 1) * width
            
            grid = arr[y_start:y_end, x_start:x_end]
            line += braille_char(braille_value(grid))
        ascii_lines.append(line)
    
    return ascii_lines

braille_index_map = [
    (0,0), (1,0), (2,0),
    (0,1), (1,1), (2,1),
    (3,0), (3,1),
]

def braille_value(grid):
    total = 0
    for i, (dy, dx) in enumerate(braille_index_map):
        if dy < grid.shape[0] and dx < grid.shape[1] and grid[dy, dx]:
            total |= (1 << i)
    return total

def braille_char(value):
    if (value == 0): return chr(0x2801)
    return chr(0x2800 + value)

def image_to_braille_bayer(image_path, vscode, char_length=128):
    img = adjust_pic(image_path, vscode, char_length)
    # below is extended function
    img = np.clip(FIX_POINT + FACTOR * (img - FIX_POINT), 0, 1)
    # above is extended function
    bool_np_array = ordered_dither(img)
    braille_array = value_2x4(bool_np_array)
    return braille_array

def str_to_bool(s):
    return s.lower() in ("true", "1", "yes", "y")

# 執行並輸出
file_name = "C:/Users/zyqio/source/repos/SidePro/pics/" + sys.argv[1]
vscode = str_to_bool(sys.argv[2])
FONT_BBOX_RATIO = 1.13 if vscode else 1.11
IS_WIDTH = sys.argv[4] == "w"
char_length = int(sys.argv[3]) * 2
if not IS_WIDTH: char_length *= 2

FIX_POINT = float(input("fix point: "))
FACTOR = float(input("factor: "))

braille_string = image_to_braille_bayer(file_name, vscode, char_length)

with open('braille/braille.txt', 'w') as f:
    for line in braille_string:
        f.write(line + "\n")
