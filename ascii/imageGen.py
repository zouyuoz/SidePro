import sys
from PIL import Image
import bisect
import numpy as np

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
BAYER_8X8 = generate_bayer_matrix(8)/64.

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
image = Image.open("C:/Users/zyqio/source/repos/SidePro/pics/" + file_name).convert("L")

# Fira Code
ascii_list = " `'.-:~!=;+<>\\/|?7clv)(Lti*rTzjxJ{1}fY4s[]FunCI32yoVae5ZkhXESP9U6KA&qpdbmHwG#OD8R%0BQN$@MW"
lightness = [255.0000, 234.2278, 223.3786, 221.7909, 215.3520, 198.9900, 198.9018, 182.0105, 177.1152, 173.4988, 167.1480, 161.7676, 161.3265, 155.9460, 154.9758, 152.1532, 150.3891, 143.5974, 143.0240, 141.0394, 141.0394, 140.5543, 140.3338, 139.1871, 136.9820, 136.7615, 135.4384, 132.1308, 130.5431, 129.4846, 129.3523, 128.2938, 127.5000, 126.9267, 126.8385, 126.7944, 125.3390, 124.2805, 123.1339, 123.1339, 120.4877, 120.4877, 118.5913, 116.6949, 116.5185, 114.7985, 114.0488, 112.2406, 110.9175, 110.6088, 105.7134, 102.9791, 102.7586, 102.0088, 100.9504, 97.9955, 92.3504, 91.8212, 90.8068, 88.6899, 85.2499, 84.1033, 80.0899, 77.6202, 76.8264, 76.1207, 75.4151, 73.0777, 72.1515, 71.5341, 70.2551, 69.1084, 66.9033, 66.6387, 66.5064, 66.1977, 64.6541, 62.5813, 54.8193, 53.7608, 50.3649, 40.9270, 40.0891, 37.5752, 36.3404, 33.9147, 26.7260, 4.4543, 3.2195, 0.0000]

# consolas
if not VSCODE:
    ascii_list = " `.-':~;!=><+*/\\?rcL()|T7JzivC{}1sFY][lItfZ3x2j5eonuSyEaVPw69U4KGXhkOAH%b#pqd8DRWmM0$BQN&@"
    lightness = [255.0000, 229.2076, 227.9919, 227.0719, 221.9463, 205.5508, 196.2853, 178.5756, 178.1813, 177.7213, 176.4727, 176.1442, 170.7557, 164.6444, 158.9273, 158.8945, 157.0216, 153.7688, 151.9617, 151.1403, 148.5446, 148.3475, 143.6819, 142.7619, 139.9691, 139.8048, 138.5891, 136.2891, 134.9092, 133.2335, 132.7078, 132.6421, 130.8349, 130.5721, 130.2764, 129.6521, 126.8593, 126.5964, 124.9536, 124.0993, 123.7708, 122.3908, 121.4051, 120.6823, 120.5180, 119.3351, 117.3309, 116.4766, 114.8338, 112.5667, 110.9896, 110.6939, 109.5110, 106.0939, 104.6482, 101.1983, 99.3255, 99.0955, 98.7669, 97.1241, 96.5655, 95.3827, 94.6927, 90.8485, 90.0271, 89.5999, 88.5157, 87.5628, 87.0371, 81.4186, 80.4658, 79.3815, 79.1515, 77.9030, 77.3773, 77.3444, 76.9830, 75.6030, 73.8945, 73.1388, 71.9559, 71.2988, 69.6888, 66.2060, 63.8075, 58.4190, 51.8806, 50.7306, 39.4936, 0.0000]

# costume
if 0:
    ascii_list = " ijJIowO@W"
    lightness = [255.0000, 136.7615, 129.3523, 127.5000, 114.0488, 105.7134, 66.5064, 62.5813, 4.4543, 0.0000]

# print(len(ascii_list))
# print(len(lightness))

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
    return LEN - (index - 1) if BAYER_8X8[i % 8][j % 8] < prob else LEN - index

def gray_to_ascii(value, ascii_list, inv, i, j):
    # 將 0~255 映射到 0~(num_chars-1) 的浮點數
    if (inv): value = 255 - value
    # value = (value * 3) % 255
    return ascii_list[find_light_index(value, lightness, i, j)]

# 調整尺寸
# new_width = 100 if vscode else 320 # horizontal vscode = 164 else 100 (verti), text editor 150
FONT_BBOX_RATIO = 0.455 if VSCODE else 0.44
resized = block_average_downsample(image, char_length)

# for _ in resized[16]: print(_)

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