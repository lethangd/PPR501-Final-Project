# Crawler Dockerfile
# Build: docker build -t student-crawler ./crawler
# Run: docker run --rm -v ${PWD}/output:/app/output --network ppr501-final-project_default student-crawler

FROM python:3.11-slim

WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy crawler script
COPY crawl_and_analyze.py .

# Create output directory
RUN mkdir -p /app/output

# Default: use Docker network hostname (backend instead of localhost)
# Prefer XML API (more stable than HTML scraping)
ENV CRAWLER_URL=http://backend:8000/api/students

# Default command
CMD ["sh", "-c", "python crawl_and_analyze.py --url $CRAWLER_URL"]
