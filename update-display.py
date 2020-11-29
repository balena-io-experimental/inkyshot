import json
import logging
import math
from pathlib import Path
import os
from os import environ
import sys
import textwrap
import time
import urllib.request
import urllib.error

from font_amatic_sc import AmaticSC
from font_caladea import Caladea
from font_fredoka_one import FredokaOne
from font_hanken_grotesk import HankenGrotesk
from font_intuitive import Intuitive
from font_roboto import Roboto
from font_source_sans_pro import SourceSansPro
from font_source_serif_pro import SourceSerifPro
from PIL import Image, ImageFont, ImageDraw
import arrow
import geocoder

icon_map = {
    "clearsky": 1,
    "cloudy": 4,
    "fair": 2,
    "fog": 15,
    "heavyrain": 10,
    "heavyrainandthunder": 11,
    "heavyrainshowers": 41,
    "heavyrainshowersandthunder": 25,
    "heavysleet": 48,
    "heavysleetandthunder": 32,
    "heavysleetshowers": 43,
    "heavysleetshowersandthunder": 27,
    "heavysnow": 50,
    "heavysnowandthunder": 34,
    "heavysnowshowers": 45,
    "heavysnowshowersandthunder": 29,
    "lightrain": 46,
    "lightrainandthunder": 30,
    "lightrainshowers": 40,
    "lightrainshowersandthunder": 24,
    "lightsleet": 47,
    "lightsleetandthunder": 31,
    "lightsleetshowers": 42,
    "lightsnow": 49,
    "lightsnowandthunder": 33,
    "lightsnowshowers": 44,
    "lightssleetshowersandthunder": 26,
    "lightssnowshowersandthunder": 28,
    "partlycloudy": 3,
    "rain": 9,
    "rainandthunder": 22,
    "rainshowers": 5,
    "rainshowersandthunder": 6,
    "sleet": 12,
    "sleetandthunder": 23,
    "sleetshowers": 7,
    "sleetshowersandthunder": 20,
    "snow": 13,
    "snowandthunder": 14,
    "snowshowers": 8,
    "snowshowersandthunder": 21,
}

def create_mask(source):
    """Create a transparency mask to draw images in grayscale
    """
    logging.info("Creating a transparency mask for the image")
    mask_image = Image.new("1", source.size)
    w, h = source.size
    for x in range(w):
        for y in range(h):
            p = source.getpixel((x, y))
            if p in [BLACK, WHITE]:
                mask_image.putpixel((x, y), 255)
    return mask_image

# Declare non pip fonts here ** Note: ttf files need to be in the /fonts dir of application repo
Grand9KPixel = "/usr/app/fonts/Grand9KPixel.ttf"

def draw_weather(weather, img, scale):
    """Draw the weather info on screen"""
    logging.info("Prepare the weather data for drawing")
    # Draw today's date on left side below today's name
    today = arrow.utcnow().format(fmt="DD MMMM", locale=LOCALE)
    date_font = ImageFont.truetype(WEATHER_FONT, 18)
    draw.text((3, 3), today, BLACK, font=date_font)
    # Draw current temperature to right of today
    temp_font = ImageFont.truetype(WEATHER_FONT, 24)
    draw.text((3, 30), f"{temp_to_str(weather['temperature'], scale)}°", BLACK, font=temp_font)
    # Draw today's high and low temps on left side below date
    small_font = ImageFont.truetype(WEATHER_FONT, 14)
    draw.text(
        (3, 72),
        f"{temp_to_str(weather['min_temp'], scale)}° - {temp_to_str(weather['max_temp'], scale)}°",
        BLACK,
        font=small_font,
    )
    # Draw today's max humidity on left side below temperatures
    draw.text((3, 87), f"{weather['max_humidity']}%", BLACK, font=small_font)
    # Load weather icon
    icon_name = weather['symbol'].split('_')[0]
    time_of_day = ''
    # Couple of symbols have different icons for day and night. Check if this symbol is one of them.
    if len(weather['symbol'].split('_')) > 1:
        symbol_cycle = weather['symbol'].split('_')[1]
        if symbol_cycle == 'day':
            time_of_day = 'd'
        elif symbol_cycle == 'night':
            time_of_day = 'n'
    icon_filename = f"{icon_map[icon_name]:02}{time_of_day}.png"
    filepath = Path(__file__).parent / 'weather-icons' / icon_filename
    icon_image = Image.open(filepath)
    icon_mask = create_mask(icon_image)
    # Draw the weather icon
    img.paste(icon_image, (120, 3), icon_mask)
    return img

