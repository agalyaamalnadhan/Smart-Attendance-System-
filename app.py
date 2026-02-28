from flask import Flask, render_template, Response, request, redirect
import cv2
import attendance_system as ats
import os

app = Flask(__name__)
camera = cv2.VideoCapture(0)

TIMETABLE = {
    "9AM": "AI - Lakshmi Mam",
    "10AM": "ML - Hema Mam",
    "11AM": "DL - Anitha Mam",
    "12PM": "Python - Rathina Mam",
    "1PM": "CB - Sowmiya Mam"
}

def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break

        frame = ats.process_frame(frame)
        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        slot = request.form.get('slot')

        if slot in TIMETABLE:
            subject_mam = TIMETABLE[slot]
            subject, mam = subject_mam.split(" - ")
            ats.set_subject(subject, mam)

            if action == 'start':
                ats.attendance_active = True
            elif action == 'end':
                ats.attendance_active = False

        return redirect('/')

    return render_template('index.html',
                           timetable=TIMETABLE,
                           active=ats.attendance_active,
                           subject=ats.CURRENT_SUBJECT,
                           count=ats.present_count)

@app.route('/video')
def video():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    os.makedirs('templates', exist_ok=True)
    print("🚀 Smart Attendance System Starting...")
    app.run(host='0.0.0.0', port=5000, debug=True)
