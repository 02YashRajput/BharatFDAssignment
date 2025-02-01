# Use the official Python image from Docker Hub
FROM python:3.11-slim

# Set the working directory inside the container to the server directory
WORKDIR /app/server

# Copy the requirements.txt from the root directory into the container
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the server directory (where manage.py and the rest of the Django app resides)
COPY server /app/server

# Set environment variables
ENV PYTHONUNBUFFERED 1

# Expose the port the app will run on
EXPOSE 8000

# Command to run the Django server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
