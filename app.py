import os
from flask import Flask, render_template, request, send_file
from PIL import Image, ImageEnhance

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/edit', methods=['POST'])
def edit_photo():
    file = request.files['image']
    filter_type = request.form.get('filter')
    
    if file:
        img_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(img_path)
        img = Image.open(img_path).convert("RGB")
        
        if filter_type == 'vibrant':
            img = ImageEnhance.Color(img).enhance(1.8)
            img = ImageEnhance.Contrast(img).enhance(1.2)
        elif filter_type == 'cinematic':
            img = ImageEnhance.Contrast(img).enhance(1.4)
            r, g, b = img.split()
            r = r.point(lambda i: i * 1.1)
            b = b.point(lambda i: i * 0.8)
            img = Image.merge('RGB', (r, g, b))

        edited_filename = "edited_" + file.filename
        edited_path = os.path.join(UPLOAD_FOLDER, edited_filename)
        img.save(edited_path)
        return send_file(edited_path, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
