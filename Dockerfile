FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libmysqlclient-dev \
    gcc

# Set work directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Command to run the application
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "web.wsgi:application"]
