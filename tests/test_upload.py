# -*- coding: utf-8 -*-

import os

from flask import Flask, request, render_template, redirect, url_for

from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = 'static/Uploads'


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'GET':
        return render_template('upload.html')
    elif request.method == 'POST':
        f = request.files['file']

        fname = secure_filename(f.filename)  # 获取一个安全的文件名，且仅仅支持ascii字符；

        f.save(os.path.join(UPLOAD_FOLDER, fname))

        return '上传成功'


@app.route('/')
def index():
    return redirect(url_for('upload'), 302)

if __name__ == '__main__':
    app.run(debug=True)
