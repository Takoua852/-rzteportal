# 🏥 Doctor Appointment API

A robust and secure RESTful API for managing medical consultations, built with **Django** and **Django REST Framework (DRF)**.

---

## 🚀 Overview

This platform facilitates the scheduling process between doctors and patients with a focus on data integrity and security.
- **Dual Profile System:** Distinct profiles for Doctors and Patients linked to Django's User model.
- **Smart Scheduling:** Built-in validation prevents double-booking for both parties.
- **Secure Access:** Row-level permissions ensure users only see and manage their own appointments.

---

## 🧱 Tech Stack

* **Framework:** Django 5.x & Django REST Framework
* **Database:** SQLite (Development)
* **Auth:** Token-based Authentication
* **Architecture:** Modular App Structure (Separation of Concerns)

---

## ⚙️ Installation & Setup

1. **Clone & Virtual Env**
   ```bash
   git clone https://github.com/Takoua852/-rzteportal
   cd doctor-booking-api
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate

## 🛠️ Dependencies & Database

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
---

## Run Server
```bash
python manage.py runserver

```
Access the API at: http://127.0.0.1:8000/api/

## 📡 API Endpoints

📅 Appointments

Method,Endpoint,Description
GET,/api/appointments/,List all appointments (filtered by user)
POST,/api/appointments/,Create a new appointment
GET,/api/appointments/{id}/,Retrieve detailed appointment info
PATCH,/api/appointments/{id}/,"Update title, description or date"
DELETE,/api/appointments/{id}/,Cancel/Delete an appointment

🧑‍⚕️ Doctors & 🧑 Patients

Method,Endpoint,Description
GET,/api/doctors/,List available doctors
GET,/api/doctors/{id}/,Doctor profile details
GET,/api/patients/{id}/,Patient profile details

## 🔒 Security & Validation Logic
Permissions
IsAuthenticated: All endpoints require a valid Token.

IsAppointmentOwner: A custom permission class ensures that only the doctor or the patient involved in an appointment can view or modify it.

Business Rules
Conflict Prevention: The API validates that neither the doctor nor the patient has another appointment at the requested time.

Database Integrity: A UniqueConstraint on the model level prevents duplicate entries (Doctor + Patient + Date).

Auto-Assignment: When creating an appointment, the API automatically links the logged-in user to their respective role (Doctor/Patient).

## 📁 Project Structure

├── core/                # Project configuration & settings
├── auth_app/            # User registration & token logic
├── doctors_app/         # Doctor models & profiles
├── patients_app/        # Patient models & profiles
└── appointments_app/    # Scheduling logic, validators & permissions
## 📌 Notes
Email is stored in the User model
Profile data is stored in Doctor/Patient models
Appointment ownership is enforced at API level

## 📝 License

This project is licensed under the MIT License.

All code in this repository was written independently as part of a learning project.