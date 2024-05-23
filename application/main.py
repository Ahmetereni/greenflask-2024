import os
from flask import Blueprint, render_template, session, send_file, request, redirect, url_for
from flask_login import login_required
from path import mypath
from werkzeug.utils import secure_filename

main = Blueprint('main', __name__)
# setting up directory
ABSOLUTE_PATH = mypath()
ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/view/<path:filename>')
@login_required
def send_attachment(filename):
    # setting up directory
    strusername = str(session["username"])
    userfile = os.path.join(ABSOLUTE_PATH, 'static', 'users', strusername, filename)
    return send_file(userfile)

@main.route('/view', methods=['GET', 'POST'])
def view():
    strusername = str(session["username"])
    users_dir = os.path.join(ABSOLUTE_PATH, 'static', 'users', strusername)

    upload_files = request.files.getlist('file')

    if request.method == 'POST':
        for file in upload_files:
            filename = file.filename
            if allowed_file(filename):
                file.save(os.path.join(users_dir, secure_filename(filename)))
                extension = filename.rsplit('.', 1)[1].lower()
                processed_filepath = os.path.join(users_dir, filename)

        return render_template('view.html', users_dir=os.listdir(users_dir), dirname=strusername)
    
    return render_template('view.html', users_dir=os.listdir(users_dir), dirname=strusername)

@main.route('/delete/<path:filename>', methods=['GET'])
@login_required
def delete(filename):
    strusername = str(session["username"])

    userfile = os.path.join(ABSOLUTE_PATH, 'static', 'users', strusername, filename)

    filters = {
        "name": filename
    }
    try:
        os.remove(userfile)
        return redirect(url_for('main.view'))
    except Exception as e:
        return f"Error deleting file: {e}"
