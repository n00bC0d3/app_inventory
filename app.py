import os
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from config import Config  # ✅ Import Config class

app = Flask(__name__)
app.config.from_object(Config)  # ✅ Load config properly

# Initialize extensions
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
Session(app)  # ✅ Initialize Flask-Session after config is loaded

# --- Models ---

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    inventory = db.relationship('Inventory', backref='creator', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Inventory(db.Model):
    __tablename__ = 'inventory'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    createTime = db.Column(db.DateTime, default=datetime.utcnow)
    lastUpdate = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# --- Routes ---

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('inventory_list'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('inventory_list'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/inventory')
@login_required
def inventory_list():
    items = Inventory.query.all()
    return render_template('inventory.html', items=items)

@app.route('/inventory/add', methods=['POST'])
@login_required
def inventory_add():
    name = request.form.get('name')
    description = request.form.get('description')
    new_item = Inventory(name=name, description=description, created_by=current_user.id)
    db.session.add(new_item)
    db.session.commit()
    return redirect(url_for('inventory_list'))

@app.route('/inventory/edit/<int:id>', methods=['POST'])
@login_required
def inventory_edit(id):
    item = Inventory.query.get_or_404(id)
    item.name = request.form.get('name')
    item.description = request.form.get('description')
    db.session.commit()
    return redirect(url_for('inventory_list'))

@app.route('/inventory/delete/<int:id>')
@login_required
def inventory_delete(id):
    item = Inventory.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return redirect(url_for('inventory_list'))

# --- DB Init ---

def init_db():
    with app.app_context():
        db.create_all()
        if not User.query.filter_by(username='admin').first():
            admin = User(username='admin')
            admin.set_password('password123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Default admin user created")

if __name__ == '__main__':
    init_db()
    app.run(debug=False, host='0.0.0.0', port=5000)