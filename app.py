from flask import Flask, request, render_template, send_file, jsonify
from flaskwebgui import FlaskUI
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.colors as mcolors
from matplotlib import font_manager as fm
import matplotlib.patches as patches
import random
import json
from core_file import giveFig

random.seed(38)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'static/results'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_csv', methods=['POST'])
def process_csv():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'data.csv')
        file.save(filepath)
        df = pd.read_csv(filepath)
        return jsonify({"column_count": len(df.columns)})
    
    return jsonify({"error": "Invalid file type"})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part"
    
    file = request.files['file']
    if file.filename == '':
        return "No selected file"
    
    if file and file.filename.endswith('.csv'):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], 'data.csv')
        file.save(filepath)
        df = pd.read_csv(filepath, encoding='utf-8')
        
        selected_colors = json.loads(request.form.get('selectedColors', '[]'))
        custom_text = request.form.get('customText', 'Languages')
        file_format = request.form.get('fileFormat', 'png')
        center_color = request.form.get('centerColor', 'white')  
        
        giveFig(False, df, custom_text, False, True, lw=1, dpi1=100, l=18, b=8, colors=selected_colors, format=file_format, center_color=center_color)  # Modified to include center_color
        
        return render_template('result.html', img_path=f'static/results/plot.png')
    
    return "Invalid file type"

@app.route('/download')
def download_file():
    filename = f'plot.{file_format}'
    return send_file(os.path.join(app.config['RESULT_FOLDER'], filename), as_attachment=True)

@app.route('/colors/<filename>')
def serve_color(filename):
    return send_file(f'colors/{filename}', mimetype='image/png')

if __name__ == '__main__':
    FlaskUI(app=app, server="flask").run()