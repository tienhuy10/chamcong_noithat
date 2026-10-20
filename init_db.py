from flask import Flask
from datetime import datetime, date, time
from models import db, User, Attendance, SupplementaryAttendance, LeaveRequest, ShiftConfig
import os

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

def create_users():
    users = [
        {'username': 'myhuyen', 'full_name': 'Mỹ Huyền', 'password': '123456', 'role': 'employee'},
        {'username': 'hongviet', 'full_name': 'Hồng Việt', 'password': '123456', 'role': 'employee'},
        {'username': 'hoainam', 'full_name': 'Hoài Nam', 'password': '123456', 'role': 'employee'},
        {'username': 'thuylinh', 'full_name': 'Thùy Linh', 'password': '123456', 'role': 'employee'},
        {'username': 'hoailam', 'full_name': 'Hoài Lâm', 'password': '123456', 'role': 'employee'},
        {'username': 'admin', 'full_name': 'Admin', 'password': 'Tipystem', 'role': 'admin'},
        {'username': 'tienhuy', 'full_name': 'Tien Huy', 'password': 'Tipystem', 'role': 'admin'},
    ]
    
    for user_data in users:
        if not User.query.filter_by(username=user_data['username']).first():
            user = User(
                username=user_data['username'],
                full_name=user_data['full_name'],
                role=user_data['role'],
                is_active=True
            )
            user.set_password(user_data['password'])
            db.session.add(user)
    db.session.commit()

def create_attendance():
    users = {
        'myhuyen': {'full_name': 'Mỹ Huyền', 'off_days': [date(2025, 8, 4), date(2025, 8, 12)]},
        'hongviet': {'full_name': 'Hồng Việt', 'off_days': [date(2025, 8, 14)], 'partial_off': [(date(2025, 8, 7), 'afternoon'), (date(2025, 8, 9), 'morning')]},
        'hoainam': {'full_name': 'Hoài Nam', 'off_days': [date(2025, 8, 6), date(2025, 8, 13)]},
        'thuylinh': {'full_name': 'Thùy Linh', 'off_days': [date(2025, 8, 7), date(2025, 8, 14)]},
        'hoailam': {'full_name': 'Hoài Lâm', 'off_days': [date(2025, 8, 14), date(2025, 8, 15)]},
    }
    
    morning_start = datetime.strptime('07:30:00', '%H:%M:%S').time()
    morning_end = datetime.strptime('11:30:00', '%H:%M:%S').time()
    afternoon_start = datetime.strptime('13:00:00', '%H:%M:%S').time()
    afternoon_end = datetime.strptime('17:00:00', '%H:%M:%S').time()
    
    for username, data in users.items():
        user = User.query.filter_by(username=username).first()
        if not user:
            continue
        
        for day in range(1, 19):  # From 1/8/2025 to 18/8/2025
            current_date = date(2025, 8, day)
            if current_date in data['off_days']:
                continue
                
            attendance = Attendance(
                user_id=user.id,
                date=current_date,
                morning_check_in=datetime.combine(current_date, morning_start),
                morning_check_out=datetime.combine(current_date, morning_end),
                afternoon_check_in=datetime.combine(current_date, afternoon_start),
                afternoon_check_out=datetime.combine(current_date, afternoon_end),
                morning_shift=True,
                afternoon_shift=True,
                morning_work_hours=4.0,
                afternoon_work_hours=4.0,
                work_hours=8.0
            )
            
            # Handle partial off days for Hồng Việt
            if 'partial_off' in data:
                for off_date, shift in data['partial_off']:
                    if current_date == off_date:
                        if shift == 'morning':
                            attendance.morning_check_in = None
                            attendance.morning_check_out = None
                            attendance.morning_shift = False
                            attendance.morning_work_hours = 0.0
                            attendance.work_hours = 4.0
                        elif shift == 'afternoon':
                            attendance.afternoon_check_in = None
                            attendance.afternoon_check_out = None
                            attendance.afternoon_shift = False
                            attendance.afternoon_work_hours = 0.0
                            attendance.work_hours = 4.0
            
            db.session.add(attendance)
    
    db.session.commit()

def create_shift_config():
    if not ShiftConfig.query.first():
        shift_config = ShiftConfig(
            morning_start=time(7, 30),
            morning_end=time(11, 30),
            afternoon_min=time(13, 0),
            afternoon_max=time(23, 59),
            afternoon_hours=4
        )
        db.session.add(shift_config)
        db.session.commit()

def init_db():
    with app.app_context():
        db.create_all()
        create_users()
        create_shift_config()
        create_attendance()

if __name__ == '__main__':
    init_db()