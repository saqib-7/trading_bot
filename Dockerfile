FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Environment variables for Binance Testnet credentials 
ENV BINANCE_API_KEY=""
ENV BINANCE_API_SECRET=""

# Default to running the CLI's help page
ENTRYPOINT ["python", "cli.py"]
CMD ["--help"]
