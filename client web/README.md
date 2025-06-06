# 🏥 AfyaSmart
**Digital Health Assistant for Tanzania**

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Backend-Flask-blue?logo=python)](https://flask.palletsprojects.com/)
[![Frontend](https://img.shields.io/badge/Frontend-React%20%7C%20TypeScript-blue?logo=react)](https://react.dev/)
[![Africa's Talking](https://img.shields.io/badge/API-Africa's%20Talking-orange)](https://africastalking.com/)
[![Gemini AI](https://img.shields.io/badge/AI-Gemini%20AI-brightgreen)](https://cloud.google.com/ai/gemini)

> **AfyaSmart** is a digital health assistant built for Tanzanians, integrating **Africa’s Talking APIs** (SMS, USSD, Voice) and **Gemini AI** to deliver reliable first aid, hospital info, and intelligent voice-based health guidance—accessible in both English and Swahili.

---

## ✨ Features

- 🧠 **AI First Aid Assistant**  
  Get guidance via SMS and Voice (powered by Gemini AI)
- 📍 **Hospital Finder**  
  USSD flow to browse hospitals by zone, region, and district
- 📤 **Bulk SMS Delivery**  
  Sends relevant hospital info via SMS
- 🌍 **Multilingual**  
  Supports **English** & **Swahili**
- 💾 **MySQL Integration**  
  Stores hospitals, users, and logs

---

## 🛠️ Technology Stack

| Layer           | Technology                |
|-----------------|--------------------------|
| Backend         | Flask (Python)           |
| AI Engine       | Gemini AI (Google Cloud) |
| Communication   | Africa's Talking APIs    |
| Database        | MySQL                    |
| Frontend (Web)  | React, TypeScript, Vite, Tailwind CSS |
| Frontend (Mobile) | Java (Android)         |

---

## 📂 Project Structure

```text
afyasmart/
├── app.py
├── config.py
├── db.py
├── models.py
├── ai_utils.py
├── sms_routes.py
├── ussd_routes.py
├── voice_routes.py
├── languages.py
├── requirements.txt
├── .env
└── README.md
```

---

## ⚡ Quickstart

### 1. Clone the Repository

```bash
git clone https://github.com/Comradewilliam/afyasmart.git
cd afyasmart
```

### 2. Create a Python Virtual Environment

```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On Unix/Mac:
source venv/bin/activate
```

### 3. Install Backend Requirements

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root:

```env
AT_USERNAME=your_africas_talking_username
AT_API_KEY=your_africas_talking_apikey
AT_SHORTCODE=your_sms_shortcode
AT_VOICE_NUMBER=your_voice_number
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URI=mysql+mysqlconnector://user:password@host/dbname
```

### 5. Setup MySQL Database

```sql
CREATE DATABASE afyasmart;
-- Then run schema from /models.py or setup script
```

### 6. Run the Flask Server

```bash
python app.py
```

---

## 🔗 API Endpoints

| Method | Endpoint  | Description                    |
|--------|-----------|--------------------------------|
| POST   | `/sms`    | Handles SMS first aid chat     |
| POST   | `/ussd`   | USSD hospital lookup           |
| POST   | `/voice`  | AI-based voice health guidance |

---

## 🤖 Gemini AI Integration

You must have access to Google Cloud’s Gemini API for intelligent health responses.

**Sample Integration:**
```python
def ask_ai(prompt):
    response = requests.post("https://gemini.googleapis.com/v1/chat", ...)
    return response.json().get("response", "Sorry, I didn't get that.")
```

---

## 🌐 Multilingual Support

- English and Swahili prompts via `languages.py`
- Automatically selects language based on user region or preference

---

## 🧪 Testing

- Use **Postman** or similar tools to test endpoints:
  - `/sms` with `text` and `from`
  - `/ussd` with `text`, `sessionId`, and `phoneNumber`
  - `/voice` with `transcriptionText`

---

## 🚀 Future Improvements

- OAuth login or OTP verification
- Location-based hospital discovery (Google Maps)
- Admin dashboard for hospital management and analytics
- Usage reporting and statistics

---

## 👤 Developer

**Project:** AfyaSmart  
**Stack:** Flask • MySQL • Gemini AI • Africa's Talking APIs  
**Country Focus:** 🇹🇿 Tanzania

---

## 📄 License

[MIT License](LICENSE) — Free for educational and health tech innovation purposes.

---

> **Empowering Tanzanians with accessible, AI-powered health support.**
