FROM python:3.12-slim

WORKDIR /app

# Copy requirements first for better caching
COPY customer-service/requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared utilities
COPY shared /app/shared

# Copy application code
COPY customer-service/ .

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]