from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.get("/")
def root():
    # A simple endpoint so students can see the container is alive.
    return jsonify({
        "service": "flask-actions-demo",
        "message": "Hello from Flask",
        "port": int(os.environ.get("PORT", "8080"))
    })

@app.get("/health")
def health():
    return jsonify({"status": "ok"})

if __name__ == "__main__":
    # Bind to 0.0.0.0 so Docker can publish the port properly.
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
