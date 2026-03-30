FROM python:3.11-slim

# Security: run as non-root
RUN groupadd -r appuser && useradd -r -g appuser appuser

WORKDIR /app

# Install uv for fast dependency installation
RUN pip install --no-cache-dir uv==0.4.29

# Copy dependency files first (layer caching)
COPY pyproject.toml ./
COPY requirements.txt ./

# Install dependencies
RUN uv pip install --system --no-cache -r requirements.txt

# Copy application code
COPY . .

# Remove any .env files that might have leaked into the image
RUN find /app -name "*.env" -delete ; find /app -name ".env" -delete ; true

# Set ownership
RUN chown -R appuser:appuser /app

USER appuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
