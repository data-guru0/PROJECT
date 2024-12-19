# Use a lightweight Python image
FROM python:slim

# Set environment variables to prevent Python from writing .pyc files & Ensure Python output is not buffered
# This reduces the docker image size further
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy only the requirements file 
COPY requirements.txt requirements.txt

# Install required packages but do not store cache files to reduce image size
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Train the model before running the application
RUN dvc repro

# Expose the port that Flask will run on
EXPOSE 5000

# Command to run the app
CMD ["python", "application.py"]