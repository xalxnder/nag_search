from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename
from .search import Search, matches, RESULTS
import os
app = Flask(__name__)
ALLOWED_EXTENSIONS = {'txt'}
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(APP_ROOT, 'static/uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


searchTool = Search()
@app.route('/', methods=["POST", "GET"])
def index():
    matches.clear()
    RESULTS.clear()
    if request.method == "POST" and 'service' in request.form:
        search_term = request.form["service"]
        searchTool.search_service(search_term)
        return redirect('/nag_search/results')
    elif request.method == "POST" and request.files:
        file = request.files['text_file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
        with open(os.path.join(
                app.config['UPLOAD_FOLDER'], file.filename), 'r') as doc:
            for line in doc:
                stripped_line = line.strip()
                searchTool.search_file(stripped_line)
        return redirect('/nag_search/file-results')
    elif request.method == "POST" and 'host' in request.form:
        host = request.form["host"]
        searchTool.search_host(host)
        return redirect('/nag_search/results')
    else:
        return render_template('index.html')


@app.route('/results', methods=["POST", "GET"])
def results():
    return render_template('results.html', matches=matches)


@app.route('/file-results', methods=["POST", "GET"])
def file_results():
    return render_template('file-results.html', RESULTS=RESULTS)


if __name__ == "__main__":
    app.run(debug=True)
