from flask import Flask, send_from_directory[cite: 1]

app = Flask(__name__, static_folder="static")[cite: 1]

@app.route("/")[cite: 1]
def home():[cite: 1]
    return send_from_directory("static", "index.html")[cite: 1]

if __name__ == "__main__":[cite: 1]
    app.run(host="0.0.0.0", port=5000)[cite: 1]
