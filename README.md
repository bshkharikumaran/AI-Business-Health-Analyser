# Vyapaar Pulse — AI Business Health Copilot & Autonomous Multilingual Voice Assistant

**Vyapaar Pulse** is an enterprise-grade AI decision-support system and business health analyzer built for MSMEs (Micro, Small, and Medium Enterprises). It integrates **autonomous multilingual NLP voice assistance**, a **3D spatial animated UI with Three.js**, **in-depth business analytics & scenario simulations**, and **Firebase database synchronization with live data feeding**.

---

## 📁 Complete Folder Structure

```
msme-prototype-2 3/
├── app.py                  # Flask web server, REST API endpoints, voice executors
├── logic.py                # Business intelligence algorithms, forecasting, scenario simulations, ABC-XYZ, sentiment
├── voice_assistant.py      # Autonomous multilingual Gemini NLP agent + offline multi-language fallback
├── db.py                   # Firebase Firestore / Realtime DB persistence layer + local JSON fallback
├── requirements.txt        # Python dependencies (Flask, numpy, vaderSentiment, google-genai, firebase-admin)
├── README.md               # Project documentation and user guide
├── test_verification.py    # Automated test suite for backend, NLP, and database operations
├── data/
│   ├── schemes.json        # Government MSME schemes and subsidy eligibility criteria
│   └── database.json       # (Auto-generated) Local persistent database file
├── templates/
│   └── index.html          # Modern 3D spatial dashboard shell with Three.js 3D Voice Orb HUD
└── static/
    ├── app.js              # Three.js 3D particle visualizer, Web Speech STT/TTS, Chart.js graphs, UI logic
    └── style.css           # 3D spatial glassmorphic styling, parallax animations, responsive layout
```

---

## 🌟 Key Features

### 1. 🌐 Autonomous Multilingual NLP Voice Assistant
* **Omnilingual Speech & Text**: Understands speech and text across **every known language** (Tamil, Hindi, Telugu, Kannada, Bengali, Marathi, Gujarati, Spanish, French, German, Japanese, Arabic, English, Hinglish, Tanglish, etc.).
* **Language-Matched Output**: Automatically detects the user's input language and crafts its response **in the exact same language and script/dialect**.
* **Localized Speech Synthesis (TTS)**: Automatically pairs the detected language code (`ta-IN`, `hi-IN`, `te-IN`, `es-ES`, etc.) with native browser speech synthesis voices.
* **Autonomous Decision-Making**: Automatically chooses and executes multi-step business actions:
  * Sales & festival surge simulations
  * Stock checks, reorders, and inventory parameter adjustments
  * Aspect-based customer sentiment analysis
  * Automated WhatsApp alerts dispatch
  * Subsidy calculations & localized marketing broadcast copywriting
* **Resilient Offline Fallback**: Dual-path engine that falls back to embedded multi-language keyword/regex parsers if offline or without an API key.

### 2. 🎨 3D Animated Spatial UI Theme & Three.js Visualizer Orb
* **Three.js WebGL 3D Voice Orb**: An interactive 3D particle sphere embedded in the voice controller that animates dynamically across states:
  * 🔵 **Idle**: Gentle breathing and rotation with cyan/gold emission.
  * 🔴 **Listening**: Rapid neon pink/red vertex pulsation with ripple waves.
  * 🟡 **Thinking**: Swirling multi-axis particle vortex.
  * 🟢 **Speaking**: Harmonic sine wave oscillations matching speech audio frequencies.
* **3D Card Parallax Tilt**: Interactive mouse-tracking physics on dashboard cards (`perspective: 1200px`, `transform-style: preserve-3d`).
* **Glassmorphic Spatial UI**: Translucent layered cards, ambient background glows, animated chart entrances, and micro-interactions.

### 3. 📊 High-Level Business Analytics & Decision Suite
* **Executive 5-Pillar Health Score**:
  1. *Revenue Velocity & Growth Trend* (25%)
  2. *Stock Availability & Reorder Prevention* (25%)
  3. *Customer Satisfaction & NPS* (20%)
  4. *Working Capital Efficiency* (15%)
  5. *Subsidy & Udyam Readiness* (15%)
* **Interactive "What-If" Sales Scenario Simulator**: Real-time sliders for WhatsApp Promo Boost, Festival Multipliers, Discount Elasticity, and Inflation with upper/lower confidence bands.
* **Smart Inventory ABC-XYZ Matrix & EOQ**: Value-based classification, demand volatility, stockout risk percentages, and Economic Order Quantity optimizer.
* **Aspect-Based Multilingual Sentiment Intelligence**: Evaluates customer reviews across 5 key dimensions: *Product Quality, Delivery Speed, Packaging, Pricing, and Staff Support*.
* **Government Subsidy Calculator & Multilingual WhatsApp Copywriter**: Calculates exact ₹ subsidy benefits and generates localized promotional broadcasts in Tamil, Hindi, Telugu, English, Spanish, and French.

### 4. 🗄️ Firebase Database Persistence & Live Data Feeding Center
* **Dual-Engine Persistence Layer ([`db.py`](file:///Users/sanjay/Downloads/msme-prototype-2%203/db.py))**:
  * Cloud sync with **Firebase Firestore / Realtime DB** (via `firebase-credentials.json` or env variables).
  * Automatic zero-config fallback to **persistent local JSON storage** (`data/database.json`).
* **Data Feeding & Ingestion Hub**:
  * Dedicated **Data Feeding & Ingestion Center** in the UI.
  * Batch CSV/JSON ingestion for Sales History, Inventory Catalogs, and Customer Feedback with live model recalculation.

---

## 🚀 Quick Start Guide

### 1. Install Dependencies
```bash
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
```

### 2. (Optional) Set Environment Variables
```bash
# To enable autonomous Gemini reasoning:
export GEMINI_API_KEY="your-gemini-api-key"

# (Optional) To connect Firebase Firestore:
export FIREBASE_CREDENTIALS="/path/to/firebase-credentials.json"
```

### 3. Start the Server
```bash
python app.py
```
Open **`http://127.0.0.1:5001`** in your browser (preferably Google Chrome or Microsoft Edge for optimal Web Speech STT/TTS support).
