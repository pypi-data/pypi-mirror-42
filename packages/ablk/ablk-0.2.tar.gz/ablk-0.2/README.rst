====
ablk
====
Terminal image viewer.
----------------------
Matthew Oertle <moertle@gmail.com>

ablk is a image viewer that uses the UTF-8 block character and 24-bit ANSI escape sequences to render an image in the terminal window. Useful over SSH into a remote machine to get an idea of what an image file looks like.

usage: ablk [-h] [--delay DELAY] [--no-name] images [images ...]

positional arguments:
  images                Image files

optional arguments:
  -h, --help            show this help message and exit
  --delay DELAY, -d DELAY
                        Delay between each image
  --no-name, -n         Show filename of image
