from flask import render_template, jsonify, redirect, url_for, request
from project import app
import os
from project import async_tasks
from project.app_state import application_state, lock
import threading
import copy
import sys

#TODO set registry!!!
@app.route('/')
def index():
    lock.acquire()
    application_state['license_check']['message'] = []
    application_state['license_check']['retry_active'] = False 
    lock.release()
    
    return render_template('welcome.html')

@app.route('/eula')
def eula():
    return render_template('eula.html')


@app.route('/check')
def check():
    t = threading.Thread(target=async_tasks.run_checks,
        daemon=True)
    t.start()
    return render_template('check.html')

@app.route('/location')
def location():
    return render_template('location.html')

@app.route('/choose-path')
def choose_path():
    t = threading.Thread(target=async_tasks.choose_dir)
    t.start()
    return render_template('location.html')


@app.route('/create_user', methods=("GET", "POST"))
def create_user():
    if request.method == 'POST':
        application_state['superuser'].update({
            'username': request.form['username'],
            'password': request.form['password'],
            "email": request.form['email']
        })
        return redirect(url_for('install'))
    else:
        return render_template('user_create.html')


@app.route('/install')
def install():
    t = threading.Thread(target=async_tasks.install, daemon=True)
    t.start()
    return render_template('install.html')


@app.route('/install-success')
def install_success():
    return render_template('install_success.html')


@app.route('/install-failure')
def install_failure():
    return render_template('install_failure.html')


@app.route('/status')
def status():
    lock.acquire()
    global application_state
    state = copy.deepcopy(application_state)
    lock.release()
    return jsonify(state)

@app.route('/finish')
def finish():
    sys.exit()
    return ''