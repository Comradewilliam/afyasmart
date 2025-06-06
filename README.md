# 🏥 AfyaSmart – Digital Health Assistant for Tanzania

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Backend: Flask](https://img.shields.io/badge/Backend-Flask-blue?logo=python)](https://flask.palletsprojects.com/)
[![Frontend: React + TS](https://img.shields.io/badge/Frontend-React%20%7C%20TypeScript-61DAFB?logo=react)](https://react.dev/)
[![API: Africa's Talking](https://img.shields.io/badge/API-Africa's%20Talking-orange)](https://africastalking.com/)
[![AI: Gemini](https://img.shields.io/badge/AI-Gemini%20AI-brightgreen)](https://cloud.google.com/ai/gemini)

> **AfyaSmart** is a multilingual, AI-powered digital health assistant designed for Tanzania. It delivers fast, localized first aid responses, hospital lookup via USSD, and intelligent health conversations via SMS and voice — all powered by **Africa’s Talking** and **Gemini AI**.

---

## ✨ Key Features

* 🧠 **AI First Aid Assistant**
  Instant guidance via SMS and voice (Gemini-powered).
* 📍 **Hospital Finder**
  Interactive USSD-based navigation by region and district.
* 📤 **Bulk SMS Delivery**
  Automated info dispatch for hospitals and updates.
* 🌍 **Multilingual Support**
  Fully functional in **English** and **Swahili**.
* 📀 **MySQL-Backed Data**
  Stores hospitals, users, logs, and interaction data.

---

## 🧱 Tech Stack

| Layer                 | Technology                               |
| --------------------- | ---------------------------------------- |
| **Backend**           | Flask (Python)                           |
| **AI Engine**         | Gemini AI (Google Cloud)                 |
| **Communication**     | Africa's Talking (SMS, Voice, USSD)      |
| **Database**          | MySQL                                    |
| **Frontend (Web)**    | React • TypeScript • Vite • Tailwind CSS |
| **Frontend (Mobile)** | Java (Android)                           |

---

## 📁 Project Structure

```
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

## ⚡ Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/Comradewilliam/afyasmart.git
cd afyasmart
```

### 2. Setup Virtual Environment

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Environment Configuration

Create a `.env` file:

```env
AT_USERNAME=your_africas_talking_username
AT_API_KEY=your_africas_talking_apikey
AT_SHORTCODE=your_sms_shortcode
AT_VOICE_NUMBER=your_voice_number
GEMINI_API_KEY=your_gemini_api_key
DATABASE_URI=mysql+mysqlconnector://user:password@host/dbname
```

### 5. Initialize MySQL Database

```sql
CREATE DATABASE afyasmart;
-- Then use models.py to create your tables
```

### 6. Launch the Server

```bash
python app.py
```

---

## 🔌 API Endpoints

| Method | Endpoint | Purpose                       |
| ------ | -------- | ----------------------------- |
| POST   | `/sms`   | First aid assistant via SMS   |
| POST   | `/ussd`  | Hospital finder via USSD      |
| POST   | `/voice` | Health support via voice + AI |

---

## 🤖 Gemini AI Example

```python
def ask_ai(prompt):
    response = requests.post("https://gemini.googleapis.com/v1/chat", ...)
    return response.json().get("response", "Sorry, I didn't get that.")
```

---

## 🌐 Language Support

* Handled via `languages.py`
* Automatically selects based on user data
* English 🇬🇪 and Swahili 🇹🇼 supported

---

## 🧪 Testing the API

Use **Postman** or similar to test:

* `/sms` → `text`, `from`
* `/ussd` → `text`, `sessionId`, `phoneNumber`
* `/voice` → `transcriptionText`

---

## 📈 Roadmap

* [ ] Admin dashboard with analytics
* [ ] OAuth or SMS OTP verification
* [ ] Google Maps-based hospital geolocation
* [ ] Usage monitoring + reporting tools

---

## 👤 Author

**William Sadiki**
*📍 Tanzania
*💻 Flask • React • AI • Health Tech
*🔗 [GitHub Profile](https://github.com/Comradewilliam)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).
*Designed for health tech solutions and educational use in Tanzania.*

---

> *Empowering Tanzanians through accessible, AI-powered healthcare — anytime, anywhere.*
