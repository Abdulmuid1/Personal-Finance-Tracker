# 1. Base image (Python)
FROM python:3.11-slim

# 2. Set working directory inside the container
WORKDIR /app

# 3. Copy project files into the container
COPY . .

# 4. Install dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# 5. Expose port 5000 (Flask's default port)
EXPOSE 5000

# 6. Run the app
CMD ["python", "app.py"]
