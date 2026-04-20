# Use a slim Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install ONLY necessary system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# NOW download the spaCy model (after spacy is installed via requirements.txt)
RUN python -m spacy download en_core_web_sm

# Copy the rest of the application code
COPY . .

# Expose port
EXPOSE 8000

# Command to run the application
CMD ["streamlit", "run", "app/streamlit_app.py", "--server.port=8000", "--server.address=0.0.0.0"]
