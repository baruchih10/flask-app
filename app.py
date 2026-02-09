from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.get("/")
def root():
    # A simple endpoint so students can see the container is alive.
    return jsonify({
        "service": "flask-actions-demo",
        "message": "Hello from Flask",
        "port": int(os.environ.get("PORT", "5000"))
    })


@app.get("/my-name")
def my_name():
    # A simple endpoint so students can see the container is alive.
    return jsonify({
        "my-name is": "King Baruchi"
    })


@app.get("/ai")
def ai():
    # A simple endpoint so students can see the container is alive.
    return jsonify({
        "invoke_ai": "predict next buy"
    })


@app.get("/release-2")
def release_2():
    return jsonify({"living in release": "2.0.0"})


@app.get("/release-3")
def release_3():
    return jsonify({"living in release": "3.0.0"})


if __name__ == "__main__":
    # Bind to 0.0.0.0 so Docker can publish the port properly.
    port = int(os.environ.get("PORT", "5000"))
    app.run(host="0.0.0.0", port=port)
