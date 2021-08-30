FROM balenalib/raspberry-pi-debian-python:3.7-buster-run

WORKDIR /usr/app
COPY pip.conf /etc/

RUN install_packages \
  cron \
  libatlas3-base \
  libgfortran3 \
  libzstd1 \
  liblcms2-2 \
  libjbig0 \
  libopenjp2-7 \
  libwebpdemux2 \
  libtiff5 \
  libwebpmux3 \
  libwebp6 \
  libxcb1 \
  libfreetype6-dev \
  jq

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY start.sh .
COPY run-update.sh .
COPY lib lib
COPY fonts fonts
COPY weather-icons weather-icons

RUN chmod +x start.sh
RUN chmod +x run-update.sh

COPY update-display.py .

CMD ["/bin/bash","start.sh"]