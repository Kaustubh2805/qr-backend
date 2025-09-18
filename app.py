from flask import Flask, render_template, request, jsonify, send_file
import qrcode
import io

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")   # <-- This will now load your webpage

@app.route("/api")
def api_status():
    return {"message": "QR Code Generator API is running!"}

@app.route("/generate_qr", methods=["POST"])
def generate_qr():
    data = request.form.get("data")
    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Generate QR code
    qr = qrcode.make(data)
    img_io = io.BytesIO()
    qr.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
