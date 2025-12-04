# ITMeet Backend (FastAPI)

A lightweight FastAPI backend providing two core features for the ITMeet website:

## Features

### 1. Google Apps Script Proxy  
Handles forwarding email submissions from the frontend to a secured Google Apps Script URL.  
The Apps Script is responsible for storing the submitted data in a Google Spreadsheet.

### 2. AI Chatbot Endpoint  
Provides an API endpoint for an AI-powered FAQ chatbot.  
This is used in the ITMeet website to automatically answer common visitor questions.

## Tech Stack
- **FastAPI** for backend REST API  
- **Python**  
- **Google Apps Script** (for spreadsheet storage)  
- **Gemini API** (for FAQ responses)

