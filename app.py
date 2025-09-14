from flask import Flask, request, jsonify, render_template
from pagerank.pagerank import iterate_pagerank, crawl, sample_pagerank
import shutil
from flask import jsonify
import os
import tempfile


app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST']) #backend route to handle file uploads
def visualize():
    uploaded_files = request.files.getlist("files")
    if uploaded_files <=  0:
        return render_template('result.html', error="No files uploaded.")
    



if __name__ == '__main__':
    app.run(debug=True)