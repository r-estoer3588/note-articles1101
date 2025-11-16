from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/health')
def health():
    return jsonify({"status": "ok"})

if __name__ == '__main__':
    print("Starting Flask on port 5679...")
    app.run(host='0.0.0.0', port=5679, debug=False)
    print("Flask stopped")
