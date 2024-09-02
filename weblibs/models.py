from weblibs import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    devices = db.relationship('Device', backref='user')

    broker_addr = db.Column(db.String(30), nullable=False, default='broker.hivemq.com')
    broker_port = db.Column(db.String(5), nullable=False, default='8083')
    broker_password = db.Column(db.String(50))

    # domoticz_addr = db.Column(db.String(30), nullable=False, default='broker.hivemq.com')
    # domoticz_port = db.Column(db.String(5), nullable=False, default='8083')
    # domoticz_password = db.Column(db.String(50))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.broker_addr}', '{self.broker_port}', '{self.broker_password}', '{self.domoticz_addr}', '{self.domoticz_port}', '{self.domoticz_password}')"

class Device(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ieee_addr = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Device('{self.ieee_addr}', {self.user_id})"