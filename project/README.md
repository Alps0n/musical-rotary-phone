# Flask Currency & Report API

A production-style Flask API that runs on `localhost:5000` and provides:

- `GET /health` → returns `{"status": "ok"}`
- `GET /convert?usd=100` → converts USD to INR using a live exchange rate
- `GET /report` → returns a sample JSON report with random data

## Project structure

```text
project/
  app.py
  requirements.txt
  run.sh
  README.md
```

## Prerequisites

- Python 3.10+
- Internet access (required for live FX rates on `/convert`)

## Run locally

```bash
cd project
chmod +x run.sh
./run.sh
```

The server starts at:

- `http://127.0.0.1:5000`

## Example requests

### Health check

```bash
curl "http://127.0.0.1:5000/health"
```

### Convert USD to INR

```bash
curl "http://127.0.0.1:5000/convert?usd=100"
```

### Generate sample report

```bash
curl "http://127.0.0.1:5000/report"
```

## Error handling

- Input validation errors return HTTP `400`
- Upstream FX provider errors return HTTP `502`
- Unexpected internal errors return HTTP `500`

## Notes for production deployment

For production, run `app.py` behind a WSGI server (e.g., Gunicorn) and reverse proxy (e.g., Nginx), with environment-specific logging and monitoring.
