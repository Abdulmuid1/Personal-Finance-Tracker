# Base image (Python)
FROM python:3.11-slim

# Set working directory inside the container
WORKDIR /app

# # Install build dependencies for numpy, pandas, etc.
# # pandas, numpy, and matplotlib all have native C extensions and need a compiler during install.
# RUN apt-get update && \
#     apt-get install -y --no-install-recommends gcc build-essential && \
#     rm -rf /var/lib/apt/lists/*

# Copy the requirements first
COPY requirements.txt .

# Use pre-built wheels instead of building from source
RUN pip install --upgrade pip setuptools wheel

# Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files into the container
COPY . .

# Expose port 5000 (Flask's default port)
EXPOSE 5000

# Command to run the app
CMD ["python", "app.py"]
