import os
import textwrap
from inky import InkyPHAT

inky_display = InkyPHAT("black")
inky_display.set_border(inky_display.WHITE)

from PIL import Image, ImageFont, ImageDraw

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

from font_fredoka_one import FredokaOne

from font_hanken_grotesk import HankenGrotesk

from font_intuitive import Intuitive

from font_source_serif_pro import SourceSerifPro

from font_source_sans_pro import SourceSansPro

from font_caladea import Caladea

from font_roboto import Roboto

from font_amatic_sc import AmaticSC

font = ImageFont.truetype(locals()[os.environ["FONT"]], int(os.environ['FONT_SIZE']))

bounding_box = [0, 0, inky_display.WIDTH, inky_display.HEIGHT]
x1, y1, x2, y2 = bounding_box 

message = os.environ['INKY_MESSAGE']
# message = "Don't try too hard, just do what makes you happy!"

test_message = ""
message_width = 0

while message_width < inky_display.WIDTH:
    test_message += os.environ['TEST_CHARACTER']
    message_width, message_height = draw.textsize(test_message, font=font)

max_width = len(test_message)

wrapper = textwrap.TextWrapper(width=max_width) 
word_list = wrapper.wrap(text=message) 
caption_new = ''

current_h, pad = 0, 0

num_lines = len(word_list)
total_height = 0

# we are iterating over the line list first to get the total height of all the lines together
for ii in word_list:
    w, h = draw.textsize(ii, font=font)
    total_height += h

line_height = total_height/num_lines
y = (y2 - y1 - total_height)/2 + y1

for ii in word_list:
    w, h = draw.textsize(ii, font=font)
    x = (x2 - x1 - w)/2 + x1
    draw.text((x, (y + current_h)), ii, inky_display.BLACK, font, align="center")
    current_h += line_height + pad

inky_display.set_image(img)
inky_display.show()