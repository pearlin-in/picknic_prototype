from PIL import Image, ImageDraw, ImageFont

def create_stamp_image(colors, size=(200, 150)):
    stamp = Image.new("RGB", size, colors["background"])
    draw = ImageDraw.Draw(stamp)
    border_color = colors["stamp_border"]
    draw.rectangle([5, 5, size[0]-5, size[1]-5], outline=border_color, width=2)
    draw.text((size[0]//2, size[1]-12), "PICKNIC", fill=border_color, anchor="ms", font=ImageFont.load_default())
    return stamp