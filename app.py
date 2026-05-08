import os
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///calculations.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.secret_key = 'super_secret_key'

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

db = SQLAlchemy(app)

# Database Model (Phase B)
class Calculation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    microscope_type = db.Column(db.String(100), nullable=False)
    measured_size = db.Column(db.Float, nullable=False)
    real_size = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(10), nullable=False)
    image_filename = db.Column(db.String(100), nullable=True)

# Predefined microscopes (Phase A & D)
MICROSCOPES = {
    'Light Microscope (1000x)': 1000,
    'Scanning Electron Microscope (100,000x)': 100000,
    'Transmission Electron Microscope (5,000,000x)': 5000000
}

# Unit multipliers from base mm
UNITS = {
    'nm': 1e6,
    'µm': 1000,
    'mm': 1,
    'cm': 0.1,
    'm': 0.001
}

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    result_data = None
    if request.method == 'POST':
        username = request.form['username']
        measured_size = float(request.form['measured_size'])
        microscope_type = request.form['microscope_type']
        unit = request.form['unit']
        
        # Image Upload Handling
        image_file = request.files.get('specimen_image')
        filename = None
        if image_file and image_file.filename != '':
            filename = secure_filename(image_file.filename)
            image_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        # Core Calculation Logic
        mag_factor = MICROSCOPES[microscope_type]
        real_size_mm = measured_size / mag_factor
        final_real_size = real_size_mm * UNITS[unit]
        
        # Save to Database
        new_calc = Calculation(
            username=username,
            microscope_type=microscope_type,
            measured_size=measured_size,
            real_size=final_real_size,
            unit=unit,
            image_filename=filename
        )
        db.session.add(new_calc)
        db.session.commit()
        
        result_data = {
            'measured': measured_size,
            'mag_factor': mag_factor,
            'real_size': final_real_size,
            'unit': unit,
            'filename': filename
        }

    # Fetch calculation history
    history = Calculation.query.order_by(Calculation.id.desc()).all()
    return render_template('index.html', microscopes=MICROSCOPES.keys(), units=UNITS.keys(), result=result_data, history=history)

if __name__ == '__main__':
    app.run(debug=True)