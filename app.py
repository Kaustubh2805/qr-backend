from flask import Flask, request, send_file, jsonify
import qrcode
import io

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify({"message": "QR Code Generator API is running!"})

@app.route("/generate_qr", methods=["POST"])
def generate_qr():
    try:
        data = request.json.get("text", "")
        if not data:
            return jsonify({"error": "No text provided"}), 400

        # Generate QR code
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_H,
            box_size=10,
            border=4,
        )
        qr.add_data(data)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")

        # Save to in-memory buffer
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)

        return send_file(buf, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
