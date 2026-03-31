from flask import Flask, render_template, request, redirect, url_for, send_file
import os
from PIL import Image

app = Flask(__name__)

# folders
UPLOAD_FOLDER = "uploads"
OUTPUT_FOLDER = "static/output"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# 🏠 HOME PAGE
@app.route("/")
def home():
    return render_template("index.html")


# 📸 GENERATE PHOTO
@app.route("/generate", methods=["POST"])
def generate():
    if "photo" not in request.files:
        return "No file uploaded"

    file = request.files["photo"]

    if file.filename == "":
        return "No selected file"

    # save uploaded file
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # open image (you can keep your own logic here)
    img = Image.open(filepath)

    # example resize (keep your feature if you have)
    img = img.resize((300, 400))

    output_path = os.path.join(OUTPUT_FOLDER, "result.jpg")
    img.save(output_path)

    return redirect(url_for("result"))


# 📄 RESULT PAGE
@app.route("/result")
def result():
    return render_template("result.html")


# 📥 DOWNLOAD
@app.route("/download")
def download():
    return send_file("static/output/result.jpg", as_attachment=True)


# 🚀 IMPORTANT FOR RENDER
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
