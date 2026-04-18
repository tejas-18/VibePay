FROM python:3.11-slim

WORKDIR /app

# Copy requirements first to leverage Docker cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port 8080 as strictly required by Cloud Run
EXPOSE 8080

# Run the Streamlit app
CMD ["streamlit", "run", "main.py", "--server.port", "8080", "--server.address", "0.0.0.0"]
