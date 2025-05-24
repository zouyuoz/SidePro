from PIL import Image, ImageTk
import numpy as np
import tkinter as tk
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
        new_height = int(old_h  * new_width / old_w)
        return (new_width, new_height)
    # else
    new_height = value
    new_width = int(old_w * new_height / old_h)
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

def adjust_pic(image_path, new_width):
    image = Image.open(image_path).convert("L")
    resized = block_average_downsample(image, new_width)
    resized /= 255.
    return resized

def const_threshold(input_array, threshold=0.45):
    h, w = input_array.shape
    threshold_map = np.full((h, w), threshold, dtype=np.float32)
    return input_array < threshold_map

def ordered_dither(input_array):
    h, w = input_array.shape
    threshold_map = np.tile(big_bayer, (h // 8 + 1, w // 8 + 1))[:h, :w]
    return input_array < threshold_map

def blue_noise_mask(input_array):
    h, w = input_array.shape
    blue_noise_matrix = adjust_pic("C:/Users/zyqio/source/repos/SidePro/pics/BlueNoise470.png", 470)
    threshold_map = np.tile(blue_noise_matrix, (h // 470 + 1, w // 470 + 1))[:h, :w]
    return input_array < threshold_map

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

def combine_three_images(img_const_threshold, img_bayer_matrix, img_blue_noise, output_path="output.png"):
    # 假設所有圖片大小一致
    width, height = img_const_threshold.size

    if width > height:
        # 上下合併
        new_img = Image.new("L", (width, height * 3))
        new_img.paste(img_const_threshold, (0, 0))
        new_img.paste(img_bayer_matrix, (0, height))
        new_img.paste(img_blue_noise, (0, 2 * height))
    else:
        # 左右合併
        new_img = Image.new("L", (width * 3, height))
        new_img.paste(img_const_threshold, (0, 0))
        new_img.paste(img_bayer_matrix, (width, 0))
        new_img.paste(img_blue_noise, (2 * width, 0))

    # 儲存結果
    new_img.save(output_path)

file_name = "C:/Users/zyqio/source/repos/SidePro/pics/" + sys.argv[1]
IS_WIDTH = sys.argv[3] == "w"
pixels_length = int(sys.argv[2])

img1, img2, img3 = image_to_01px_3(file_name, pixels_length)

img2.save("output.png")

# combine_three_images(img1, img2, img3)