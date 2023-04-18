# Use an official Python runtime as a parent image

FROM python:3.11.2-slim-bullseye

# Set the working directory to /app

WORKDIR /app

# Copy the requirements file into the container

COPY requirements.txt .

# Install the dependencies

RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask app code into the container

COPY main.py .

# Expose the port that the Flask app will run on

EXPOSE 8080

# Start the Flask app when the container starts

CMD ["python3", "main.py"]
