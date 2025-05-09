from PIL import Image, ImageDraw, ImageFont
import numpy as np

fira = "C:/Users/zyqio/AppData/Local/Microsoft/Windows/Fonts/FiraCode-Regular.ttf"
consolas = "C:/Windows/Fonts/consolab.ttf"

abandom = ["g", "^", "\"", "_", ","] # "w", "y", 

def get_char_grayscale(char, font_path=fira, font_size=16):
    if char in abandom: return
    # 計算行數
    lines = char.split("\n")
    num_lines = len(lines)
    
    line_spacing = font_size // 3
    
    # 動態調整畫布大小
    image_width = int(0.6 * font_size * max(len(line) for line in lines))  # 取最長行的長度
    image_height = int(0.87 * (font_size + line_spacing) * num_lines)  # 高度根據行數調整
    image_size = (image_width, image_height)
    
    # 建立白底畫布
    img = Image.new("L", image_size, color=255)  # L 模式 = 灰階
    draw = ImageDraw.Draw(img)
    
    # 載入 Consolas 字體
    font = ImageFont.truetype(font_path, font_size)
    
    # 計算位置置中
    bbox = draw.textbbox((0, 0), char, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pos = ((image_size[0] - w) // 2 - bbox[0], (image_size[1] - h) // 2 - bbox[1])
    
    # 畫每一行文字
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
        pos = ((image_size[0] - w) // 2 - bbox[0], i * (font_size + line_spacing))  # 每行垂直偏移
        draw.text(pos, line, fill=0, font=font)

    # img.show()
    
    img_array = np.array(img, dtype=np.uint8)
    mean_val = img_array.mean()

    # Normalize：黑=0，白=255 -> 白背景越多 = 越高值
    normalized = mean_val / 255.0
    return normalized
    
def analyze_string(string):
    result = {}
    for ch in string:
        gray_level = get_char_grayscale(ch)
        if gray_level is None: continue
        result[ch] = gray_level
    return result


ascii_printable = ''.join(chr(i) for i in range(32, 127))
# 測試
result = analyze_string(ascii_printable)

result = sorted(result.items(), key=lambda x: x[1], reverse=True)
min_val = result[len(result) - 1][1]
normalize_raio = 255 / (1 - min_val)

# for ch, val in result:
#     norVal = (val - min_val) * normalize_raio
#     print(ch, f"{norVal:.4f}")

# exit()

SELECT = " JIWOjiwo"
SELECT += "+-:"

# print(min_val)
print("ascii_list = \"", end="")
for ch, val in result:
    # if (ch not in SELECT): continue
    prefix = "\\" if ch == "\\" or ch == "\"" else "" 
    print(prefix, ch, sep="", end="")
    
print("\"\n    lightness = [", end="")

for i, (ch, val) in enumerate(result):
    # if (ch not in SELECT): continue
    norVal = (val - min_val) * normalize_raio
    end_str = ", " if i != len(result) - 1 else ""
    print(f"{norVal:.4f}", end=end_str)
print("]")
