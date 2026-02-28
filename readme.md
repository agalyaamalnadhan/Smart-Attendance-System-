# 🤖 AI Attendance Dashboard

A web-based AI Smart Attendance System using OpenCV face recognition.  
The system detects faces through a webcam and automatically stores attendance in an Excel file via a live dashboard.

---

## 🚀 Features

- Real-time face recognition
- Web dashboard interface (Flask)
- Start / End attendance control
- Staff & subject selection
- Automatic Excel logging
- Live camera streaming

---

## 🛠 Requirements

- Python 3.11
- Webcam
- Required libraries (see requirements.txt)

Install dependencies:

pip install -r requirements.txt

---

## 📂 Project Structure

attendance_system.py  
app.py  
templates/index.html  
static/favicon.png  
attendence_excel.xls  
requirements.txt  

⚠️ Keep the Excel file closed before running.

---

## ▶️ How to Run (Web Dashboard)

1. Open terminal in project folder

2. (Optional) Create virtual environment

python -m venv venv  
venv\Scripts\activate  

3. Install packages

pip install -r requirements.txt

4. Run the web app

python app.py

5. Open browser:

http://127.0.0.1:5000

---

## 🎥 How It Works

- Select timetable slot
- Click **Start Attendance**
- Faces detected automatically
- Attendance saved to Excel
- Click **End Attendance** to stop

If staff changes, attendance automatically switches to **Stopped**.

---

## 📊 Output

Attendance records are stored in:

attendence_excel.xls

---

## 🧠 Technologies Used

- Python
- OpenCV
- Flask
- NumPy
- Excel (xlrd, xlutils)

---
