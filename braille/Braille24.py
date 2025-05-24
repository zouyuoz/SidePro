from PIL import Image
import numpy as np
import sys

# 你可以自訂 pattern 或使用實際點亮邏輯產生的值，但這裡我們將使用真實 Braille 點陣（2x4）
# Braille dots mapping: (x, y) → dot index (0~7)
braille_dots_map = {
    (0, 0): 0,  # dot 1
    (0, 1): 1,  # dot 2
    (0, 2): 2,  # dot 3
    (1, 0): 3,  # dot 4
    (1, 1): 4,  # dot 5
    (1, 2): 5,  # dot 6
    (0, 3): 6,  # dot 7
    (1, 3): 7   # dot 8
}

def get_pixels_from_block(pixels, x_block, y_block, image_width, block_w=2, block_h=4):
    """取出一個 2x4 block 的像素清單"""
    block = []
    for y in range(block_h):
        for x in range(block_w):
            px = x_block * block_w + x
            py = y_block * block_h + y
            index = py * image_width + px
            if index < len(pixels):
                block.append((x, y, pixels[index]))
            else:
                block.append((x, y, 255))  # 超出邊界填白
    return block

def bayer_block_to_braille(block_pixels, inv):
    bayer = np.array([
        [0, 8, 2, 10],
        [12, 4, 14, 6],
        [3, 11, 1, 9],
        [15, 7, 13, 5]
    ]) / 16.0
    """
    對整個 2x4 Braille block 做 Bayer Dithering
    輸出對應的 Braille 字元 (U+2800 ~ U+28FF)
    """
    value = 0
    for x, y, gray in block_pixels:
        norm_gray = gray / 255.0
        threshold = bayer[y % 4][x % 2]
        fill = norm_gray >= threshold if inv else norm_gray <= threshold
        if fill:
            dot = braille_dots_map[(x, y)]
            value |= (1 << dot)
    
    if value==0:
        # shift_num = random.randrange(0,8,1)
        return chr(0x2800 + 1)
    
    return chr(0x2800 + value)

def image_to_braille_bayer(image_path, vscode):
    img = Image.open(image_path).convert("L")

    # 調整尺寸
    width, height = img.size
    aspect_ratio = height / width
    new_width = 264 if vscode else 210 # horizontal vscode = 264 else 160 (verti)
    font_bbox_ration = 1.14 if vscode else 1.35
    new_height = int(aspect_ratio * new_width * font_bbox_ration)
    resized = img.resize((new_width, new_height))
    pixels = list(resized.getdata())
    image_width = resized.width

    output = ""
    height_blocks = resized.height // 4
    width_blocks = resized.width // 2

    for y_block in range(height_blocks):
        for x_block in range(width_blocks):
            block = get_pixels_from_block(pixels, x_block, y_block, image_width)
            char = bayer_block_to_braille(block, vscode)
            output += char
        output += "\n"
    return output

# 執行並輸出
file_name = "pics/" + sys.argv[1]
def str_to_bool(s):
    return s.lower() in ("true", "1", "yes", "y")
vscode = str_to_bool(sys.argv[2])
braille_string = image_to_braille_bayer(file_name, vscode)

with open('braille.txt', 'w', encoding='utf-8') as f:
    f.write(braille_string)
