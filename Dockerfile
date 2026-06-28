# Use official lightweight Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /code

# Copy requirements file first (for caching layers)
COPY ./requirements.txt /code/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

# Copy all project files into the container
COPY . .

# Create and switch to a non-root user (Hugging Face requirements)
RUN useradd -m -u 1000 user
RUN chown -R user:user /code
USER user

# Set environment home variables for writable caches (Hugging Face requirement)
ENV HOME=/home/user \
    PATH=/home/user/.local/bin:$PATH

# Expose standard HF Spaces port
EXPOSE 7860

# Start ASGI application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "7860"]
