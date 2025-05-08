import sys
from PIL import Image
import bisect
import random
import numpy as np

# Fira Code
fira_code_ascii_list = " `'.-_,:~\"^!=+;|><\\/?7()lLcvtiTJ{*}jYzxr1f4[]suFnCIy23VZoa5ehXkPEUS9KA6Hqpd&bOG#mDRw8QBgN0%$@MW"
fira_code_lightness = [255.0000, 236.1338, 223.7690, 223.0330, 218.8623, 207.9450, 203.3818, 201.4191, 200.9039, 192.4399, 191.7039, 187.7295, 186.5028, 175.4137, 174.3588, 168.6425, 167.1214, 166.9742, 166.8025, 166.7289, 159.0745, 156.9155, 155.9097, 155.0019, 154.8057, 153.8734, 153.0883, 153.0638, 149.3838, 148.6232, 143.4467, 141.6803, 141.6312, 141.3123, 141.1651, 140.6008, 140.2574, 139.8894, 139.6686, 138.9571, 138.6872, 138.1966, 135.2035, 135.1299, 135.1053, 133.4125, 132.4312, 131.1800, 130.9592, 129.5117, 129.4136, 125.6355, 125.3165, 124.4579, 122.4216, 118.9133, 118.1528, 115.9938, 115.8221, 111.0136, 109.7624, 108.8792, 105.7389, 103.5799, 103.1138, 100.3906, 100.3661, 94.2082, 94.1101, 93.5213, 91.1415, 91.0434, 89.4242, 87.8541, 87.6087, 87.1916, 84.6647, 83.7815, 79.8071, 78.5559, 75.8082, 74.7042, 70.5825, 69.3804, 69.1596, 57.5063, 56.6967, 49.7537, 49.2140, 43.7676, 23.3558, 21.0742, 4.4651, 3.9989, 0.0000]

# consolas
consolas_ascii_list = " `.-':_,~^\";=!><+cr/\\?z*vLsTi7|)J(xtnu}l{CFo1yY[I]3fjZea52wSEkhPVqp6KmU94bGdXAOHRD#8N0MBW$g%Q&@"
consolas_lightness = [255.0000, 237.8490, 234.4511, 230.8713, 222.7407, 217.3001, 209.6145, 207.7740, 195.2141, 195.0928, 192.7669, 188.9039, 185.6274, 180.0048, 177.1732, 177.1530, 174.7664, 169.9124, 168.2337, 168.0112, 167.9707, 164.1886, 162.6919, 161.4987, 160.0222, 159.3345, 155.8356, 151.2040, 151.0220, 150.7995, 149.1815, 147.7455, 147.6241, 147.5230, 147.2398, 142.6083, 141.2532, 141.0105, 139.8981, 139.5745, 139.3318, 139.2306, 138.0576, 137.7542, 136.5811, 135.8126, 135.3878, 134.9833, 133.8507, 133.8507, 133.1833, 132.6979, 132.4350, 131.3428, 129.1180, 128.8146, 128.1877, 127.4595, 126.5090, 123.6370, 115.7491, 114.1513, 112.9176, 112.6951, 108.4478, 106.6275, 105.9803, 105.7983, 104.7668, 104.2207, 103.9174, 103.7758, 101.9555, 101.9353, 101.0858, 99.9532, 90.7103, 90.5485, 90.2653, 89.1327, 87.7776, 80.6583, 80.2538, 77.2200, 72.1233, 70.8895, 67.0063, 66.9456, 65.2669, 61.2421, 60.5140, 57.8442, 55.4576, 45.1023, 0.0000]

DITHER = False
if DITHER:
    fira_code_ascii_list = " iJoW"
    fira_code_lightness = [255.0000, 148.6232, 141.6803, 118.1528, 0.0000]
    consolas_ascii_list = " -;+lH@"
    consolas_lightness = [255.0000, 230.8713, 188.9039, 174.7664, 139.5745, 89.1327, 0.0]

NMIXX = False
if NMIXX:
    consolas_ascii_list = " -;ixnImXNM"
    consolas_lightness = [255.0000, 230.8713, 188.9039, 151.0220, 147.2398, 141.2532, 133.8507, 104.2207, 90.7103, 72.1233, 0.0]

JIWOO = False
if JIWOO:
    fira_code_ascii_list = " -:iJjIoOwW"
    fira_code_lightness = [255.0000, 218.8623, 201.4191, 148.6232, 141.6803, 140.6008, 129.4136, 118.1528, 83.7815, 69.3804, 0.0000]
    
UNI = False
if UNI:
    consolas_ascii_list = " -:inuIUN@"
    consolas_lightness = [255.0000, 230.8713, 217.3001, 151.0220, 141.2532, 141.0105, 133.8507, 103.9174, 72.1233, 0.0000]
    fira_code_ascii_list = " -:iunIUN@"
    fira_code_lightness = [255.0000, 218.8623, 201.4191, 148.6232, 132.4312, 130.9592, 129.4136, 100.3906, 49.2140, 0.0]

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
    lightness_list = fira_code_lightness if inv else consolas_lightness
    return ascii_list[find_light_index(value, lightness_list)]

def str_to_bool(s):
    return s.lower() in ("true", "1", "yes", "y")

# =============
# program start
# =============

# 載入圖片
file_name = sys.argv[1]
vscode = str_to_bool(sys.argv[2])
image = Image.open("pics/" + file_name).convert("L")
# if not vscode: consolas_ascii_list = " `.-':_,~^\";=!><+cr/\\?z*vLsTi7|)J(xtnu}l{CFo1yY[I]3fjZea52wSEkhPVqp6KmU94bGdXAOHRD#8g0MBW$N%Q&@"
# 調整尺寸
'''
width, height = image.size
aspect_ratio = height / width
new_width = 164 if vscode else 150 # horizontal vscode = 164 else 100 (verti)
font_bbox_ration = 0.455 if vscode else 0.51
new_height = int(aspect_ratio * new_width * font_bbox_ration)
resized = image.resize((new_width, new_height))
'''
new_width = 100 if vscode else 320 # horizontal vscode = 164 else 100 (verti), text editor 150
font_bbox_ratio = 0.455 if vscode else 0.48
resized = block_average_downsample(image, new_width, font_bbox_ratio)

# print(resized)
# exit()

# 轉換為 ASCII 字串
ascii_list = fira_code_ascii_list if vscode else consolas_ascii_list
# 假設 resized 是 2D: resized[y][x] = 0~255 float
ascii_lines = []
for row in resized:
    line = ''.join([gray_to_ascii(p, ascii_list, vscode) for p in row])
    ascii_lines.append(line)

ascii_img = '\n'.join(ascii_lines)

# print(ascii_img)
# 或寫入文字檔
with open('ascii_art.txt', 'w') as f:
    f.write(ascii_img)

print("ascii art generated successfully.")