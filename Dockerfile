# Use official Python image
FROM python:3.10-slim

# Install tesseract-ocr
RUN apt-get update && apt-get install -y tesseract-ocr

# Set work directory
WORKDIR /app

# Copy all files
COPY . .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port (Flask default)
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
