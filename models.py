from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import uuid
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(20), default='employee')  # 'employee' or 'admin'
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Attendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    morning_check_in = db.Column(db.DateTime)
    morning_check_out = db.Column(db.DateTime)
    afternoon_check_in = db.Column(db.DateTime)
    afternoon_check_out = db.Column(db.DateTime)
    work_hours = db.Column(db.Float, default=0.0)
    morning_work_hours = db.Column(db.Float, default=0.0)
    afternoon_work_hours = db.Column(db.Float, default=0.0)
    late = db.Column(db.Boolean, default=False)
    late_minutes = db.Column(db.Integer, default=0)
    late_reason = db.Column(db.String(200))
    morning_late_minutes = db.Column(db.Integer, default=0)
    afternoon_late_minutes = db.Column(db.Integer, default=0)
    morning_late_reason = db.Column(db.String(200))
    afternoon_late_reason = db.Column(db.String(200))
    early_leave = db.Column(db.Boolean, default=False)
    morning_shift = db.Column(db.Boolean, default=False)
    afternoon_shift = db.Column(db.Boolean, default=False)
    image_proof = db.Column(db.String(120))
    location = db.Column(db.String(120))
    user = db.relationship('User', backref='attendances')

class SupplementaryAttendance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    shift = db.Column(db.String(20), nullable=False)  # 'morning' or 'afternoon'
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    hours = db.Column(db.Float, nullable=False)
    reason = db.Column(db.String(200))
    image_proof = db.Column(db.String(120))
    status = db.Column(db.String(20), default='pending')  # 'pending', 'approved', 'rejected'
    admin_response = db.Column(db.String(200))  # Lý do phản hồi của admin
    user = db.relationship('User', backref='supplementary_attendances')

class LeaveRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    shift = db.Column(db.String(20), nullable=False)  # 'morning', 'afternoon', 'full'
    reason = db.Column(db.String(200))
    status = db.Column(db.String(20), default='pending')  # 'pending', 'approved', 'rejected'
    user = db.relationship('User', backref='leave_requests')

class ShiftConfig(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    morning_start = db.Column(db.Time, default='07:30:00')
    morning_end = db.Column(db.Time, default='11:30:00')
    afternoon_min = db.Column(db.Time, default='13:00:00')
    afternoon_max = db.Column(db.Time, default='23:59:00')
    afternoon_hours = db.Column(db.Integer, default=4)

class ShareToken(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(36), unique=True, nullable=False)  # UUID
    month = db.Column(db.Integer, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    period = db.Column(db.String(20), default='month')  # 'month', 'week', ...
    expiration_time = db.Column(db.DateTime, nullable=False)

    created_at = db.Column(db.DateTime, default=db.func.now())
