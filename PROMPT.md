Prompt for Codex to develop a conversational AI assistant named **Metabolix Chatbot**.

Metabolix Chatbot helps users of mymetabolix.com learn about weight-loss programs and products. It can book appointments, collect orders and escalate to doctors as needed while following India's Telemedicine Practice Guidelines 2020 and DPDP Act.

This chatbot is built using Python (FastAPI backend), hosted on Render, connected to a MongoDB Atlas instance, and uses ChatGPT (GPT-4) API as the conversational engine.

=== OBJECTIVE ===
Build a secure, user-friendly WhatsApp-like chatbot interface that:
- Uses a conversational flow (not form-based)
- Performs basic symptom triage
- Gives wellness/supplement suggestions (AI-only scope)
- Connects to human RMPs when needed
- Saves data to MongoDB
- Summarizes chat for doctors
- Initiates Razorpay payment link for consultations

=== FEATURES ===

1. START CHAT FLOW:
Greet user → Ask for consent → Collect basic demographic info (name, age, gender, location)
Use conversational tone and confirm each input with natural follow-up.

2. TRIAGE:
Detect common symptoms using GPT-4 → Guide user using symptom checklists → AI gives general advice if low risk
If red flags found, escalate to RMP (doctor).

3. AI SERVICES (as per Healthcare Services Scope):
- General health education
- Nutrition & lifestyle guidance
- Mental wellness screening
- Supplement suggestions
- Triage and referral to specialist (via text)
AI will never diagnose or prescribe medications.

4. ESCALATION:
If medical consult needed:
- Offer video consult → Razorpay ₹499 payment link (15 min)

5. DATABASE INTEGRATION (MongoDB):
- Store user profile, chat history, symptoms, suggestions, consent, and timestamps
- On RMP escalation: summarize chat + export to structured format (e.g., JSON) and save to MongoDB with consult status
- Enable doctor to query past history via patient phone number

6. INPUT VALIDATION:
Use regex or NLP for basic validation (e.g., age must be number < 120, valid PIN code, name not empty)
Use fallback clarifying messages in case of ambiguous inputs

7. SECURITY & COMPLIANCE:
- Follow DPDP Act: store only necessary data with user consent
- Add opt-out and data erasure option
- Show privacy policy link at start

=== SAMPLE CONVERSATION SNIPPET ===
User: "Hello"
Bot: "Hi! 👋 Welcome to Metabolix. Can I share some health-related info with you? ✅ Type 'Yes' to continue. 🌐 https://www.mymetabolix.com"

User: "Yes"
Bot: "Great! Let’s begin. What’s your name?"
...
Bot: "Thanks, Ramesh. I’ll remember that. What health issue are you facing today?"

...
Bot: "From your answers, it seems you might be experiencing mild acidity. Here are some home tips. Would you like to speak with a doctor just to be safe?"

User: "Yes, video call."
Bot: "Got it. Please complete your ₹249 payment using this link: https://razorpay.com/pay/video249. Once done, I’ll connect you."

=== DEPLOYMENT ===
- Backend: FastAPI
- AI: OpenAI GPT-4 API
- Hosting: Render
- Database: MongoDB Atlas
- Payments: Razorpay links (WhatsApp/audio: ₹99; video: ₹249)

=== ADDITIONAL ===
- Include basic analytics (no. of users, triage outcomes, consults booked)
- Multilingual support with fallback to English (Hindi default)
- Support voice-to-text in future version

END PROMPT.
