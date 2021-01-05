FROM mcr.microsoft.com/playwright:bionic
RUN apt-get update && apt-get install -y --no-install-recommends curl

# Confirm node and npm exist
RUN node -v
RUN npm -v

# Install python3.8
RUN : \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        software-properties-common \
    && add-apt-repository -y ppa:deadsnakes \
    && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
        python3.8-venv \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && :

RUN python3.8 -m venv /venv
ENV PATH=/venv/bin:$PATH

RUN /venv/bin/python3.8 -m pip install --upgrade pip
COPY ./requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# playwright is installed under pwuser
USER pwuser
COPY ./checker /home/pwuser/checker

WORKDIR /home/pwuser
ENTRYPOINT python -m checker.app
