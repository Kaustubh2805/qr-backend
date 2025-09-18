from flask import Flask, render_template, request, jsonify, send_file
import qrcode
import io

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api")
def api_status():
    return {"message": "QR Code Generator API is running!"}

@app.route("/generate_qr", methods=["POST"])
def generate_qr():
    data = request.form.get("data")
    fg_color = request.form.get("fg", "black")
    bg_color = request.form.get("bg", "white")
    size = int(request.form.get("size", 10))

    if not data:
        return jsonify({"error": "No data provided"}), 400

    qr = qrcode.QRCode(
        version=1,
        box_size=size,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color=fg_color, back_color=bg_color)

    img_io = io.BytesIO()
    img.save(img_io, "PNG")
    img_io.seek(0)

    return send_file(img_io, mimetype="image/png")

if __name__ == "__main__":
    app.run(debug=True)
