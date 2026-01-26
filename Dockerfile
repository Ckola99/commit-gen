FROM python:3.11-slim

# Install git (required for diff/commit)
RUN apt-get update \
 && apt-get install -y git \
 && rm -rf /var/lib/apt/lists/*

# Create non-root user
RUN useradd -m app

WORKDIR /workspace

# Copy project metadata
COPY pyproject.toml README.md ./

# Copy the src layout exactly as-is
COPY src ./src

RUN chown -R app:app /workspace

USER app

# Install the package
RUN pip install --no-cache-dir .

# Run commitgen by default
ENTRYPOINT ["commitgen"]
