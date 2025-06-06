# AfyaSmart Backend Server

Flask-based backend server for AfyaSmart that provides health assistance through AI, hospital information, and emergency services via SMS, USSD, and Voice.

## Setup

1. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and configure your environment variables:
```bash
cp .env.example .env
```

4. Initialize the database:
```bash
python -c "from database import init_db; init_db()"
```

## API Endpoints

### AI Health Assistant

- `POST /api/ai/first-aid`
  - Get first aid guidance for specific conditions
  - Body: `{"condition": string, "language": "en"|"sw", "user_id": number?}`

- `POST /api/ai/health-advice`
  - Get general health advice
  - Body: `{"query": string, "language": "en"|"sw", "user_id": number?}`

- `GET /api/ai/conversation-history?user_id=<id>`
  - Get conversation history for a user

### Hospital Search

- `GET /api/hospitals`
  - List hospitals with optional filters
  - Query params: `zone`, `region`, `district`, `search`, `lat`, `lng`

- `GET /api/hospitals/<id>`
  - Get hospital details by ID

- `GET /api/hospitals/zones`
  - Get list of unique zones

- `GET /api/hospitals/regions?zone=<zone>`
  - Get list of regions, optionally filtered by zone

- `GET /api/hospitals/districts?region=<region>`
  - Get list of districts, optionally filtered by region

### SMS Services

- `POST /api/sms/send`
  - Send SMS to one or more recipients
  - Body: `{"phone_numbers": string[], "message": string}`

- `POST /api/sms/callback`
  - Webhook for SMS delivery reports

### USSD Service

- `POST /api/ussd/callback`
  - Handle USSD sessions
  - Form data: `sessionId`, `phoneNumber`, `text`

- `POST /api/ussd/hospitals`
  - Get hospitals list for USSD
  - Body: `{"zone"?: string, "region"?: string, "district"?: string}`

- `POST /api/ussd/hospital-details`
  - Get hospital details for USSD
  - Body: `{"hospital_id": number}`

### Voice Services

- `POST /api/voice/call`
  - Initiate a voice call
  - Body: `{"phone_number": string, "callback_url"?: string}`

- `POST /api/voice/callback`
  - Handle voice call events
  - Form data: `sessionId`, `callerNumber`, `direction`, `recordingUrl`

- `POST /api/voice/menu`
  - Handle DTMF input for voice menu
  - Form data: `dtmfDigits`

## Database Models

- `Hospital`: Healthcare facility information
- `User`: User profiles with phone numbers and language preferences
- `AIConversation`: AI chat history
- `SMSLog`: SMS delivery tracking

## Services

- Africa's Talking: SMS, USSD, and Voice integration
- Gemini AI: Health advice and first aid guidance
- Geopy: Distance calculations for hospital search
