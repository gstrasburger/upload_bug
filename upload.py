import os
from flask import Blueprint, flash, request, redirect, url_for, send_from_directory, render_template, Request, abort
from werkzeug.utils import secure_filename

bp = Blueprint('upload', __name__)
UPLOAD_FOLDER = 'ORM/uploads'
ALLOWED_EXTENSIONS = {'zip'}

#a function which determines if a file is of the allowed type
def allowed_file(filename):
    return '.' in filename and  filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@bp.route('/upload', methods=['GET','POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('upload.upload_file', filename=filename))

    return render_template('uploads/upload_file.html')

@bp.route('/uploads/<path:filename>', methods=['GET','POST'])
def uploaded_file(filename):
    print(filename+" "+UPLOAD_FOLDER)
    try:
        return send_from_directory(UPLOAD_FOLDER, filename, as_attachment=True)
    except Exception as e:
        print(e)
        abort(404)

