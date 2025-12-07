# 🚀 ITMeet Backend (FastAPI)

A lightweight **FastAPI backend** powering the ITMeet website.
It provides two core services:

1. **Email Submission Proxy** → forwards data to a secured Google Apps Script endpoint
2. **AI Chatbot** → uses Gemini API to answer FAQs about ITMeet

This backend is simple, secure, and easy for contributors to install on any system.

## 📌 Features

### ✅ 1. Google Apps Script Proxy

Used by the frontend for form submissions.
The backend safely forwards user–submitted data to a private Apps Script URL, which then stores the data into a Google Spreadsheet.

### ✅ 2. AI Chatbot Endpoint

Powered by **Google Gemini**.
This API answers frequently asked questions about ITMeet using a custom prompt context.

## 🛠 Tech Stack

* **FastAPI** (Python framework)
* **Uvicorn** (ASGI server)
* **Google Gemini API** (google-generativeai)
* **Google Apps Script** (for spreadsheet storage)
* **dotenv** (secure environment variable handling)


## ⚙️ Installation & Setup

Follow these steps to run the backend on your system.

### 1️⃣ **Clone the repository**

git clone https://github.com/Adarsha16/itmeet_backend.git
cd itmeet_backend

### 2️⃣ **Create a virtual environment (REQUIRED)**

> ⚠️ Use **Python 3.12 or 3.13**
> (Google Gemini does **NOT** support Python 3.14 yet)

py -3.12 -m venv .venv
.\.venv\Scripts\activate   # Windows
# OR
source .venv/bin/activate  # Mac/Linux

### 3️⃣ **Install dependencies**

pip install -r requirements.txt

### 4️⃣ **Create your `.env` file**

Copy:

cp .env.example .env

Then fill in the variables:

GEMINI_API_KEY=your_gemini_api_key_here
APPS_SCRIPT_URL=https://script.google.com/macros/s/XXXXXX/exec

## ▶️ Running the Server

Start FastAPI locally:
cd src
uvicorn main:app --reload

Server will run at:
http://127.0.0.1:8000

Swagger Docs:
http://127.0.0.1:8000/docs

## 📡 API Endpoints

### 🔹 POST `/chat`

Send a user message to the Gemini-powered chatbot.

#### Request
{
  "message": "When is ITMeet happening?"
}

#### Response

{
  "reply": "IT Meet 2025 will be held at Kathmandu University..."
}
## 🔐 Environment Variables

| Variable                  | Description                          |
| --------------------------| ------------------------------------ |
| `GEMINI_API_KEY`          | Gemini API key from Google AI Studio |
| `APPS_SCRIPT_URL`         | Secured Google Apps Script URL       |