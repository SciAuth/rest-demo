FROM hub.opensciencegrid.org/opensciencegrid/software-base:3.6-el8-release


## Set the Python version.


ARG PY_PKG=python39
ARG PY_EXE=python3.9


## Locale and Python settings required by Flask.


ENV LANG="en_US.utf8"
ENV LC_ALL="en_US.utf8"
ENV PYTHONUNBUFFERED=1


## Install core dependencies and configuration.


RUN yum module enable -y ${PY_PKG} \
    && yum update -y \
    && yum install -y httpd mod_ssl ${PY_PKG}-pip ${PY_PKG}-mod_wsgi \
    && yum clean all \
    && rm -rf /etc/httpd/conf.d/* /var/cache/yum/ \
    #
    && ${PY_EXE} -m pip install --no-cache-dir -U pip setuptools wheel

COPY etc /etc/


## Install the Flask and WSGI applications.

# Cashman
COPY cashman /srv/cashman
COPY utils /srv/utils

# Dependencies
COPY requirements.txt Pipfile Pipfile.lock /srv/

# Main WSGI app
COPY wsgi.py /srv/

WORKDIR /srv
RUN  ${PY_EXE} -m pip install --no-cache-dir -r requirements.txt