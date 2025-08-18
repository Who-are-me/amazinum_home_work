# ---------- Base ----------
FROM python:3.12-slim AS base

# Avoid interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Set working directory
WORKDIR /app

# Copy app code
COPY . .
COPY . /app

# Install system dependencies (needed for Pillow, TensorFlow, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libglib2.0-0 \
        libsm6 \
        libxrender1 \
        libxext6 \
        git \
    && rm -rf /var/lib/apt/lists/*

# ---------- Dependencies ----------
FROM base AS deps

# Copy requirements file first (caching)
COPY app/requirements.txt .

# Install Python packages
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# ---------- Final ----------
FROM base AS final

# Copy installed Python packages from deps
COPY --from=deps /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=deps /usr/local/bin /usr/local/bin

# Expose port
EXPOSE 8000

# Command to run FastAPI with Uvicorn
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
