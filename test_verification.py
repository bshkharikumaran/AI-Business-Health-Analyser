"""
Comprehensive Verification Test Suite for Vyapaar Pulse
Tests Analytics, Database Persistence, Multilingual Voice Intent Engine (Tamil, English, Telugu, Malayalam, Kannada, Hindi),
AI Dynamic WhatsApp Message Generation, and WhatsApp Alert Automation Endpoints.
"""
import sys
import os
import json

# Add current workspace to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import db
import logic
import voice_assistant
import app

def test_all():
    print("=== 1. Testing Database & Persistence Layer ===")
    status = db.get_db_status()
    print("DB Status:", status["mode"])
    state = db.load_state()
    assert "inventory" in state, "State missing inventory"
    assert "sales_history" in state, "State missing sales_history"
    assert "whatsapp_automation" in state, "State missing whatsapp_automation"
    print("Database loaded with", len(state["inventory"]), "SKUs and", len(state["whatsapp_log"]), "WhatsApp logs")

    print("\n=== 2. Testing Logic, Analytics & AI Dynamic Messaging ===")
    forecast = logic.forecast_sales(state["sales_history"])
    print("Forecast for next 3 months:", forecast["forecast"])
    assert len(forecast["forecast"]) == 3

    sim = logic.simulate_sales_scenario(state["sales_history"], promo_boost_pct=15, festival_multiplier=1.25)
    print("Scenario Sim 3M Delta: ₹", sim["incremental_revenue_3m"], "k")
    assert sim["incremental_revenue_3m"] > 0

    inv = logic.evaluate_inventory(state["inventory"])
    print("Inventory ABC/XYZ evaluated. Total locked capital: ₹", inv["total_capital_locked"])
    assert inv["total"] > 0

    sent = logic.analyze_reviews(state["reviews"])
    print("Sentiment NPS Estimate:", sent["nps_estimate"], "Positive %:", sent["positive_pct"])
    assert "aspect_breakdown" in sent

    health = logic.compute_health_score(forecast, inv, sent, state["business_profile"])
    print("5-Pillar Health Score:", health["score"], "/ 100 - Badge:", health["badge"])
    assert 0 <= health["score"] <= 100

    # Test AI Dynamic WhatsApp Message Generator
    ai_msg_en = logic.generate_ai_whatsapp_message("stockout_risk", inv["items"][0], profile=state["business_profile"], language="en")
    print("AI WhatsApp Msg [EN]:", ai_msg_en["title"])
    assert "Stockout" in ai_msg_en["title"]

    ai_msg_ta = logic.generate_ai_whatsapp_message("stockout_risk", inv["items"][0], profile=state["business_profile"], language="ta")
    print("AI WhatsApp Msg [TA]:", ai_msg_ta["title"])
    assert "ஸ்டாக்" in ai_msg_ta["title"]

    ai_msg_hi = logic.generate_ai_whatsapp_message("daily_summary", {"health_score": health["score"], "badge": health["badge"], "sales_forecast_3m": 196.6, "reorder_count": 2, "nps": 21, "positive_pct": 57.1}, profile=state["business_profile"], language="hi")
    print("AI WhatsApp Summary [HI]:", ai_msg_hi["title"])
    assert "ब्रीफिंग" in ai_msg_hi["title"] or "दैनिक" in ai_msg_hi["title"]

    print("\n=== 3. Testing Autonomous Multilingual Voice Assistant (6 Languages) ===")
    # 1. English
    res_en = voice_assistant.handle_voice_command("What is my business health?", app.VOICE_EXECUTORS)
    print("Voice [EN] ->", res_en["spoken_text"][:80], "| Lang:", res_en.get("lang_code"))
    assert res_en["lang_code"] == "en-IN"

    # 2. Tamil
    res_ta = voice_assistant.handle_voice_command("வணக்கம், business health eppadi irukku?", app.VOICE_EXECUTORS)
    print("Voice [TA] ->", res_ta["spoken_text"][:80], "| Lang:", res_ta.get("lang_code"))
    assert res_ta["lang_code"] == "ta-IN"

    # 3. Hindi
    res_hi = voice_assistant.handle_voice_command("Vyapar kaisa chal raha hai?", app.VOICE_EXECUTORS)
    print("Voice [HI] ->", res_hi["spoken_text"][:80], "| Lang:", res_hi.get("lang_code"))
    assert res_hi["lang_code"] == "hi-IN"

    # 4. Telugu
    res_te = voice_assistant.handle_voice_command("Business ela undi, chupinchu?", app.VOICE_EXECUTORS)
    print("Voice [TE] ->", res_te["spoken_text"][:80], "| Lang:", res_te.get("lang_code"))
    assert res_te["lang_code"] == "te-IN"

    # 5. Malayalam
    res_ml = voice_assistant.handle_voice_command("Business engane und, parayuka?", app.VOICE_EXECUTORS)
    print("Voice [ML] ->", res_ml["spoken_text"][:80], "| Lang:", res_ml.get("lang_code"))
    assert res_ml["lang_code"] == "ml-IN"

    # 6. Kannada
    res_kn = voice_assistant.handle_voice_command("Business hegide, nodona?", app.VOICE_EXECUTORS)
    print("Voice [KN] ->", res_kn["spoken_text"][:80], "| Lang:", res_kn.get("lang_code"))
    assert res_kn["lang_code"] == "kn-IN"

    print("\n=== 4. Testing Voice-Controlled WhatsApp Automations ===")
    # Voice command: Enable WhatsApp alerts
    res_v_enable = voice_assistant.handle_voice_command("Enable WhatsApp alerts for critical events", app.VOICE_EXECUTORS)
    print("Voice [Enable WhatsApp] ->", res_v_enable["spoken_text"])
    assert "enabled" in res_v_enable["spoken_text"].lower() or "activate" in res_v_enable["spoken_text"].lower()

    # Voice command: Send performance summary
    res_v_summary = voice_assistant.handle_voice_command("Send today's performance summary to WhatsApp", app.VOICE_EXECUTORS)
    print("Voice [Send Summary] ->", res_v_summary["spoken_text"])
    assert "summary" in res_v_summary["spoken_text"].lower()

    # Voice command: Test WhatsApp connection
    res_v_test = voice_assistant.handle_voice_command("Test WhatsApp connection", app.VOICE_EXECUTORS)
    print("Voice [Test Connection] ->", res_v_test["spoken_text"])
    assert "test" in res_v_test["spoken_text"].lower()

    # Voice command: Scenario simulation
    res_sim = voice_assistant.handle_voice_command("Simulate festival surge for Diwali", app.VOICE_EXECUTORS)
    print("Voice [Simulate] ->", res_sim["spoken_text"][:80])
    assert res_sim["view"] == "sales"

    print("\n=== 5. Testing WhatsApp Automation Rules & Config CRUD ===")
    config = db.get_whatsapp_config()
    assert config["enabled"] is True
    print("WhatsApp Recipient:", config["recipient_phone"], "| Mode:", config["provider"])

    # Create new rule
    new_rule = db.save_whatsapp_rule({
        "name": "Custom Margin Warning",
        "event_type": "custom_metric",
        "metric": "margin_pct",
        "operator": "<",
        "threshold": 30,
        "urgency": "medium"
    })
    print("Saved New Rule:", new_rule["name"], "(ID:", new_rule["id"], ")")
    assert new_rule["id"] in [r["id"] for r in db.get_whatsapp_rules()]

    # Append alert log
    log_entry = db.append_whatsapp_log({
        "to": "Test User",
        "phone": "+91 98765 43210",
        "event_type": "custom",
        "urgency": "info",
        "title": "Automated Verification Alert",
        "message": "Verification test alert payload."
    })
    print("Appended Alert Log:", log_entry["title"], "| Total Logs:", len(db.get_whatsapp_logs()))
    assert len(db.get_whatsapp_logs()) > 0

    print("\n🎉 ALL BACKEND, NLP MULTILINGUAL AGENTS, WHATSAPP AUTOMATION & REPOSITORIES VERIFIED SUCCESSFULLY!")

if __name__ == "__main__":
    test_all()