def get_location():
    """Return coordinate and location info based on IP address"""
    url = "https://ipinfo.io"
    req = urllib.request.Request(url, headers={"Accept" : "application/json"})
    try:
        res = urllib.request.urlopen(req, timeout=5)
        logging.info("Retrieved the location data using device's IP address")
        if(res.status == 200):
            return json.loads(res.read().decode())
    except (urllib.error.HTTPError, urllib.error.URLError) as err:
        logging.error(err)
    logging.error("Failed to retrieve the location data")
    return {}

def get_weather(lat, long):
    """Return weather report for the next 24 hours"""
    url = f"https://api.met.no/weatherapi/locationforecast/2.0/compact?lat={lat}&lon={long}"
    req = urllib.request.Request(url, headers={"Accept" : "application/json"})
    logging.info("Retrieving weather forecast")
    weather = {}
    try:
        res = urllib.request.urlopen(req, timeout=5)
        if(res.status == 200):
            data = json.loads(res.read().decode())
            timeseries = data['properties']['timeseries']
            now = arrow.utcnow()
            tomorrow = now.shift(hours=+24)
            weather_24hours = []
            for t in timeseries:
                tm = arrow.get(t['time'])
                if tm < tomorrow:
                    temp = t['data']['instant']['details']['air_temperature']
                    humid = t['data']['instant']['details']['relative_humidity']
                    symbol = t['data']['next_1_hours']['summary']['symbol_code']
                    weather_24hours.append({
                        'time': tm,
                        'temperature': temp,
                        'humidity': humid,
                        'symbol': symbol,
                    })
            weather_24hours = sorted(weather_24hours, key=lambda x: x['time'])
            weather = [x for x in weather_24hours if x['time'] <= now.shift(hours=+1)][-1]
            temperatures = [x['temperature'] for x in weather_24hours if x['time'] <= now.shift(days=+1)]
            weather['max_temp'] = max(temperatures)
            weather['min_temp'] = min(temperatures)
            weather['max_humidity'] = max([x['humidity'] for x in weather_24hours if x['time'] <= now.shift(days=+1)])
    except (urllib.error.HTTPError, urllib.error.URLError) as err:
        logging.error(err)
    return weather

def temp_to_str(temp, scale):
    """Prepare the temperature to draw based on the defined scale: Celcius or Fahrenheit"""
    if scale == 'F':
        temp = temp * 9/5 + 32
    return f"{temp:.1f}"

# Read the preset environment variables and overwrite the default ones
if "DEBUG" in os.environ:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)

# Check if daily quote is disabled
DISPLAY_QUOTE = True
if "DISPLAY_QUOTE" in os.environ and not os.environ["DISPLAY_QUOTE"]:
    DISPLAY_QUOTE = False

# Assume a default font if none set
FONT_SELECTED = AmaticSC
if "FONT" in os.environ:
    FONT_SELECTED = locals()[os.environ["FONT"]]

FONT_SIZE = 24
if "FONT_SIZE" in os.environ:
    FONT_SIZE = int(os.environ["FONT_SIZE"])

# Check for a quote of the day category, otherwise use inspire
CATEGORY = "inspire"
if "QOD_CATEGORY" in os.environ:
    CATEGORY = os.environ['QOD_CATEGORY']

# Check for a quote of the day language. ** Note: Only English is supported currently. **
LANGUAGE = "en"
if "QOD_LANGUAGE" in os.environ:
    LANGUAGE = os.environ['QOD_LANGUAGE']

FONT = ImageFont.truetype(FONT_SELECTED, FONT_SIZE)

WEATHER_FONT = FredokaOne
if "WEATHER_FONT" in os.environ:
    WEATHER_FONT = locals()[os.environ["WEATHER_FONT"]]

[LAT, LONG] = [float(x) for x in os.environ["LATLONG"].split(",")] if "LATLONG" in os.environ else [None, None]

# Temperature scale
SCALE = 'F' if "SCALE" in os.environ and os.environ["SCALE"] == 'F' else 'C'

# Locale formatting of date
LOCALE = os.environ["LOCALE"] if "LOCALE" in os.environ else 'en'

# Alternate displaying quote and weather
NEXT_DISPLAY = os.environ["NEXT_DISPLAY"] if "NEXT_DISPLAY" in os.environ else 'quote'

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
    BLACK = "black"
    WHITE = "white"
    img = Image.new('1', (WIDTH, HEIGHT), 255)
else:
    import inky
    display = inky.auto()
    logging.info("Display type: " + type(display).__name__)
    display.set_border(display.WHITE)
    WIDTH = display.WIDTH
    HEIGHT = display.HEIGHT
    BLACK = display.BLACK
    WHITE = display.WHITE
    img = Image.new("P", (WIDTH, HEIGHT))

draw = ImageDraw.Draw(img)

