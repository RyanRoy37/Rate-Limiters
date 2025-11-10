# Use an official, slim Python base
FROM python:3.11-slim

# Set non-root user and dirs
ENV APP_HOME=/app
WORKDIR ${APP_HOME}

# Reduce layers: install OS packages needed for some Python wheels (if any),
# upgrade pip, then install python deps (cache busting using requirements.txt timestamp)
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc build-essential curl \
    && rm -rf /var/lib/apt/lists/*

# Copy only requirements first to leverage Docker cache
COPY requirements.txt .

# Ensure latest pip and install deps
RUN python -m pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Create a non-root user and fix permissions
RUN useradd --create-home --shell /bin/bash appuser \
    && chown -R appuser:appuser ${APP_HOME}

USER appuser

# Expose the port Uvicorn will listen on
EXPOSE 8000

# Environment: you can override these at docker run time if desired
ENV HOST=0.0.0.0
ENV PORT=8000
ENV UVICORN_WORKERS=1

# Healthcheck (optional): checks the root endpoint
#HEALTHCHECK --interval=30s --timeout=3s --start-period=10s \
 # CMD curl -f http://localhost:${PORT}/ || exit 1

# Default command to start the FastAPI app with uvicorn
CMD ["sh", "-c", "uvicorn main:app --host ${HOST} --port ${PORT} --workers ${UVICORN_WORKERS}"]
