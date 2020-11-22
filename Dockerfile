
FROM buildkite/puppeteer

ENV DEBIAN_FRONTEND="noninteractive" \
    INITRD="No" \
    PACKAGES="git curl ffmpeg sox libsox-fmt-mp3 python3 python3-pip python3-virtualenv python3-dev python3-setuptools"

WORKDIR /usr/src/app

RUN apt-get update \
    && apt-get install -yq --no-install-recommends $PACKAGES \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && ln -s /usr/bin/python3 /usr/bin/python

COPY requirements.txt /usr/src/app/
RUN pip3 install --no-cache-dir -r requirements.txt

COPY . /usr/src/app

CMD python main.py
