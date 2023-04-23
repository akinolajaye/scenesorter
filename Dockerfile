# Use the official Python base image
FROM python:3.11

# Set the working directory
WORKDIR /app


# Copy the requirements.txt file into the container
COPY requirements.txt /app

# Install any needed packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y


# Copy the rest of the application code into the container
COPY . /app

# Run the Python script
CMD ["python", "./scenesorter.py", "-f", "media", "-d", "0.7"]

