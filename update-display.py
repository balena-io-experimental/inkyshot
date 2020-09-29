import os
import textwrap
import urllib.request
import urllib.error
import json
import math
import logging

from PIL import Image, ImageFont, ImageDraw
from font_fredoka_one import FredokaOne
from font_hanken_grotesk import HankenGrotesk
from font_intuitive import Intuitive
from font_source_serif_pro import SourceSerifPro
from font_source_sans_pro import SourceSansPro
from font_caladea import Caladea
from font_roboto import Roboto
from font_amatic_sc import AmaticSC

# Declare non pip fonts here ** Note: ttf files need to be in the /fonts dir of application repo
Grand9KPixel = "/usr/app/fonts/Grand9KPixel.ttf"

if "DEBUG" in os.environ:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

# Assume a default font if none set
font_selected = AmaticSC
if "FONT" in os.environ:
    font_selected = locals()[os.environ["FONT"]]

# Init the display. TODO: support other colours
logging.debug("Init and Clear")
if "WAVESHARE" in os.environ:
    logging.info("Display type: Waveshare")

    import lib.epd2in13_V2  
    display = lib.epd2in13_V2.EPD()
    display.init(display.FULL_UPDATE)
    display.Clear(0xFF)
    # These are the opposite of what InkyPhat uses.
    WIDTH = display.height # yes, Height
    HEIGHT = display.width # yes, width
    img = Image.new('1', (WIDTH, HEIGHT), 255)
    BLACK = "black"
else:
    logging.info("Display type: InkyPHAT")

    from inky import InkyPHAT
    display = InkyPHAT("black")
    display.set_border(display.WHITE)
    WIDTH = display.WIDTH
    HEIGHT = display.HEIGHT
    img = Image.new("P", (display.WIDTH, display.HEIGHT))
    BLACK = display.BLACK

logging.info("Display dimensions: W %s x H %s", WIDTH, HEIGHT)

draw = ImageDraw.Draw(img)

font_size = 37
if "FONT_SIZE" in os.environ:
    font_size = int(os.environ["FONT_SIZE"])

# Use a dashboard defined message if we have one, otherwise load a nice quote
if "INKY_MESSAGE" in os.environ:
   message = os.environ['INKY_MESSAGE']

   if message == "":
       # If the message var was set but blank, use the device name
       message = os.environ['DEVICE_NAME']
else:
    req = urllib.request.Request("https://quotes.rest/qod?language=en", headers={"Accept" : "application/json"})
    try:
        res = urllib.request.urlopen(req, timeout=5).read()
        data = json.loads(res.decode())
        message = data['contents']['quotes'][0]['quote']
    except (urllib.error.HTTPError, urllib.error.URLError) as err:
        font_size = 25
        message = "Sorry folks, today's quote has gone walkies :("

logging.info("Message: %s", message)

# Work out what size font is required to fit this message on the display
message_does_not_fit = True

test_character = "a"
if "TEST_CHARACTER" in os.environ:
    test_character = os.environ['TEST_CHARACTER']

while message_does_not_fit == True:
    test_message = ""
    message_width = 0
    font_size -= 1

    # Start with the chosen font and size
    if font_size > 17:
       font = ImageFont.truetype(font_selected, font_size)
    else:
       font_size = 8
       font = ImageFont.truetype("/usr/app/fonts/Grand9KPixel.ttf", font_size)

    # We're using the test character here to work out how many characters
    # can fit on the display when using the chosen font
    while message_width < WIDTH: 
        test_message += test_character
        message_width, message_height = draw.textsize(test_message, font=font)

    max_width = len(test_message)
    max_lines = math.floor(HEIGHT/message_height)

    # We wrap the message to the width we worked out earlier
    wrapper = textwrap.TextWrapper(width=max_width) 
    word_list = wrapper.wrap(text=message)
    
    if len(word_list) <= max_lines:
        message_does_not_fit = False

    if font_size < 9:
        message_does_not_fit = False

logging.info("Font size: %s", font_size)
offset_x, offset_y = font.getoffset(message)

# Rejoin the wrapped lines with newline chars
separator = '\n'
output_text = separator.join(word_list)

w, h = draw.multiline_textsize(output_text, font=font, spacing=0)

x = (WIDTH - w)/2
y = (HEIGHT - h - offset_y)/2
draw.multiline_text((x, y), output_text, BLACK, font, align="center", spacing=0)

# Rotate and display the image
if "ROTATE" in os.environ:
    img = img.rotate(180)

if "WAVESHARE" in os.environ:
    # epd does not have a set_image method.
    display.display(display.getbuffer(img))
else:
    display.set_image(img)
    display.show()
