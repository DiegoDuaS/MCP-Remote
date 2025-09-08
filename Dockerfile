# Use official Python slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port required by Cloud Run
EXPOSE 8080

# Run the FastAPI server
CMD ["uvicorn", "server.mcp_server:app", "--host", "0.0.0.0", "--port", "8080"]
