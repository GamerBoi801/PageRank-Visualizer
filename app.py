from flask import Flask, request, jsonify, render_template
from pagerank.pagerank import iterate_pagerank, crawl, sample_pagerank
import shutil
from flask import jsonify
import os
import tempfile
from werkzeug.utils import secure_filename

app = Flask(__name__)

DAMPING = 0.85
SAMPLES = 10000

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/visualize', methods=['POST']) #backend route to handle file uploads
def visualize():
    uploaded_files = request.files.getlist("files")
    if len(uploaded_files) <=  0:
        return render_template('result.html', error="No files uploaded.")
        #change result.html

    with tempfile.TemporaryDirectory() as tempdir:
        html_files = []

        #save only html files
        for file in uploaded_files:
            if file and file.filename.endswith('.html'):
                filename = secure_filename(file.filename)
                file_path = os.path.join(tempdir, filename)
                file.save(file_path)
                html_files.append(file_path)

            #Validate whether we have html files
            if not html_files:
                return jsonify({"error": "No valid HTML files uploaded."}), 400
        
        
        #crawl gets the corpus
        try:
            corpus = crawl(tempdir) 
        except FileNotFoundError or not corpus:
            return jsonify({"error": "No valid HTML files found in corpus."}), 400
        
        # run PageRank
        pagerank = iterate_pagerank(corpus, DAMPING) 

        #JSON response
        nodes = [{"id": page, "rank": rank} for page, rank in pagerank.items()]
        links = [
            {"source": page, "target": link}
            for page, targets in corpus.items()
            for link in targets
        ]

        return jsonify({"nodes": nodes, "links": links})
        
    

if __name__ == '__main__':
    app.run(debug=True)