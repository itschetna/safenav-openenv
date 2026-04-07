FROM python:3.10

# Set working directory
WORKDIR /app

# Prevent Python buffering (important for logs)
ENV PYTHONUNBUFFERED=1

# Copy only requirements first (better caching)
COPY requirements.txt .

# Upgrade pip + install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy rest of project
COPY . .

# Expose HF Spaces port
EXPOSE 7860

# Run FastAPI app
CMD ["uvicorn", "my_env.api:app", "--host", "0.0.0.0", "--port", "7860"]