import os
import textwrap
import urllib.request
import json

from inky import InkyPHAT
from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
from font_hanken_grotesk import HankenGrotesk
from font_intuitive import Intuitive
from font_source_serif_pro import SourceSerifPro
from font_source_sans_pro import SourceSansPro
from font_caladea import Caladea
from font_roboto import Roboto
from font_amatic_sc import AmaticSC

# Init the display. TODO: support other colours
inky_display = InkyPHAT("black")
inky_display.set_border(inky_display.WHITE)

img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
draw = ImageDraw.Draw(img)

font = ImageFont.truetype(locals()[os.environ["FONT"]], int(os.environ['FONT_SIZE']))

# We're using the test character here to work out how many characters
# can fit on the display when using the chosen font
test_message = ""
message_width = 0
test_character = "a"

if "TEST_CHARACTER" in os.environ:
    test_character = os.environ['TEST_CHARACTER']

while message_width < inky_display.WIDTH:
    test_message += test_character
    message_width, message_height = draw.textsize(test_message, font=font)

max_width = len(test_message)

# Use a dashboard defined message if we have one, otherwise load a nice quote
if "INKY_MESSAGE" in os.environ:
   message = os.environ['INKY_MESSAGE'] 
else:
    req = urllib.request.Request("https://quotes.rest/qod?language=en", headers={"Accept" : "application/json"})
    res = urllib.request.urlopen(req).read()
    data = json.loads(res.decode())
    message = data['contents']['quotes'][0]['quote']

# We wrap the message to the width we worked out earlier
wrapper = textwrap.TextWrapper(width=max_width) 
word_list = wrapper.wrap(text=message) 

num_lines = len(word_list)
message_height = 0

# Iterate over the line list first to get the total height of all the lines together
for ii in word_list:
    w, h = draw.textsize(ii, font=font)
    message_height += h


# Take the total line height and subtract from the entire display
# this allows us to center vertically
line_height = message_height/num_lines
y = (inky_display.HEIGHT - message_height)/2


# Draw the wrapped lines
current_h = 0

for ii in word_list:
    w, h = draw.textsize(ii, font=font)

    # Figure out the offset needed to center horizontally
    x = (inky_display.WIDTH - w)/2
    draw.text((x, (y + current_h)), ii, inky_display.BLACK, font, align="center")
    current_h += line_height


# Rotate and display the image
if "ROTATE" in os.environ:
    img = img.rotate(180)

inky_display.set_image(img)
inky_display.show()