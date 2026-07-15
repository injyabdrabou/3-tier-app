import os
import time

from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)

DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "db"),
    "port": int(os.environ.get("DB_PORT", 3306)),
    "user": os.environ.get("DB_USER"),
    "password": os.environ.get("DB_PASSWORD"),
    "database": os.environ.get("DB_NAME"),
}


def get_connection(retries=10, delay=3):
    """Retry because MySQL takes longer to boot than Flask."""
    for attempt in range(retries):
        try:
            return mysql.connector.connect(**DB_CONFIG)
        except mysql.connector.Error:
            print(f"DB not ready (attempt {attempt + 1}/{retries}), retrying...")
            time.sleep(delay)
    raise RuntimeError("Could not connect to database")


@app.route("/health")
def health():
    return jsonify({"status": "ok"})


@app.route("/items")
def items():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM items;")
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(rows)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
