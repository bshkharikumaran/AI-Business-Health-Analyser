"""
Flask REST API End-to-End Test Suite for WhatsApp Alert Automation & Voice Assistant
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

def test_routes():
    client = app.test_client()

    print("=== Testing Flask HTTP Endpoints ===")

    # 1. Index
    res = client.get("/")
    assert res.status_code == 200, "Failed to load index.html"
    assert b"PULSE" in res.data
    assert b"WhatsApp Alerts" in res.data
    assert b"floatingAiBtn" in res.data
    assert b"floatingAiPanel" in res.data
    print("✓ GET / rendered with WhatsApp Alerts & Floating AI Assistant")

    # 2. WhatsApp Config
    res = client.get("/api/whatsapp/config")
    assert res.status_code == 200
    cfg = res.get_json()["config"]
    assert "recipient_phone" in cfg
    print("✓ GET /api/whatsapp/config ->", cfg["recipient_phone"])

    # 3. WhatsApp Toggle
    res = client.post("/api/whatsapp/toggle", json={"enabled": True})
    assert res.status_code == 200
    assert res.get_json()["enabled"] is True
    print("✓ POST /api/whatsapp/toggle -> Enabled: True")

    # 4. WhatsApp Rules
    res = client.get("/api/whatsapp/rules")
    assert res.status_code == 200
    rules = res.get_json()["rules"]
    assert len(rules) >= 4
    print("✓ GET /api/whatsapp/rules -> Count:", len(rules))

    # 5. WhatsApp Immediate Dispatch
    res = client.post("/api/whatsapp/send-immediate", json={
        "event_type": "stockout_risk",
        "urgency": "critical",
        "data": {
            "name": "Silk Sarees Premium",
            "sku": "SAR-001",
            "stock": 2,
            "days_left": 1,
            "stockout_risk_pct": 98.0,
            "reorder_point_units": 15,
            "eoq_units": 20
        }
    })
    assert res.status_code == 200
    assert res.get_json()["success"] is True
    print("✓ POST /api/whatsapp/send-immediate -> Dispatched AI Alert")

    # 6. WhatsApp Connection Test
    res = client.post("/api/whatsapp/test-connection", json={"phone": "+91 98765 43210"})
    assert res.status_code == 200
    assert res.get_json()["success"] is True
    print("✓ POST /api/whatsapp/test-connection -> Ping Success")

    # 7. WhatsApp History
    res = client.get("/api/whatsapp/history")
    assert res.status_code == 200
    logs = res.get_json()["logs"]
    assert len(logs) > 0
    print("✓ GET /api/whatsapp/history -> Total logs:", len(logs))

    # 8. WhatsApp Evaluate Triggers
    res = client.post("/api/whatsapp/evaluate-triggers")
    assert res.status_code == 200
    assert "triggered_count" in res.get_json()
    print("✓ POST /api/whatsapp/evaluate-triggers -> Success")

    # 9. Voice Command (English)
    res = client.post("/api/voice/command", json={"transcript": "Send today's performance summary to WhatsApp"})
    assert res.status_code == 200
    v_res = res.get_json()
    assert "summary" in v_res["spoken_text"].lower()
    print("✓ POST /api/voice/command (Summary) ->", v_res["spoken_text"][:60])

    # 10. Voice Command (Tamil)
    res = client.post("/api/voice/command", json={"transcript": "வணக்கம், business health eppadi irukku?"})
    assert res.status_code == 200
    v_res = res.get_json()
    assert v_res["lang_code"] == "ta-IN"
    print("✓ POST /api/voice/command (Tamil) -> Lang:", v_res["lang_code"])

    # 11. Voice Command (Hindi)
    res = client.post("/api/voice/command", json={"transcript": "WhatsApp alerts chalu karo"})
    assert res.status_code == 200
    v_res = res.get_json()
    assert v_res["lang_code"] == "hi-IN"
    print("✓ POST /api/voice/command (Hindi WhatsApp on) -> Lang:", v_res["lang_code"])

    # 12. Voice Multilingual TTS Audio Stream (Tamil)
    res = client.get("/api/voice/tts?lang=ta&text=" + "வணக்கம் உங்கள் பிசினஸ் சுருக்கம்")
    assert res.status_code == 200
    assert res.content_type == "audio/mpeg"
    assert len(res.data) > 1000
    print(f"✓ GET /api/voice/tts (Tamil Audio MP3) -> Status: 200, Stream Size: {len(res.data)} bytes")

    print("\n🎉 ALL REST API ENDPOINTS & VOICE EXECUTORS VALIDATED SUCCESSFULLY!")

if __name__ == "__main__":
    test_routes()