logging.info("Display dimensions: W %s x H %s", WIDTH, HEIGHT)

display_weather = False

if NEXT_DISPLAY == 'weather':
    weather_location = None
    if "WEATHER_LOCATION" in os.environ:
        weather_location = os.environ["WEATHER_LOCATION"]
    # Get the latitute and longitude of the address typed in the env variable if latitude and longitude are not set
    if weather_location and (not LAT or not LONG):
        logging.info(f"Location is set to {weather_location}")
        try:
            geo = geocoder.arcgis(weather_location)
            [LAT, LONG] = geo.latlng
        except Exception as e:
            print(f"Unexpected error: {e.message}")

    # If no address or latitute / longitude are found, retrieve location via IP address lookup
    if not LAT or not LONG:
        location = get_location()
        [LAT, LONG] = [float(x) for x in location['loc'].split(',')]
    weather = get_weather(LAT, LONG)
    # Set latitude and longituted as environment variables for consecutive calls
    os.environ['LATLONG'] = f"{LAT},{LONG}"
    # If weather is empty dictionary fall back to drawing quote
    if len(weather) > 0:
        img = draw_weather(weather, img, SCALE)
        display_weather = True

message = None
# Use a dashboard defined message if we have one, otherwise load a nice quote
if "INKY_MESSAGE" in os.environ and not display_weather and DISPLAY_QUOTE:
   message = os.environ['INKY_MESSAGE']

   if message == "":
       # If the message var was set but blank, use the device name
       message = os.environ['DEVICE_NAME']
elif not display_weather and DISPLAY_QUOTE:
    req = urllib.request.Request(f"https://quotes.rest/qod?category={CATEGORY}&language={LANGUAGE}", headers={"Accept" : "application/json"})
    try:
        res = urllib.request.urlopen(req, timeout=5).read()
        data = json.loads(res.decode())
        message = data['contents']['quotes'][0]['quote']
    except (urllib.error.HTTPError, urllib.error.URLError) as err:
        FONT_SIZE = 25
        message = "Sorry folks, today's quote has gone walkies :("

if message:
    logging.info("Message: %s", message)
    # Work out what size font is required to fit this message on the display
    message_does_not_fit = True

    test_character = "a"
    if "TEST_CHARACTER" in os.environ:
        test_character = os.environ['TEST_CHARACTER']

    while message_does_not_fit == True:
        test_message = ""
        message_width = 0
        FONT_SIZE -= 1

        if FONT_SIZE <= 17:
            FONT_SIZE = 8
            FONT = ImageFont.truetype("/usr/app/fonts/Grand9KPixel.ttf", FONT_SIZE)

        # We're using the test character here to work out how many characters
        # can fit on the display when using the chosen font
        while message_width < WIDTH:
            test_message += test_character
            message_width, message_height = draw.textsize(test_message, font=FONT)

        max_width = len(test_message)
        max_lines = math.floor(HEIGHT/message_height)

        # We wrap the message to the width we worked out earlier
        wrapper = textwrap.TextWrapper(width=max_width)
        word_list = wrapper.wrap(text=message)

        if len(word_list) <= max_lines:
            message_does_not_fit = False

        if FONT_SIZE < 9:
            message_does_not_fit = False

    logging.info("Font size: %s", FONT_SIZE)
    offset_x, offset_y = FONT.getoffset(message)

    # Rejoin the wrapped lines with newline chars
    separator = '\n'
    output_text = separator.join(word_list)

    w, h = draw.multiline_textsize(output_text, font=FONT, spacing=0)

    x = (WIDTH - w)/2
    y = (HEIGHT - h - offset_y)/2
    draw.multiline_text((x, y), output_text, BLACK, FONT, align="center", spacing=0)

# Rotate and display the image
if "ROTATE" in os.environ:
    img = img.rotate(180)

if "WAVESHARE" in os.environ:
    # epd does not have a set_image method.
    display.display(display.getbuffer(img))
else:
    display.set_image(img)
    display.show()

logging.info("Done drawing")
# Alternate to other display

#    default --> quote only.
#    ALTERNATE_FREQUENCY set --> switch between quote/weather
#    DISPLAY_QUOTE = 0 --> showing only weather

if "DISPLAY_QUOTE" in os.environ and os.environ["DISPLAY_QUOTE"]=='0':
        os.environ["NEXT_DISPLAY"] = 'weather'
else:
        if(NEXT_DISPLAY == 'quote' and "ALTERNATE_FREQUENCY" in os.environ): 
            os.environ["NEXT_DISPLAY"] = 'weather'
        else :
            os.environ["NEXT_DISPLAY"] = 'quote'

sys.exit(0)
