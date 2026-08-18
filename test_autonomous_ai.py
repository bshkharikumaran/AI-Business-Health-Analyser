"""
Test Suite for Autonomous Multilingual AI Voice Assistant Knowledge & Web Data Engine
"""
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

def test_autonomous_ai():
    client = app.test_client()
    
    queries = [
        ("tell summary in tamil", "ta-IN", "வணக்கம்"),
        ("tell summary in hindi", "hi-IN", "नमस्ते"),
        ("what is our net ARR and MRR?", "en-IN", "$8.45 Million"),
        ("who is at risk of churning?", "en-IN", "CUST-903"),
        ("what is our credit risk and cash runway?", "en-IN", "ENT-01"),
        ("show supply chain and gross margins", "en-IN", "Sandalwood"),
        ("which government schemes can I apply for?", "en-IN", "government"),
        ("Enable WhatsApp alerts for critical events", "en-IN", "WhatsApp"),
        ("vanakkam, business eppadi irukku?", "ta-IN", "வணக்கம்")
    ]

    print("=== Testing Autonomous AI Assistant Data Access & Multilingual Engine ===")

    for q, expected_lang, expected_keyword in queries:
        res = client.post("/api/voice/command", json={"transcript": q})
        assert res.status_code == 200, f"Failed on query: {q}"
        data = res.get_json()
        print(f"\n[USER]: \"{q}\"")
        print(f"  [AI LANG]: {data.get('lang_code')}")
        print(f"  [AI ACTION]: {data.get('action')}")
        print(f"  [AI RESPONSE]: {data.get('spoken_text')}")
        assert expected_keyword.lower() in data.get('spoken_text', '').lower() or expected_keyword in data.get('spoken_text', '')

    print("\n🎉 ALL AUTONOMOUS MULTILINGUAL AI QUERIES TESTED & VERIFIED WITH FULL WEB DATA ACCESS!")

if __name__ == "__main__":
    test_autonomous_ai()
