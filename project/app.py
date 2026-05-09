"""Flask API application.

Endpoints:
- GET /health: Service health check.
- GET /convert?usd=<amount>: Converts USD to INR using a live exchange rate.
- GET /report: Returns a sample JSON report with random data.
"""

from __future__ import annotations

import logging
import os
import random
from datetime import UTC, datetime
from decimal import Decimal, InvalidOperation
from typing import Any

import requests
from flask import Flask, jsonify, request

# Basic structured logging for observability in production-like environments.
logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(message)s",
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# External API endpoint for live FX rates.
# exchangerate.host offers simple conversion when provided with an access key in
# some plans; if unavailable, this code gracefully returns an informative error.
EXCHANGE_API_URL = "https://api.exchangerate.host/convert"
REQUEST_TIMEOUT_SECONDS = 10


def parse_usd_amount(raw_value: str | None) -> Decimal:
    """Parse and validate USD query parameter as a positive decimal number."""
    if raw_value is None:
        raise ValueError("Missing required query parameter: usd")

    try:
        amount = Decimal(raw_value)
    except (InvalidOperation, TypeError) as exc:
        raise ValueError("Invalid usd amount. Provide a numeric value.") from exc

    if amount < 0:
        raise ValueError("Invalid usd amount. Value must be non-negative.")

    return amount


def fetch_usd_to_inr_rate() -> Decimal:
    """Fetch live USD->INR exchange rate from the external provider."""
    params = {"from": "USD", "to": "INR", "amount": 1}
    response = requests.get(EXCHANGE_API_URL, params=params, timeout=REQUEST_TIMEOUT_SECONDS)
    response.raise_for_status()

    payload: dict[str, Any] = response.json()

    # Expected shape often contains a numeric `result` field.
    rate_value = payload.get("result")
    if rate_value is None:
        raise RuntimeError("Exchange provider response missing 'result' field.")

    try:
        return Decimal(str(rate_value))
    except (InvalidOperation, TypeError) as exc:
        raise RuntimeError("Exchange provider returned non-numeric rate.") from exc


@app.errorhandler(Exception)
def handle_unexpected_error(error: Exception):
    """Catch-all handler to avoid leaking internals while logging details."""
    logger.exception("Unhandled exception: %s", error)
    return jsonify({"error": "Internal server error"}), 500


@app.get("/health")
def health() -> tuple[Any, int]:
    """Simple health check endpoint."""
    return jsonify({"status": "ok"}), 200


@app.get("/convert")
def convert() -> tuple[Any, int]:
    """Convert a USD amount to INR using a live exchange rate."""
    try:
        usd_amount = parse_usd_amount(request.args.get("usd"))
    except ValueError as exc:
        return jsonify({"error": str(exc)}), 400

    try:
        usd_to_inr_rate = fetch_usd_to_inr_rate()
    except requests.RequestException as exc:
        logger.warning("Exchange API request failed: %s", exc)
        return jsonify({"error": "Failed to fetch live exchange rate."}), 502
    except RuntimeError as exc:
        logger.warning("Exchange API returned unexpected payload: %s", exc)
        return jsonify({"error": "Exchange rate service response invalid."}), 502

    inr_amount = (usd_amount * usd_to_inr_rate).quantize(Decimal("0.01"))

    return (
        jsonify(
            {
                "usd": float(usd_amount),
                "inr": float(inr_amount),
                "rate": float(usd_to_inr_rate),
                "currency_pair": "USD/INR",
                "timestamp_utc": datetime.now(UTC).isoformat(),
            }
        ),
        200,
    )


@app.get("/report")
def report() -> tuple[Any, int]:
    """Generate a sample JSON report with random metrics and rows."""
    rows = []
    for idx in range(1, 6):
        rows.append(
            {
                "id": idx,
                "category": random.choice(["alpha", "beta", "gamma"]),
                "score": round(random.uniform(0, 100), 2),
                "active": random.choice([True, False]),
            }
        )

    report_payload = {
        "report_id": f"RPT-{random.randint(1000, 9999)}",
        "generated_at_utc": datetime.now(UTC).isoformat(),
        "summary": {
            "row_count": len(rows),
            "avg_score": round(sum(row["score"] for row in rows) / len(rows), 2),
        },
        "data": rows,
    }

    return jsonify(report_payload), 200


if __name__ == "__main__":
    # For local development. In production, use a WSGI server (gunicorn/uwsgi).
    app.run(host="127.0.0.1", port=5000, debug=False)
