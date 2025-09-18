from flask import Flask, render_template, request
import qrcode
import io
import base64

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate_qr():
    data = request.form.get("data")
    if not data:
        return render_template("index.html", error="⚠ Please enter some text or URL.")

    # Generate QR code
    qr = qrcode.make(data)
    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")
    img_str = base64.b64encode(buffer.getvalue()).decode()

    return render_template("index.html", qr_code=img_str, text=data)

if __name__ == "__main__":
    app.run(debug=True)
