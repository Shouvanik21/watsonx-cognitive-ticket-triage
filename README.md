# ⚡ IBM Watsonx Cognitive Ticket Triage & Process Automation Engine

A full-stack Cognitive Process Automation engine built with **Node.js, Express.js, and Python**, leveraging **IBM Watsonx.ai (Granite-13b Foundation Model)** for intelligent ticket classification, urgency evaluation, sentiment analysis, and agent-assist response generation.

This project demonstrates how to bridge natural language AI processing with backend web microservices to build scalable, cognitive process automation workflows for enterprise customer support systems.

---

## 🚀 Features

### ⚡ Cognitive Ticket Triage & Analytics

The engine automatically ingests unstructured support ticket text and extracts structured intelligence metrics:

- **Category Classification** (Billing, Technical Bug, Account Access, General Query)
- **Urgency Scoring** (Integer scale from 1 to 5)
- **Sentiment Extraction** (Frustrated, Neutral, Positive)
- **Recommended Operational Action** (Escalate to Human Agent, Auto-Resolve, Queue for Technical Review)
- **Agent-Assist Response Generation** (Auto-drafts tailored customer responses)

### 🛡️ Resilient Dual-Mode Execution

- **Live AI Engine**: Queries the `ibm/granite-13b-chat-v2` model via Python foundation model SDKs.
- **Offline Rule-Based Fallback**: Automatically activates keyword analysis fallback if API keys are absent, network errors occur, or credit limits are reached, maintaining 100% application uptime.

### 📜 Operational Audit Logging

- Appends real-time, ISO-timestamped transactional audit records directly to an operational CSV file (`data/audit_log.csv`).
- Provides a dedicated REST endpoint to fetch and view recent system activity logs in tabular format.

---

## 🔄 API Operations

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/triage` | Submit raw support ticket text for AI analysis and auto-reply drafting |
| `GET` | `/api/logs` | Retrieve the last 10 operational audit records from the system log |

---

## 🛠️ Tech Stack

### Backend & Orchestration

- **Node.js**
- **Express.js** (REST API Microservices & Static Web Server)
- **Python 3** (AI Sub-process Execution Engine)

### AI & Cognitive Processing

- **IBM Watsonx.ai Foundation Models** (`ibm/granite-13b-chat-v2`)
- **IBM Watsonx Python SDK** (`ibm-watsonx-ai`)

### Frontend

- **HTML5 / CSS3 / Modern JavaScript (ES6)** (Single-page dashboard)

### Development & Utilities

- **dotenv** (Environment variable management)
- **csv-parser** (CSV data parsing)
- **VS Code**

---

## 📁 Project Structure

```text
watsonx-cognitive-ticket-triage/
│
├── data/
│   └── audit_log.csv         # Timestamped process audit database
│
│── index.html                # Dashboard UI (HTML/CSS/JS)
├── .env                      # API keys & environment configuration
├── .gitignore                # Git exclusion rules
├── package.json              # Node.js dependencies and scripts
├── package-lock.json
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── server.js                 # Express server & sub-process manager
└── watsonx_engine.py         # IBM Watsonx AI core script
```
---
## 🔄 System Architecture

```text
User Input (Browser)
       │
       ▼
Express.js Server (/api/triage)
       │
       ▼ (Child Process Spawn)
Python Engine (watsonx_engine.py)
       │
   ┌───┴────────────────────────┐
   ▼                            ▼
IBM Watsonx Granite LLM    Offline Fallback Engine
   └───┬────────────────────────┘
       │
       ▼ (JSON Extraction Output)
Express.js Server
   ├── Append to data/audit_log.csv
   └── Send JSON to Client Dashboard
   ```
   ---
   ## 📌 API Endpoints
   ### 1. Triage Ticket
   
   ```
   POST /api/triage
   ```
   ### Request Body:
```
JSON
{
  "ticket_text": "URGENT: I was double charged $150 on my invoice yesterday and I cannot log into my portal!"
}
```
### Response Example:
```
JSON
{
  "category": "Billing",
  "urgency_score": 4,
  "sentiment": "Frustrated",
  "recommended_action": "Escalate to Human Agent",
  "drafted_response": "We have received your billing inquiry and routed it to our finance team for immediate verification."
}
```
### 2. Fetch Audit Logs
```
HTTP
GET /api/logs
```
### Response Example:
```
JSON
[
  {
    "timestamp": "2026-09-30 17:30:00",
    "ticket_text": "URGENT: I was double charged $150...",
    "category": "Billing",
    "urgency": "4",
    "sentiment": "Frustrated",
    "action": "Escalate to Human Agent"
  }
]
```
### 🔐 Environment Variables

Create a .env file in the project root directory:

```
Code snippet
PORT=5000
WATSONX_APIKEY=your_ibm_cloud_api_key_here
WATSONX_PROJECT_ID=your_watsonx_project_id_here
WATSONX_URL=[https://us-south.ml.cloud.ibm.com](https://us-south.ml.cloud.ibm.com)
```

Note: If ```WATSONX_APIKEY``` or ```WATSONX_PROJECT_ID``` are omitted or left blank, the system automatically runs in Mock Fallback Mode, allowing full end-to-end functionality without API credentials.

## ⚙️ Installation & Setup
### 1. Clone the repository
```bash
git clone https://github.com/Shouvanik21/watsonx-cognitive-ticket-triage.git
```
### 2. Navigate into the project folder
```bash
cd watsonx-cognitive-ticket-triage
```
### 3. Install Node.js dependencies
```bash
npm install
```
### 4. Install Python dependencies
```bash
pip install -r requirements.txt
```
### 5. Configure environment variables
```bash
Create your .env file.
```

### 6. Start the server
```bash
npm start
```

For development mode (with auto-reload using nodemon):

```bash
npm run dev
```

Open your browser and navigate to:

```text
http://localhost:5000
```

## 📚 What I Learned

Through building this project, I practiced and implemented:

- Building asynchronous RESTful API services with **Express.js**
- Interfacing Node.js backend services with Python scripts using child processes (`spawn`)
- Integrating **IBM Watsonx.ai** foundation model APIs (`ibm/granite-13b-chat-v2`)
- Structuring LLM prompts for deterministic **JSON data extraction**
- Building **resilient fallback systems** to handle API connectivity issues gracefully
- Managing structured transactional logs using **CSV file handling** in Node.js
- Designing lightweight, single-page web applications for real-time AI analytics
- Securing environment keys and configuring repository exclusions via `.gitignore`

## 🎯 Project Purpose

This project was engineered to demonstrate a practical implementation of **Cognitive Process Automation (CPA)** in modern software engineering. It showcases how enterprise Large Language Models (LLMs) can be integrated into traditional REST microservices to automate data triage, improve operational response times, and provide real-time agent-assist capabilities.