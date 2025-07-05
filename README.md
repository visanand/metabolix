# Metabolix Chatbot

**Metabolix Chatbot** is an AI-powered assistant for [mymetabolix.com](https://www.mymetabolix.com). It answers questions about weight-loss products, helps users book appointments, accepts product orders and notifies the admin on WhatsApp.

---

## 🔧 Tech Stack
- **Backend**: FastAPI
- **AI Engine**: OpenAI GPT-4 API (ChatGPT)
- **Database**: MongoDB Atlas
- **Session Store**: Redis
- **Hosting**: Render
- **Payments**: Razorpay (₹99 for audio/WhatsApp, ₹249 for video consult)

---

## 🚀 Features
- Conversational product FAQs and weight-loss guidance using GPT-4
- Appointment booking with optional payment links
- Product order capture with WhatsApp alerts to admin
- MongoDB-based storage of chats, orders and appointments
- Multilingual support

---

## 🛠️ Getting Started

### 1. Clone the repo
```bash
git clone https://github.com/yourusername/metabolix-chatbot.git
cd metabolix-chatbot
```

### 2. Setup environment variables
Create a `.env` file with the following:
```env
OPENAI_API_KEY=your_openai_key
MONGODB_URI=your_mongodb_connection_string
MONGODB_ALLOW_INVALID_CERTS=false
RAZORPAY_KEY_ID=your_key_id
RAZORPAY_KEY_SECRET=your_key_secret
REDIS_URL=redis://redis-17168.crce206.ap-south-1-1.ec2.redns.redis-cloud.com:17168
BOT_NAME=MetabolixBot
ADMIN_PHONE=+919810519452
RAZORPAY_WEBHOOK_SECRET=your_webhook_secret
LOG_LEVEL=INFO
PORT=8000
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_WHATSAPP_NUMBER=14155238886
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the API server
```bash
uvicorn main:app --reload
```

### 5. Run tests
```bash
pytest
```

---

## 💬 Chatbot Workflow
1. Greet user & get consent
2. Collect basic demographic info
3. Conduct symptom triage or lifestyle support
4. Provide AI-guided suggestions if low-risk
5. Escalate to RMP for red flags
6. Generate Razorpay link for ₹99/₹249 consult
7. Summarize chat and save to MongoDB
8. Allow doctor review before consult

---

## 📦 Folder Structure
```
/metabolix-chatbot
│
├── main.py               # FastAPI app
├── chat_engine.py        # GPT-4 logic integration
├── db.py                 # MongoDB functions
├── routes.py             # API endpoints
├── schemas.py            # Pydantic models
├── utils.py              # Input validation, summaries
├── razorpay_utils.py     # Payment integration
├── .env.example          # Example environment file
├── requirements.txt      # Python dependencies
└── README.md             # Project overview
```

---

## 🛡️ Compliance & Security
- Follows **Telemedicine Practice Guidelines 2020**
- Compliant with **DPDP Act 2023** (India)
- No AI-based prescribing — only RMPs prescribe
- Explicit user consent required before data capture

---

## 🙌 Credits
Built with ❤️ to serve India's growing need for accessible, digital-first healthcare.

---

## 📫 Contact / Collaboration
Interested in contributing, testing, or partnering?
Email us at [support@mymetabolix.com](mailto:support@mymetabolix.com)

---

## 📜 Prompt Specification
For the complete design prompt guiding Metabolix Chatbot's features and compliance goals, see [PROMPT.md](PROMPT.md).

---

## 🏁 License
This project is licensed under the [MIT License](LICENSE).
