from PIL import Image, ImageDraw, ImageFont
import numpy as np

fira = "C:/Users/zyqio/AppData/Local/Microsoft/Windows/Fonts/FiraCode-VariableFont_wght.ttf"
consolas = "C:/Windows/Fonts/consola.ttf"

abandom = ["g", "^", "\"", "w", "y", "_", ","]

def get_char_grayscale(char, font_path=fira, font_size=32, image_size=(20, 32)):
    if char in abandom: return
    # 建立白底畫布
    img = Image.new("L", image_size, color=255)  # L 模式 = 灰階
    draw = ImageDraw.Draw(img)
    
    # 載入 Consolas 字體
    font = ImageFont.truetype(font_path, font_size)
    
    # 計算位置置中
    bbox = draw.textbbox((0, 0), char, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pos = ((image_size[0] - w) // 2 - bbox[0], (image_size[1] - h) // 2 - bbox[1])
    
    # 畫字
    draw.text(pos, char, fill=0, font=font)
    
    check_list = ["\"", ";", "=", ","] # "|", "_", "L", "g", "`", "^", "U", "K"
    # if char in check_list: img.show()

    # 計算平均色階
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