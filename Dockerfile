# Use a base image with Python 3.7
FROM python:3.7-slim

# Install Chrome dependencies and wget
RUN apt-get update && apt-get install -y wget gnupg \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable wget \
    && apt-get purge -y gnupg && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the Chrome binary path as an environment variable
ENV CHROME_BIN /usr/bin/google-chrome-stable

# Set the working directory in the container
WORKDIR /app

# Copy all necessary files for the application, including the utils folder
COPY app.py requirements.txt /app/
COPY utils /app/utils

# Install application dependencies
RUN pip install -r requirements.txt

# Expose the port your application will run on
EXPOSE 3000

# Define the command to run your application
CMD ["python", "app.py"]
