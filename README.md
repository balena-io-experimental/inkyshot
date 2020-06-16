# Inkyshot - a shot of inspiration to start the day

![](https://raw.githubusercontent.com/balenalabs-incubator/inkyshot/master/assets/header-photo.jpg)

**Get a daily random inspirational quote delivered direct to your desk with Inkyshot. Build multiple Inkyshots and share the inspiration with your friends, family and loved ones ❤️**

## Hardware required

![](https://raw.githubusercontent.com/balenalabs-incubator/inkyshot/master/assets/hardware-photo.jpg)

* Raspberry Pi (tested with Zero and 3B so far)
* [Pimoroni InkyPHAT display](https://shop.pimoroni.com/products/inky-phat?variant=12549254938707)
* 8GB SD Card (Sandisk Extreme Pro recommended)
* Power supply
* **Optional:** 3D printed case with [micro USB sockets](https://www.aliexpress.com/item/4000484202812.html)
* **Optional:** [Waveshare 2.13" e-paper display V2](https://www.waveshare.com/wiki/2.13inch_e-Paper_HAT) (**Note:** the case designs will need modification to fit this display. Set the `WAVESHARE` environment variable to `1` to enable support)

## Setup & Installation

Running this project is as simple as deploying it to a balenaCloud application. You can do it in just one click by using the button below:

[![](https://balena.io/deploy.png)](https://dashboard.balena-cloud.com/deploy)

You can also deploy in the traditional manner using the balena CLI and `balena push` command. For more information [check out the docs](https://www.balena.io/docs/learn/deploy/deployment/).

## Customization

Your fleet of Inkyshots can all be managed centrally via balenaCloud. Try any of the environment variables below to add some customization.

### Update time

Inkyshot wants to deliver a shot of inspiration to start your day, and by default will do this at 9AM/0900 hours UTC. You can change the hour that the update will happen with the `UPDATE_HOUR` variable; set it anywhere from `0` to `23`.

### Timezone

In order for the update time to work correctly, you'll of course have to tell Inkyshot what timezone you'd like to use. Set the `TZ` environment variable to any [IANA timezone](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones), e.g. `Europe/London`, `America/Los_Angeles`, `Asia/Taipei` etc.

### Message override

Is there a special occasion in your family? Override the daily quote with a shot of celebration by setting the `INKY_MESSAGE` environment variable. Try `Happy birthday Sister!`, `Congratulations on the new job, mate!`, or `Happy mother's day!`.

### Font

There are a few fonts built in that you can try. The default is `AmaticSC`, but you can use the `FONT` variable and set it to any of: `FredokaOne`, `HankenGrotesk`, `Intuitive`, `SourceSerifPro`, `SourceSansPro`, `Caladea` and `Roboto`. You're welcome to PR more options into the project!

### Font size

Inkyshot will automatically choose the largest font size for your message that still fits on the display. Too big? Override it with the `FONT_SIZE` variable and Inkyshot will use this as a maximum and continue to resize downwards if your message doesn't fit.

### Test character

When figuring out what size font to use, Inkyshot (invisibly) fills the screen with the `a` character to see how many will fit. You can override this by setting the `TEST_CHARACTER` environment variable with any wider (`w`) or slimmer (`i`) characters of your choosing to adjust this behavior.

### Rotation

If Inkyshot is living in a different house where things aren't necessarily always the same way up, use the `ROTATE` environment variable to rotate the output by 180 degrees.

## Case

STL files are included within the assets folder of the project for you to 3D print your own case.

![](https://raw.githubusercontent.com/balenalabs-incubator/inkyshot/master/assets/inky-print.png)

The case has two positions for a captive M3 nut, and can be fastened together with two countersunk 8mm M3 machine screws.

A position is open in the rear of the case for the use of a [micro USB PCB socket](https://www.aliexpress.com/item/4000484202812.html), allowing for direct connection of power to the back of a Raspberry Pi Zero.

![](https://raw.githubusercontent.com/balenalabs-incubator/inkyshot/master/assets/inky-rear.png)


## Credits

Quotes are delivered from the 
<span style="z-index:50;font-size:0.9em; font-weight: bold;">
      <img src="https://theysaidso.com/branding/theysaidso.png" height="20" width="20" alt="theysaidso.com"/>
      <a href="https://theysaidso.com" title="Powered by quotes from theysaidso.com" style="color: #ccc; margin-left: 4px; vertical-align: middle;">
        They Said So®
      </a>
</span> REST API.
