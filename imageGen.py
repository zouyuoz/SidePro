import sys
from PIL import Image
import bisect
import numpy as np

bayer = np.array([
    [ 0,  8,  2, 10],
    [12,  4, 14,  6],
    [ 3, 11,  1,  9],
    [15,  7, 13,  5]
]) / 16.0

def str_to_bool(s):
    return s.lower() in ("true", "1", "yes", "y")

# =============
# program start
# =============

# 載入圖片
file_name = sys.argv[1]
VSCODE = str_to_bool(sys.argv[2])
char_length = int(sys.argv[3])
IS_WIDTH = sys.argv[4] == "w"
image = Image.open("pics/" + file_name).convert("L")

# Fira Code
ascii_list = " `'.-:~!=+;|></\\?7)(vlLctiTrJ*zYxf1j{}4][sunFIC32VoZ5aehXkEPSU9KA6Hqpd&bOG#mDR8BQN0%$@MW"
lightness = [255.0000, 235.9793, 223.6357, 222.2207, 218.8208, 201.0314, 200.6700, 187.7261, 186.3968, 175.7746, 174.2248, 168.1602, 167.3822, 167.1556, 166.7329, 166.3960, 159.4431, 157.2072, 156.3741, 156.2638, 154.0402, 153.9176, 153.3234, 153.0600, 149.4948, 148.3615, 143.3138, 141.5373, 141.4577, 141.1024, 140.5817, 139.8895, 139.5403, 139.4423, 139.4239, 139.3198, 138.3213, 138.2110, 136.4897, 135.7301, 135.6627, 133.1143, 132.1342, 131.4420, 131.1847, 128.7589, 128.6180, 126.5474, 125.7388, 122.1675, 120.3910, 118.5716, 117.1443, 114.1855, 111.8087, 110.2956, 109.2420, 106.3689, 103.1590, 102.6873, 102.2156, 101.9093, 96.6227, 94.5093, 92.8431, 92.8370, 90.8277, 89.3208, 88.6530, 87.4708, 86.4477, 86.2701, 81.2163, 80.3219, 78.4413, 75.8684, 74.0123, 70.9555, 69.3077, 56.2719, 54.9487, 49.7111, 45.6374, 22.0897, 17.6424, 4.4167, 4.2636, 0.0000]

# consolas
if not VSCODE:
    ascii_list = " `.-':~;!>=</\\*+?rcL)(|T7JvsizltFY{}C1[I]xf3nujo25eSaVEkPZhUKX469bdqGpOHmARD#8NW0M%B$Q&@"
    lightness = [255.0000, 238.0589, 228.4908, 228.2314, 227.0591, 210.8762, 197.0380, 185.4346, 180.8401, 178.2561, 178.0166, 177.8919, 172.4643, 172.4444, 171.1673, 171.0626, 161.6741, 160.3372, 159.0950, 157.4189, 152.5201, 152.3056, 150.5995, 148.7338, 145.4364, 143.6105, 142.9969, 142.0391, 139.7494, 138.5721, 136.5218, 134.6112, 134.1921, 133.1845, 133.0647, 132.9600, 129.9469, 129.8920, 129.8421, 129.4879, 128.9891, 128.9841, 127.6621, 127.5424, 126.7442, 126.5846, 121.6409, 121.3915, 121.3267, 121.3167, 117.6750, 113.1754, 111.5341, 110.3917, 109.2194, 107.6181, 107.5932, 106.5306, 105.8123, 102.6345, 101.9012, 101.3924, 100.4545, 98.2745, 97.6510, 92.3980, 91.2856, 90.8965, 89.9786, 89.9387, 88.8362, 88.6766, 85.1896, 85.1746, 80.4554, 79.1634, 75.6814, 71.8701, 64.9660, 64.2726, 63.7537, 63.3896, 63.2449, 62.9606, 60.5461, 49.7110, 39.3148, 0.0000]

# costume
if 0:
    ascii_list = " -:+iJjIoOW"
    lightness = [255.0000, 218.8208, 201.0314, 175.7746, 148.3615, 141.4577, 139.3198, 128.7589, 120.3910, 81.2163, 0.0000]

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

def find_light_index(value, lightness_list, i, j):
    if value in lightness_list: return lightness_list.index(value)
    
    reversed_lightness = list(reversed(lightness_list))
    index = bisect.bisect_left(reversed_lightness, value)
    lower = reversed_lightness[index - 1]
    upper = reversed_lightness[index]
    
    prob = (upper - value) / (upper - lower)
    LEN = len(lightness_list) - 1
    return LEN - (index - 1) if bayer[i % 4][j % 4] < prob else LEN - index

def gray_to_ascii(value, ascii_list, inv, i, j):
    # 將 0~255 映射到 0~(num_chars-1) 的浮點數
    if (inv): value = 255 - value
    return ascii_list[find_light_index(value, lightness, i, j)]

# 調整尺寸
# new_width = 100 if vscode else 320 # horizontal vscode = 164 else 100 (verti), text editor 150
FONT_BBOX_RATIO = 0.455 if VSCODE else 0.44
resized = block_average_downsample(image, char_length)

# 轉換為 ASCII 字串
ascii_lines = []
for i, row in enumerate(resized):
    line = ''.join([gray_to_ascii(p, ascii_list, VSCODE, i, j) for j, p in enumerate(row)])
    ascii_lines.append(line)

ascii_img = '\n'.join(ascii_lines)

# 或寫入文字檔
with open('ascii_art.txt', 'w') as f:
    f.write(ascii_img)

# print("ascii art generated successfully.")