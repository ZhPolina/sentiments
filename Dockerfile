# Use an official Python runtime as a parent image
FROM python:3.8-slim-buster

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN mkdir -p /usr/local/lib/python3.8/site-packages/dostoevsky/data/models/
COPY models/fasttext-social-network-model.bin /usr/local/lib/python3.8/site-packages/dostoevsky/data/models/

RUN apt-get update && apt-get install -y --no-install-recommends python3-setuptools python3-wheel python3-dev gcc build-essential
RUN pip install fasttext
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    python-dev
RUN pip install flask-mysqldb
RUN pip install python-dotenv
RUN pip install mysqlclient


# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define environment variables
ENV FLASK_APP=main.py
ENV FLASK_ENV=development
ENV MYSQL_DATABASE=flask
ENV MYSQL_PASSWORD=9156
ENV MYSQL_HOST=mysql
ENV MYSQL_CHARSET=utf8
ENV MYSQL_COLLATION=utf8_general_ci

# Run the Flask application when the container starts
CMD ["flask", "run", "--host", "0.0.0.0"]