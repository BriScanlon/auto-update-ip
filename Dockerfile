# Base image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy the application code
COPY . /app

# Install dependencies
RUN pip install -r requirements.txt

# Run the application
CMD ["python", "app.py"]