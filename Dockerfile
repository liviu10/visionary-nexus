# Use the official Python 3.14.2 image
FROM python:3.14.2

# Set environment variables
# PYTHONUNBUFFERED: Ensures that python output is sent straight to terminal (useful for logs)
# PYTHONDONTWRITEBYTECODE: Prevents Python from writing .pyc files to disk
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt /app/

# Install dependencies
# Using the full image ensures build tools like gcc are available if needed
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . /app/

# Set the default command to run your script
CMD ["python", "main.py"]