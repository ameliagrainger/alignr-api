FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy all app files
COPY . .

# Upgrade pip and setuptools to fix security issues
RUN pip install --upgrade pip setuptools \
    && pip install --no-cache-dir -r requirements.txt

# Expose the API port
EXPOSE 8080

# Run the app
CMD ["python", "app.py"]

