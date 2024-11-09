# Use the official Python 3.11 image from Docker Hub
FROM python:3.11-slim

# Set a working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install any dependencies specified in requirements.txt
RUN pip install -r requirements.txt

# Copy the current directory contents into the container
COPY . .

# Specify the command to run your application
CMD ["python", "your_script.py"]
