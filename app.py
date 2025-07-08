from flask import Flask, render_template, request
import pytesseract
import cv2
import os
import re
from difflib import SequenceMatcher

# You can comment this line since Render installs tesseract via build.sh
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

app = Flask(__name__)

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PLATES_DB = os.path.join(BASE_DIR, 'plates_db.txt')

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def load_valid_plates():
    with open(PLATES_DB, 'r') as f:
        plates = f.read().splitlines()
    plates = [p.strip().upper() for p in plates]
    return plates

def is_similar(a, b, threshold=0.8):
    return SequenceMatcher(None, a, b).ratio() >= threshold

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(filepath)

            img = cv2.imread(filepath)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            gray = cv2.bilateralFilter(gray, 11, 17, 17)
            _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)

            text = pytesseract.image_to_string(thresh, config='--psm 7')
            text = text.strip().replace(" ", "").upper()
            text = re.sub(r'\W+', '', text)

            valid_plates = load_valid_plates()
            matched = any(is_similar(text, plate) for plate in valid_plates)

            if matched:
                result = "✅ Real Number Plate (Approx Match)"
            else:
                result = "❌ Fake Number Plate"

            return render_template('result.html', text=text, result=result, image_path=filepath)
        else:
            return "Invalid file type. Please upload a PNG, JPG, or JPEG image."

    return render_template('index.html')

# ✅ Updated for Render deployment
if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
# Deployment port fix
