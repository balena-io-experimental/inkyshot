FROM balenalib/raspberry-pi-debian-python:3.7-buster-build
RUN pip install inky
RUN install_packages python3-pil

RUN pip install font_fredoka_one
COPY displaytext.py .

CMD while : ; do python displaytext.py; sleep ${INTERVAL=10}; done