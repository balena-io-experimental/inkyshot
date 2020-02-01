import os
from inky import InkyPHAT

inky_display = InkyPHAT("black")
inky_display.set_border(inky_display.WHITE)

from PIL import Image, ImageFont, ImageDraw

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

from font_fredoka_one import FredokaOne

from font_hanken_grotesk import HankenGrotesk

font = ImageFont.truetype(HankenGrotesk, 16)

message = os.environ['INKY_MESSAGE']
w, h = font.getsize(message)
x = (inky_display.WIDTH / 2) - (w / 2)
y = (inky_display.HEIGHT / 2) - (h / 2)

draw.text((x, y), message, inky_display.BLACK, font)
inky_display.set_image(img)
inky_display.show()