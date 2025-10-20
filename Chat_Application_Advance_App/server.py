# server.py
import os
from datetime import datetime, timedelta
from flask import Flask, request, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_socketio import SocketIO, join_room, leave_room, emit

BASE_DIR = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'replace-with-a-strong-secret'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(BASE_DIR, 'chat.db')
app.config['JWT_SECRET_KEY'] = 'replace-with-another-strong-secret'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

db = SQLAlchemy(app)
jwt = JWTManager(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')  # or 'gevent'

# -------------------------
# Models
# -------------------------
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    room = db.Column(db.String(120), nullable=False)
    sender = db.Column(db.String(80), nullable=False)
    content = db.Column(db.Text, nullable=True)  # text or media url
    is_media = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# -------------------------
# REST: Auth & Uploads
# -------------------------
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    if not username or not password:
        return jsonify(msg="username and password required"), 400
    if User.query.filter_by(username=username).first():
        return jsonify(msg="username taken"), 409
    user = User(username=username, password_hash=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return jsonify(msg="registered"), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username'); password = data.get('password')
    user = User.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify(msg="bad credentials"), 401
    access_token = create_access_token(identity=username, expires_delta=timedelta(days=7))
    return jsonify(access_token=access_token)

@app.route('/upload', methods=['POST'])
@jwt_required()
def upload():
    # simple image upload
    if 'file' not in request.files:
        return jsonify(msg="no file part"), 400
    f = request.files['file']
    if f.filename == '':
        return jsonify(msg="no selected file"), 400
    # safe filename handling omitted for brevity: you should use werkzeug.utils.secure_filename
    filename = f'{int(datetime.utcnow().timestamp())}_{f.filename}'
    path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    f.save(path)
    url = f'/uploads/{filename}'
    return jsonify(url=url), 201

@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    # Optionally protect with authentication
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# -------------------------
# Socket.IO events
# -------------------------
@socketio.on('join')
def handle_join(data):
    room = data.get('room')
    username = data.get('username')
    join_room(room)
    emit('system', {'msg': f'{username} joined {room}'}, room=room)
    # send recent history
    last = Message.query.filter_by(room=room).order_by(Message.timestamp.desc()).limit(50).all()[::-1]
    history = [{'sender': m.sender, 'content': m.content, 'is_media': m.is_media, 'timestamp': m.timestamp.isoformat()} for m in last]
    emit('history', history)

@socketio.on('leave')
def handle_leave(data):
    room = data.get('room'); username = data.get('username')
    leave_room(room)
    emit('system', {'msg': f'{username} left {room}'}, room=room)

@socketio.on('message')
def handle_message(data):
    # data: {room, username, content, is_media}
    room = data.get('room'); username = data.get('username'); content = data.get('content')
    is_media = data.get('is_media', False)
    # save to DB
    m = Message(room=room, sender=username, content=content, is_media=is_media)
    db.session.add(m); db.session.commit()
    emit('message', {'sender': username, 'content': content, 'is_media': is_media, 'timestamp': m.timestamp.isoformat()}, room=room)

# -------------------------
# Bootstrap
# -------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    # use eventlet or gevent for production socket support
    socketio.run(app, host='0.0.0.0', port=5000)
