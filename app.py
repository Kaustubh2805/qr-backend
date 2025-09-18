from flask import Flask, render_template, request, jsonify, send_file
import qrcode
import io

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")   # 👈 loads your webpage

@app.route("/api")
def api_status():
    return {"message": "QR Code Generator API is running!"}

@app.route("/generate_qr", methods=["POST"])
def generate_qr():
    data = request.form.get("data")
    fg = request.form.get("fg", "#000000")
    bg = request.form.get("bg", "#ffffff")
    size = int(request.form.get("size", 10))

    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Generate QR code
    qr = qrcode.QRCode(box_size=size, border=2)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fg, back_color=bg)

    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
