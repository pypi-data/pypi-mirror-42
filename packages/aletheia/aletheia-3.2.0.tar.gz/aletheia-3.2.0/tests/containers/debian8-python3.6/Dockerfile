FROM python:3.6-jessie

# https://superuser.com/questions/1068949
RUN echo "deb http://ftp.debian.org/debian jessie-backports main" >> /etc/apt/sources.list
RUN apt-get update; apt-get install -y ffmpeg libimage-exiftool-perl; apt-get clean
RUN pip install --upgrade pip \
  && pip install pytest pytest-sugar pytest-cov pytest-xdist \
  && pip install cryptography file-magic requests termcolor dnspython \
  && rm -rf /root/.cache
