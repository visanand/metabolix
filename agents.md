# Agents Configuration for AarogyaAI

This `agents.md` file documents the configuration of agents used in the **AarogyaAI** project, compliant with Codex guidelines. Agents here refer to logic components or API-backed services responsible for distinct tasks in the chatbot system.

---

## 🤖 Agent: ChatGPT (AI Reasoning Agent)
**Purpose:** Provides symptom triage, general wellness suggestions, and conversational flows.

- **Type**: LLM-based reasoning agent
- **Model**: OpenAI GPT-4 (ChatGPT)
- **Scope**:
  - Symptom interpretation
  - Triage classification (low-risk vs red-flag)
  - Health education responses
  - Lifestyle/diet guidance
  - Supplement suggestions (non-medical)
- **Limitations:**
  - Cannot prescribe medications
  - Does not replace clinical decision-making

---

## 🩺 Agent: RMP Escalation Handler
**Purpose:** Interfaces between chatbot and registered medical practitioners for real-time teleconsults.

- **Type**: Rule-based + API call handler
- **Triggers:**
  - Red flag detection in chat
  - User requests doctor consult
- **Workflow:**
  1. Summarize chat history using GPT-4
  2. Store structured summary in MongoDB
  3. Trigger payment flow (Razorpay)
  4. Notify RMP for consult scheduling

---

## 💰 Agent: Payment Handler (Razorpay)
**Purpose:** Facilitates payment link generation and tracking for doctor consults.

- **Type**: API integration agent
- **Provider**: Razorpay
- **Consult Types:**
  - WhatsApp/Audio → ₹99
  - Video (15 mins) → ₹249
- **Outputs:**
  - Razorpay link URL
  - Payment status webhook handling
- **Security:** Uses key/secret securely stored in environment variables

---

## 🧠 Agent: Input Validator
**Purpose:** Validates user-provided inputs (e.g., name, age, location).

- **Type**: Rule-based validator
- **Checks:**
  - Name (non-empty)
  - Age (integer, 1–120)
  - PIN code (6-digit)
  - Gender (M/F/O)
- **Fallback:** Prompts user again for invalid input

---

## 🗃️ Agent: Data Persistence Agent
**Purpose:** Stores and retrieves user sessions, chat history, and medical summaries.

- **Type**: Database agent
- **Backend**: MongoDB Atlas
- **Functions:**
  - Save user profile
  - Save consent logs
  - Store and retrieve chat transcripts
  - Tag consults as pending/completed
- **Compliance:** Adheres to DPDP Act (India) for personal data protection

---

## 🔄 Future Agents (Planned)
| Agent Name        | Description                                |
|------------------|--------------------------------------------|
| Voice-to-Text     | Accept voice input via IVR or WhatsApp     |
| Language Localizer| Detect & auto-translate user language      |
| Analytics Tracker | Monitor usage, conversion, consult metrics |

---

**Note:** All agents operate under the principle of "assistive AI only" — final clinical decisions rest with licensed human doctors.
