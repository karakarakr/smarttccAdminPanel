from flask import render_template, flash, url_for, redirect, request
from weblibs.forms import LoginForm, RegistrationForm, DeviceAddForm, BrokerChangeForm
from weblibs import app, db, bcrypt
from weblibs.models import User, Device
from flask_login import login_user, current_user, logout_user, login_required

# Need to work on devices.html
# Now my task - design

@app.route("/")
def index():
    if current_user.is_authenticated:
        user = User.query.filter_by(id=current_user.id).first()
        device = Device.query.filter_by(user_id=current_user.id).all()
        return render_template("index.html", user=user, devices=device)
    return redirect(url_for('login'))

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('index'))
        flash('Login unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/server", methods=['GET', 'POST'])
@login_required
def server():
    user = User.query.filter_by(id=current_user.id).first()
    form = BrokerChangeForm()
    if form.validate_on_submit():
        user.broker_addr = form.addr.data
        user.broker_port = form.port.data
        user.broker_password = form.password.data
        print(form.addr.data)
        db.session.commit()
        print(user.broker_addr)
        flash(f'Broker has been changed successfully!', 'success')
        return redirect(url_for('server'))
    print(form.addr.data)
    return render_template('server.html', title='Server settings', form=form, user=user)

@app.route("/domoticz", methods=['GET', 'POST'])
@login_required
def domoticz():
    user = User.query.filter_by(id=current_user.id).first()
    form = DomoticzChangeForm()
    if form.validate_on_submit():
        user.broker_addr = form.addr.data
        user.broker_port = form.port.data
        user.broker_password = form.password.data
        print(form.addr.data)
        db.session.commit()
        print(user.broker_addr)
        flash(f'Broker has been changed successfully!', 'success')
        return redirect(url_for('domoticz'))
    print(form.addr.data)
    return render_template('domoticz.html', title='Domoticz settings', form=form, user=user)

@app.route("/devices", methods=['GET', 'POST'])
@login_required
def devices():
    form = DeviceAddForm()
    user = User.query.filter_by(id=current_user.id).first()
    if form.validate_on_submit():
        device = Device(ieee_addr=form.ieee_addr.data, user_id=current_user.id)
        if form.add.data:
            db.session.add(device)
            flash(f'Device {form.ieee_addr.data} added successfully!', 'success')
        else:
            existed_device = Device.query.filter_by(ieee_addr=form.ieee_addr.data, user_id=current_user.id).first()
            db.session.delete(existed_device)
            flash(f'Device {form.ieee_addr.data} removed successfully!', 'success')
        db.session.commit()
        return redirect(url_for('devices'))
    return render_template('devices.html', title='Devices', form=form, devices=Device.query.filter_by(user_id=current_user.id).all(), user=user)