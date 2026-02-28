import cv2
import numpy as np
import urllib.request
import os
from datetime import datetime
import xlrd
import xlwt
from xlutils.copy import copy as xl_copy

# ==============================
# GLOBAL VARIABLES
# ==============================
attendance_active = False
CURRENT_SUBJECT = "NotSet"
CURRENT_MAM = "NotSet"

marked_students = {}
present_count = 0

excel_file = "attendence_excel.xls"

print("🔄 Loading face detection...")

# ==============================
# FACE CASCADE DOWNLOAD
# ==============================
cascade_path = "haarcascade_frontalface_default.xml"

if not os.path.exists(cascade_path):
    print("📥 Downloading cascade file...")
    urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/opencv/opencv/master/data/haarcascades/haarcascade_frontalface_default.xml",
        cascade_path
    )

face_cascade = cv2.CascadeClassifier(cascade_path)

# ==============================
# CREATE EXCEL FILE IF MISSING
# ==============================
def create_excel():
    wb = xlwt.Workbook()
    sheet = wb.add_sheet("Attendance")

    headers = ["Name", "Date", "Time", "Subject", "Staff", "Status"]
    for col, header in enumerate(headers):
        sheet.write(0, col, header)

    wb.save(excel_file)
    print("📄 Excel file created")

if not os.path.exists(excel_file):
    create_excel()

# ==============================
# STUDENT LABELS
# ==============================
labels = {"Agalya": 0, "Christena": 1, "Pugazhmathy": 2, "Pushpa Lakshmi": 3}
faces = []
ids = []

print("🧠 Training faces...")

for name, label in labels.items():
    img_path = f"{name}.png"

    if os.path.exists(img_path):
        img = cv2.imread(img_path)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        detected = face_cascade.detectMultiScale(gray, 1.3, 5)

        for (x, y, w, h) in detected:
            face_img = gray[y:y+h, x:x+w]
            face_img = cv2.resize(face_img, (200, 200))
            faces.append(face_img)
            ids.append(label)

        print(f"✅ {name} trained")
    else:
        print(f"⚠️ {img_path} missing")

if len(faces) == 0:
    print("❌ No training images found!")
    exit()

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.train(faces, np.array(ids))

print("🎯 Training complete!")
print("✅ attendance_system READY!")

# ==============================
# RESET SESSION
# ==============================
def reset_session():
    global present_count, marked_students
    present_count = 0
    marked_students = {}
    print("🔄 Attendance Session Reset")

# ==============================
# SET SUBJECT
# ==============================
def set_subject(subject, mam):
    global CURRENT_SUBJECT, CURRENT_MAM

    if CURRENT_SUBJECT != subject:
        reset_session()

    CURRENT_SUBJECT = subject
    CURRENT_MAM = mam

    print(f"📘 {subject} - {mam}")

# ==============================
# SAVE ATTENDANCE
# ==============================
def save_attendance(name):
    global present_count, marked_students

    # Prevent duplicate marking in same session
    if name in marked_students:
        return False

    now = datetime.now()
    today = now.strftime("%d-%m-%Y")
    time_now = now.strftime("%H:%M:%S")  # Full time with seconds

    try:
        rb = xlrd.open_workbook(excel_file, formatting_info=True)
        read_sheet = rb.sheet_by_index(0)
        row = read_sheet.nrows

        wb = xl_copy(rb)
        sheet = wb.get_sheet(1)

        sheet.write(row, 0, name)
        sheet.write(row, 1, today)
        sheet.write(row, 2, time_now)
        sheet.write(row, 3, CURRENT_SUBJECT)
        sheet.write(row, 4, CURRENT_MAM)
        sheet.write(row, 5, "Present")

        wb.save(excel_file)

        marked_students[name] = True
        present_count += 1

        print(f"✅ {name} marked at {time_now}! Total: {present_count}")
        return True

    except Exception as e:
        print("❌ Excel error:", e)
        return False

# ==============================
# PROCESS FRAME
# ==============================
def process_frame(frame):
    global attendance_active

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces_detected = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces_detected:
        face_img = gray[y:y+h, x:x+w]
        face_img = cv2.resize(face_img, (200, 200))

        label, conf = recognizer.predict(face_img)
        name = "Unknown"

        for n, l in labels.items():
            if l == label and conf < 70:
                name = n
                break

        if name != "Unknown" and attendance_active and CURRENT_SUBJECT != "NotSet":
            save_attendance(name)

        color = (0, 0, 255) if name in marked_students else (0, 255, 0)

        cv2.rectangle(frame, (x, y), (x+w, y+h), color, 2)
        cv2.putText(frame, f"{name} ({100-conf:.0f}%)",
                    (x, y-10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    color,
                    2)

    status = "ON" if attendance_active else "OFF"

    cv2.putText(frame,
                f"Present: {present_count} | {status} | {CURRENT_SUBJECT}",
                (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (255, 255, 255),
                2)

    return frame
