FROM python:3.6-slim

# A note on the order of commands in this file:
# Docker uses caching extensively.
# By first installing requirements.txt and only then copying the actually application, we can get Docker to cache the Image that is created by installing the requirements.txt.
# This makes it much quicker to recompile Docker Images when you change your code but don't change requirements.txt
COPY requirements.txt /
RUN pip install -r /requirements.txt

COPY . /app
WORKDIR /app

CMD ["python", "app.py"]
