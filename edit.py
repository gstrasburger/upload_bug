import os
import subprocess
import shlex
import datetime
from flask import Blueprint, flash, request, redirect, url_for, send_from_directory, render_template, Request, abort
from werkzeug.utils import secure_filename

bp = Blueprint('edit', __name__)
UPLOAD_FOLDER = './ORM/uploads'


#define a function which takes the first few chars in a rule and expresses that as a regex (e.g. E64 becomes ^E64*, G432-7 becomes ^G43[2-7]*)
def regexify(s):
    regex = ''
    if s[-2] == '-':
        regex = '^' + s[:-3] + '[' + s[-3:] + ']*'
    else:
        regex = '^' + s + '*'
    return regex

#define a function which takes the user input for the rules they desire to edit and turns them into one big regex
def regparse(l):
    list = l.split(',')
    bigreg = ''
    for term in list:
        if term[0] == ' ':
            term = term[1:0]
        bigreg = bigreg + '(' + regexify(term) + ')|'
    bigreg = bigreg[:-1]
    return bigreg

@bp.route('/edit/<path:filename>', methods=['GET','POST'])
def edit_file(filename):
    error=None
    if request.method == 'POST':
        #unzips the rules file to the appropriate directory
        print('unzip ' + os.path.join(UPLOAD_FOLDER, filename) + ' -d ' + UPLOAD_FOLDER)
        #subprocess.call(['pwd'])
        subprocess.call(['unzip', os.path.join(UPLOAD_FOLDER, filename)])
        subprocess.call(['rm', os.path.join(UPLOAD_FOLDER, filename)])
        #remove = request.form['remove']
        regex = request.form['regex']
        terms = request.form['terms']
        #change this later to determine the name of the directory by getting the zip info
        dirname = filename.rsplit('.', 1)[0]
        removearg = ''
        #if remove == True:
        #    removearg = 'remove'
        #else:
        removearg = 'identify'
        if regex=='':
            if terms!='':
                error='NoRegex'
                flash('Make sure to input a regex')
            else:
                regex='*'
        #calls the rule management shell script
        if error==None:
            try:
                subprocess.call([os.path.join(UPLOAD_FOLDER, 'rule_manager.sh'), dirname, removearg, terms, regex])
            except Exception as e:
                print(e)
                error=e
                flash('Couldn\'t edit the given zip file. Make sure you\'ve zipped a folder containing only the rules as text files')
        if error==None:
            subprocess.call(['rm', '-r',  os.path.join(UPLOAD_FOLDER, dirname)])
            subprocess.call(['cp', os.path.join(UPLOAD_FOLDER, 'superstringlog.txt'), os.path.join(UPLOAD_FOLDER, 'updated_rules')])
            timestamp = datetime.datetime.now()
            timestamp = timestamp[:10] + '_' + timestamp[11:16]
            sendfilename = 'rules_updated' + timestamp + '.zip'
            subprocess.call(['zip', '-r', os.path.join(UPLOAD_FOLDER, 'updated_rules'), sendfilename])
            return redirect(url_for('upload.uploaded_file', filename=sendfilename))
    
    print(error)
    return render_template('edit.html')
