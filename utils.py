from datetime import datetime, timedelta, time
from models import ShiftConfig

def calculate_work(attendance):
    config = ShiftConfig.query.first()
    if not config:
        morning_start = time(7, 30)
        morning_end = time(11, 30)
        afternoon_min = time(13, 0)
        afternoon_max = time(23, 59)
        afternoon_hours = 4
    else:
        morning_start = config.morning_start
        morning_end = config.morning_end
        afternoon_min = config.afternoon_min
        afternoon_max = config.afternoon_max
        afternoon_hours = config.afternoon_hours

    attendance.morning_shift = False
    attendance.afternoon_shift = False
    attendance.work_hours = 0.0
    attendance.late = False
    attendance.late_minutes = 0
    attendance.early_leave = False

    # Tính giờ làm ca sáng
    if attendance.morning_check_in and attendance.morning_check_out:
        if attendance.morning_check_out > attendance.morning_check_in:
            attendance.morning_shift = True
            delta = attendance.morning_check_out - attendance.morning_check_in
            morning_hours = delta.total_seconds() / 3600
            attendance.work_hours += morning_hours
            print(f"Morning hours for {attendance.date}: {morning_hours}")  # Debug
            if attendance.morning_check_in.time() > time(7, 30):
                attendance.late = True
                late_delta = datetime.combine(datetime.today(), attendance.morning_check_in.time()) - datetime.combine(datetime.today(), time(7, 30))
                attendance.late_minutes += int(late_delta.total_seconds() / 60)

    # Tính giờ làm ca chiều
    if attendance.afternoon_check_in and attendance.afternoon_check_out:
        if attendance.afternoon_check_out > attendance.afternoon_check_in:
            attendance.afternoon_shift = True
            delta = attendance.afternoon_check_out - attendance.afternoon_check_in
            afternoon_hours = delta.total_seconds() / 3600
            attendance.work_hours += afternoon_hours
            print(f"Afternoon hours for {attendance.date}: {afternoon_hours}")  # Debug
            if delta < timedelta(hours=afternoon_hours):
                attendance.early_leave = True

    print(f"Total work_hours for {attendance.date}: {attendance.work_hours}")  # Debug
    shifts = sum([1 if attendance.morning_shift else 0, 1 if attendance.afternoon_shift else 0])
    return shifts * 0.5