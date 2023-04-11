# Use a base image with Python 3.7
FROM python:3.7-slim

# Install Chrome dependencies
RUN apt-get update && apt-get install -y wget gnupg \
    && wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update && apt-get install -y google-chrome-stable \
    && apt-get purge -y wget gnupg && apt-get autoremove -y && apt-get clean && rm -rf /var/lib/apt/lists/*

# Set the Chrome binary path as an environment variable
ENV CHROME_BIN /usr/bin/google-chrome-stable

# Set the working directory in the container
WORKDIR /app

# Copy only necessary files for the application
COPY app.py requirements.txt /app/

# Install application dependencies
RUN pip install -r requirements.txt

# Expose the port your application will run on
EXPOSE 3000

# Define the command to run your application
CMD ["python", "app.py"]
