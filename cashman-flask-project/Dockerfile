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


# Docker
COPY docker-compose.yaml Dockerfile /srv/

# Cashman
COPY cashman utils /srv/cashman/

# Dependencies
COPY requirements.txt Pipfile Pipfile.lock /srv/
RUN  ${PY_EXE} -m pip install --no-cache-dir -r /srv/requirements.txt

# Main WSGI app
COPY wsgi.py /srv/
