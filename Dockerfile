FROM python:3.12-slim

WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY app.py .

# Copy SMS policy file from OPsKPI repo if available
COPY sms_policy.html . 2>/dev/null || echo "SMS policy file not included"

# Railway config
ENV PORT=8000
EXPOSE ${PORT}

# Run Flask app
CMD ["python", "app.py"]
