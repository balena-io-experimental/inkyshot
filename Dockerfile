FROM balenalib/raspberry-pi-debian-python:3.7-buster-build
RUN pip install inky
RUN install_packages python3-pil

RUN pip install font_fredoka_one font_hanken_grotesk font_intuitive font_source_serif_pro font_source_sans_pro font_caladea font_roboto font_amatic_sc
COPY displaytext.py .

CMD while : ; do python displaytext.py; sleep ${INTERVAL=600}; done