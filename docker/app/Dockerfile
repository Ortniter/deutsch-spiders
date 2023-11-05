FROM arm64v8/python:3.8-slim-bullseye
WORKDIR /app
RUN apt-get update && \
apt-get install -y --no-install-recommends libjpeg-dev \
                                               libtiff-dev \
                                               liblcms2-dev \
                                               libpq-dev \
                                               libwebp-dev \
                                               libxml2-dev \
                                               libxslt1-dev \
                                               gettext \
                                               git \
                                               gcc \
                                               libffi-dev \
                                               tcl-dev \
                                               g++ \
                                               libmagic-dev \
                                               wkhtmltopdf \
                                               libcairo2 \
                                               libpango-1.0-0 \
                                               libpangocairo-1.0-0 \
                                               libgdk-pixbuf2.0-0 \
                                               libffi-dev \
                                               shared-mime-info
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt --src=/root/pip
COPY docker/app/wait-for.sh /usr/local/bin/wait-for
