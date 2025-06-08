FROM python:3.11-slim

WORKDIR /app

# Copy the requirements file from the backend folder (since we're already in backend/)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all backend source code into the image
COPY . .

# Expose the port the app runs on
EXPOSE 5000

# Run the Flask app
CMD ["python", "main.py"]
