# E2B Sandbox Dockerfile for KimiK2Manim
# Base image with Python 3.13
FROM python:3.13-slim

# Install system dependencies for Manim and multimedia processing
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libcairo2-dev \
    libpango1.0-dev \
    texlive \
    texlive-latex-extra \
    texlive-fonts-extra \
    texlive-latex-recommended \
    texlive-science \
    texlive-fonts-recommended \
    dvipng \
    cm-super \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /home/user/kimik2

# Copy requirements first for better caching
COPY requirements.txt pyproject.toml ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install Manim
RUN pip install --no-cache-dir manim

# Install additional useful tools for interactive exploration
RUN pip install --no-cache-dir \
    jupyter \
    ipywidgets \
    matplotlib \
    numpy \
    pandas \
    rich \
    typer \
    httpx

# Copy the entire project
COPY . .

# Create output directories
RUN mkdir -p /home/user/kimik2/media/videos \
    /home/user/kimik2/media/images \
    /home/user/kimik2/output \
    /home/user/kimik2/logs

# Set environment variables for Manim
ENV MANIM_OUTPUT_DIR=/home/user/kimik2/media

# Expose port for Jupyter (if needed)
EXPOSE 8888

# Default command
CMD ["python", "-m", "examples.test_kimi_integration"]
