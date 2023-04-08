# Use a base image with Python 3.7
FROM python:3.7

# Install Chrome dependencies
RUN apt-get update && apt-get install -y wget curl gnupg
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update && apt-get install -y google-chrome-stable

# Set the Chrome binary path as an environment variable
ENV CHROME_BIN /usr/bin/google-chrome-stable

# Set the working directory in the container
WORKDIR /app

# Copy your application code into the container
COPY . /app

# Install application dependencies
RUN pip install -r requirements.txt

# Expose the port your application will run on
EXPOSE 5000

# Define the command to run your application
CMD ["python", "app.py"]
