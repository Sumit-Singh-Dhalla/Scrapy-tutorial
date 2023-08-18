# Use an official Python runtime as a parent image
FROM python:3.9.17-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the scrapy spider when the container launches
CMD scrapy crawl quotes
