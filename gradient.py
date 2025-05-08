from PIL import Image, ImageDraw, ImageFont

consolas = "C:/Windows/Fonts/consola.ttf"
def draw_char(char, font_path=consolas, font_size=16, image_size=(10, 16)):
    img = Image.new("L", image_size, color=255)
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype(font_path, font_size)

    bbox = draw.textbbox((0, 0), char, font=font)
    w, h = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pos = ((image_size[0] - w) // 2 - bbox[0], (image_size[1] - h) // 2 - bbox[1])

    # 畫字
    draw.text(pos, char, fill=0, font=font)

    # 畫 bbox 框線（加回 pos 的偏移量）
    draw.rectangle(
        [pos[0] + bbox[0], pos[1] + bbox[1], pos[0] + bbox[2], pos[1] + bbox[3]],
        outline=128  # 灰色框
    )

    # 顯示圖片（限指定字元）
    check_list = ["|", "`", ",", "_", "L", "^"]
    if char in check_list:
        img.show()

# 範例
for i in range(32, 127):
    draw_char(chr(i))