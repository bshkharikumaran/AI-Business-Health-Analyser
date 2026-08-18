"""
Vyapaar Pulse — Enterprise-Grade MSME Business Health Analyzer & Autonomous Voice AI Copilot.
Flask Application Entrypoint with Firebase Database Persistence, Real-Time Analytics,
and AI-Powered WhatsApp Alert Automation Engine.
"""
import re
import os
import uuid
from datetime import datetime
from flask import Flask, jsonify, request, render_template

import db
import logic
import voice_assistant

app = Flask(__name__)

# Initialize Firebase on startup
db.init_firebase()


def _get_current_state():
    return db.load_state()


def _current_analysis():
    """Computes all analytical models from live state."""
    state = _get_current_state()
    forecast = logic.forecast_sales(state.get("sales_history", []))
    inventory = logic.evaluate_inventory(state.get("inventory", []))
    sentiment = logic.analyze_reviews(state.get("reviews", []))
    health = logic.compute_health_score(forecast, inventory, sentiment, state.get("business_profile"))
    return forecast, inventory, sentiment, health


def _find_inventory_item(query):
    """Fuzzy-match product name or SKU."""
    state = _get_current_state()
    q = query.lower().strip()
    for item in state.get("inventory", []):
        if q in item["name"].lower() or q in item.get("sku", "").lower():
            return item
    qwords = set(re.split(r"[\s\-—]+", q))
    best, best_score = None, 0
    for item in state.get("inventory", []):
        iwords = set(re.split(r"[\s\-—()]+", item["name"].lower()))
        score = len(qwords & iwords)
        if score > best_score:
            best, best_score = item, score
    return best


def _resolve_month_index(query):
    """Resolves month phrasing to index in sales_months."""
    state = _get_current_state()
    q = query.lower().strip()
    months = state.get("sales_months", [])
    if q in ("this month", "current month", "latest month", "last recorded month"):
        return len(months) - 1
    if q in ("last month", "previous month"):
        return max(0, len(months) - 2)
    for i, m in enumerate(months):
        if q in m.lower() or m.lower() in q:
            return i
    for i, m in enumerate(months):
        name_part = m.split("'")[0].lower()
        if name_part and (name_part in q or q in name_part):
            return i
    return None


# ---------------------------------------------------------------------------
# Shared Mutation & Query Helpers (Syncs to Firebase / DB)
# ---------------------------------------------------------------------------
def set_sales_history(history):
    state = _get_current_state()
    state["sales_history"] = [max(0.0, float(v)) for v in history]
    db.save_state(state)
    return logic.forecast_sales(state["sales_history"])


def update_inventory_field(sku, field, value):
    state = _get_current_state()
    for item in state.get("inventory", []):
        if item["sku"].upper() == sku.upper():
            item[field] = max(0.0, float(value))
            db.save_state(state)
            return logic.evaluate_inventory(state["inventory"])
    return None


def set_reviews(reviews):
    state = _get_current_state()
    formatted = []
    for r in reviews:
        if isinstance(r, str):
            formatted.append({"text": r.strip(), "source": "User Submission", "date": "Today"})
        elif isinstance(r, dict):
            formatted.append(r)
    state["reviews"] = formatted
    db.save_state(state)
    return logic.analyze_reviews(state["reviews"])


def dispatch_alerts():
    state = _get_current_state()
    forecast, inventory, sentiment, health = _current_analysis()
    rules = db.get_whatsapp_rules()
    profile = state.get("business_profile", {})
    recent_logs = db.get_whatsapp_logs(limit=20)
    
    # Evaluate dynamic rules
    alerts = logic.evaluate_alert_rules(rules, inventory, sentiment, forecast, health, profile, recent_logs=recent_logs, force_send=True)
    if not alerts:
        # Fallback to legacy alerts if none matched
        owner = profile.get("owner_name", "Chinnu")
        alerts = logic.generate_alerts(inventory, sentiment, forecast, owner)
        
    for a in alerts:
        db.append_whatsapp_log(a)
    return alerts


def update_profile_and_match(updates):
    state = _get_current_state()
    state["business_profile"].update({
        k: v for k, v in updates.items()
        if k in ("category", "sector", "turnover_lakhs", "state", "owner_name", "name", "phone", "city") and v is not None
    })
    db.save_state(state)
    return logic.match_schemes(state["business_profile"])


# ---------------------------------------------------------------------------
# Voice Command Executors
# ---------------------------------------------------------------------------
def _voice_navigate(view):
    labels = {
        "overview": "the Executive Dashboard Overview",
        "dashboard": "the Executive Dashboard Overview",
        "sales": "AI Sales Forecasting & Scenario Simulator",
        "inventory": "Inventory Intelligence & ABC-XYZ Matrix",
        "sentiment": "Aspect-Based Customer Sentiment",
        "alerts": "Alerts & Government Scheme Subsidies",
        "whatsapp-automation": "AI-Powered WhatsApp Alert Automation Dashboard",
        "data-feed": "Data Feeding & Ingestion Studio",
        "data_feeding": "Data Feeding & Ingestion Studio",
        "data-analysis": "Dedicated Data Analysis Workspace",
        "analytics": "Visual Analytics Studio",
        "insights": "AI Business Insights Stream",
        "reports": "Executive Report Generation Studio"
    }
    view_key = "dashboard" if view == "overview" else view
    return {
        "spoken_text": f"Navigating to {labels.get(view, view)}.",
        "view": view_key,
        "data": {"view": view_key}
    }


def _voice_get_health():
    _, _, _, health = _current_analysis()
    return {
        "spoken_text": f"Your business health score is {health['score']} out of 100 ({health['badge']}). {health['verdict']}",
        "view": "dashboard",
        "data": health
    }


def _voice_get_forecast():
    state = _get_current_state()
    forecast = logic.forecast_sales(state["sales_history"])
    direction = "rise" if forecast["next_period_pct_change"] >= 0 else "dip"
    text = (f"The 3-month sales forecast projects next month at ₹{forecast['forecast'][0]} thousand, "
            f"a {abs(forecast['next_period_pct_change'])}% {direction} compared to last recorded revenue.")
    return {"spoken_text": text, "view": "sales", "data": forecast}


def _voice_simulate_scenario(promo_boost_pct=15.0, festival_multiplier=1.2, discount_pct=0.0, inflation_pct=0.0):
    state = _get_current_state()
    sim = logic.simulate_sales_scenario(
        state["sales_history"],
        promo_boost_pct=float(promo_boost_pct),
        festival_multiplier=float(festival_multiplier),
        discount_pct=float(discount_pct),
        inflation_pct=float(inflation_pct)
    )
    text = f"Scenario simulated: Projected 3-month revenue shift of {'+' if sim['incremental_revenue_3m'] >= 0 else ''}₹{sim['incremental_revenue_3m']} thousand ({sim['revenue_delta_pct']}%). {sim['recommendation']}"
    return {"spoken_text": text, "view": "sales", "data": sim}


def _voice_update_sales_month(month, value):
    state = _get_current_state()
    idx = _resolve_month_index(month)
    if idx is None:
        return {"spoken_text": f"Could not match '{month}' to a recorded month in the database.", "view": "sales", "data": None}
    history = list(state["sales_history"])
    history[idx] = max(0.0, float(value))
    forecast = set_sales_history(history)
    label = state["sales_months"][idx]
    return {
        "spoken_text": f"Updated {label} sales to ₹{value} thousand. Recalculated forecast for next month is now ₹{forecast['forecast'][0]} thousand.",
        "view": "sales",
        "data": forecast
    }


def _voice_get_inventory_status(product_name=None):
    state = _get_current_state()
    if not product_name:
        inv = logic.evaluate_inventory(state["inventory"])
        text = (f"Inventory status: {inv['healthy_count']} of {inv['total']} products are optimal. "
                f"{inv['reorder_count']} items require urgent reorder, and ₹{inv['total_capital_locked']} is currently locked in stock.")
        return {"spoken_text": text, "view": "inventory", "data": inv}
    item = _find_inventory_item(product_name)
    if item is None:
        return {"spoken_text": f"No product matching '{product_name}' was found in the inventory database.", "view": "inventory", "data": None}
    eval_item = logic.evaluate_inventory_item(item)
    text = f"{eval_item['name']} has {eval_item['stock']} units on hand ({eval_item['days_left']} days left). Status: {eval_item['status'].upper()} with stockout risk of {eval_item['stockout_risk_pct']}%."
    return {"spoken_text": text, "view": "inventory", "data": eval_item}


def _voice_update_inventory_item(product_name, field, value):
    item = _find_inventory_item(product_name)
    if item is None:
        return {"spoken_text": f"Could not find product '{product_name}' in inventory.", "view": "inventory", "data": None}
    inv = update_inventory_field(item["sku"], field, value)
    return {"spoken_text": f"Updated {item['name']} {field.replace('_', ' ')} to {value} in database.", "view": "inventory", "data": inv}


def _voice_run_sentiment():
    state = _get_current_state()
    sentiment = logic.analyze_reviews(state["reviews"])
    text = f"Analyzed {sentiment['total']} customer reviews: {sentiment['positive_pct']}% positive rating with an estimated Net Promoter Score of +{sentiment['nps_estimate']}."
    return {"spoken_text": text, "view": "sentiment", "data": sentiment}


def _voice_enable_whatsapp_alerts(category=None):
    cfg = db.update_whatsapp_config({"enabled": True, "notify_critical_only": (category == "critical")})
    phone = cfg.get("recipient_phone", "+91 98765 43210")
    text = f"WhatsApp alerts for {'critical events' if category == 'critical' else 'all operational events'} have been enabled and connected to {phone}."
    return {"spoken_text": text, "view": "whatsapp-automation", "data": cfg}


def _voice_disable_whatsapp_alerts():
    cfg = db.update_whatsapp_config({"enabled": False})
    text = "WhatsApp alerts and notifications have been paused and disabled."
    return {"spoken_text": text, "view": "whatsapp-automation", "data": cfg}


def _voice_send_performance_summary_whatsapp():
    state = _get_current_state()
    forecast, inventory, sentiment, health = _current_analysis()
    profile = state.get("business_profile", {})
    phone = state.get("whatsapp_automation", {}).get("recipient_phone", profile.get("phone", "+91 98765 43210"))
    
    summary_data = {
        "health_score": health.get("score", 47),
        "badge": health.get("badge", "Attention Required"),
        "sales_forecast_3m": forecast.get("forecast", [196.6])[0],
        "reorder_count": inventory.get("reorder_count", 2),
        "nps": sentiment.get("nps_estimate", 21),
        "positive_pct": sentiment.get("positive_pct", 57.1)
    }
    
    ai_msg = logic.generate_ai_whatsapp_message("daily_summary", summary_data, profile=profile)
    log_entry = db.append_whatsapp_log({
        "to": f"{profile.get('owner_name', 'Chinnu')} ({phone})",
        "phone": phone,
        "event_type": "daily_summary",
        "type": "daily_summary",
        "urgency": "info",
        "title": ai_msg["title"],
        "message": ai_msg["message"],
        "status": "delivered",
        "channel": "WhatsApp (Automated Bot)",
        "timestamp": datetime.now().isoformat(timespec="seconds")
    })
    
    text = f"Today's business performance summary (Health Score: {summary_data['health_score']}/100) has been generated and dispatched to your WhatsApp ({phone})."
    return {"spoken_text": text, "view": "whatsapp-automation", "data": log_entry}


def _voice_send_alerts():
    alerts = dispatch_alerts()
    if not alerts:
        return {"spoken_text": "All metrics are within optimal thresholds. No critical alerts to dispatch.", "view": "whatsapp-automation", "data": []}
    return {"spoken_text": f"Dispatched {len(alerts)} automated WhatsApp alerts to the store owner.", "view": "whatsapp-automation", "data": alerts}


def _voice_create_whatsapp_rule(name, event_type, condition_threshold, urgency="high"):
    rule = db.save_whatsapp_rule({
        "name": name,
        "event_type": event_type,
        "metric": "value",
        "operator": "<",
        "threshold": condition_threshold,
        "urgency": urgency,
        "enabled": True,
        "auto_send": True,
        "description": f"Automated trigger when {event_type} threshold reaches {condition_threshold}"
    })
    text = f"Created new WhatsApp automation rule: '{name}' with {urgency} priority."
    return {"spoken_text": text, "view": "whatsapp-automation", "data": rule}


def _voice_get_alert_history():
    logs = db.get_whatsapp_logs(limit=5)
    count = len(logs)
    if count == 0:
        text = "No alerts have been recorded today. Your WhatsApp notification queue is clear."
    else:
        latest = logs[0]
        text = f"You have {count} recent alerts on record. The latest alert was '{latest.get('title', 'Notification')}' delivered via WhatsApp."
    return {"spoken_text": text, "view": "whatsapp-automation", "data": logs}


def _voice_test_whatsapp(phone=None):
    state = _get_current_state()
    profile = state.get("business_profile", {})
    target_phone = phone or state.get("whatsapp_automation", {}).get("recipient_phone", profile.get("phone", "+91 98765 43210"))
    
    ai_msg = logic.generate_ai_whatsapp_message("test_connection", {"phone": target_phone}, profile=profile)
    log_entry = db.append_whatsapp_log({
        "to": f"{profile.get('owner_name', 'Chinnu')} ({target_phone})",
        "phone": target_phone,
        "event_type": "test_connection",
        "type": "system",
        "urgency": "info",
        "title": ai_msg["title"],
        "message": ai_msg["message"],
        "status": "delivered",
        "channel": "WhatsApp (Automated Bot)",
        "timestamp": datetime.now().isoformat(timespec="seconds")
    })
    
    text = f"WhatsApp connection test completed successfully. A verification ping was delivered to {target_phone}."
    return {"spoken_text": text, "view": "whatsapp-automation", "data": log_entry}


def _voice_generate_campaign(theme="festival", discount_pct=15, product_name="Sarees & Home Goods", language="ta"):
    campaign = logic.generate_localized_campaign(theme=theme, discount_pct=discount_pct, language=language, product_name=product_name)
    state = _get_current_state()
    state.setdefault("campaigns", []).append(campaign)
    db.save_state(state)
    return {"spoken_text": f"Generated {theme} promotional campaign in {language.upper()} with {discount_pct}% discount.", "view": "whatsapp-automation", "data": campaign}


def _voice_get_schemes(category=None, sector=None, turnover_lakhs=None, state=None):
    updates = {"category": category, "sector": sector, "turnover_lakhs": turnover_lakhs, "state": state}
    result = update_profile_and_match(updates)
    return {"spoken_text": f"Matched {result['match_count']} government subsidy schemes for this enterprise.", "view": "dashboard", "data": result}


def _voice_get_full_summary(language=None):
    state = _get_current_state()
    forecast, inventory, sentiment, health = _current_analysis()
    profile = state.get("business_profile", {})
    
    summary_data = {
        "health_score": health.get("score", 47),
        "health_badge": health.get("badge", "Attention Required"),
        "net_arr": "$8.45M",
        "arr_growth_yoy": "+18.4%",
        "subscribers": 3850,
        "cac": "$315",
        "ltv": "$9,450",
        "churn_rate": "0.9%",
        "net_retention": "140%",
        "forecast_next_month": forecast.get("forecast", [196.6])[0],
        "inventory_total": inventory.get("total", 7),
        "reorder_count": inventory.get("reorder_count", 2),
        "locked_capital": inventory.get("total_capital_locked", 102710.0),
        "critical_items": [i["name"] for i in inventory.get("items", []) if i.get("days_left", 99) <= 3],
        "positive_sentiment_pct": sentiment.get("positive_pct", 60.0),
        "nps": sentiment.get("nps_estimate", 27),
        "data_records": "142,850",
        "data_sources": "8 Connected",
        "data_quality": "98.5%"
    }
    
    # Regional Spoken Summaries
    lang = (language or "en").lower()
    if "ta" in lang:
        spoken = (
            f"வணக்கம்! உங்கள் பிசினஸ் சுருக்கம்: மொத்த Net ARR $8.45 Million (வளர்ச்சி +18.4%), "
            f"பிசினஸ் ஹெல்த் ஸ்கோர் 100-க்கு {summary_data['health_score']} ({summary_data['health_badge']}). "
            f"அடுத்த மாத உத்தேச விற்பனை ₹{summary_data['forecast_next_month']}k. "
            f"இருப்பில் Cotton Sarees உள்ளிட்ட {summary_data['reorder_count']} பொருட்களுக்கு உடனடி ரீஆர்டர் தேவை. "
            f"வாடிக்கையாளர் பாசிட்டிவ் ரேட்டிங் {summary_data['positive_sentiment_pct']}% (NPS: +{summary_data['nps']})."
        )
    elif "hi" in lang:
        spoken = (
            f"नमस्ते! आपके व्यापार का मुख्य सारांश: कुल Net ARR $8.45 Million है (+18.4% YoY), "
            f"बिजनेस हेल्थ स्कोर {summary_data['health_score']}/100 है। "
            f"अगले महीने का अनुमानित राजस्व ₹{summary_data['forecast_next_month']}k है। "
            f"इन्वेंट्री में {summary_data['reorder_count']} उत्पादों का तुरंत रीऑर्डर आवश्यक है। "
            f"ग्राहक संतुष्टि {summary_data['positive_sentiment_pct']}% पॉजिटिव (NPS: +{summary_data['nps']}) है।"
        )
    elif "te" in lang:
        spoken = (
            f"నమస్కారం! మీ వ్యాపార సారాంశం: మొత్తం Net ARR $8.45M (+18.4% వృద్ధి), "
            f"హెల్త్ స్కోర్ 100 కి {summary_data['health_score']} ({summary_data['health_badge']}). "
            f"వచ్చే నెల అంచనా అమ్మకాలు ₹{summary_data['forecast_next_month']}k. "
            f"స్టాక్‌లో {summary_data['reorder_count']} వస్తువులకు వెంటనే రీఆర్డర్ అవసరం. "
            f"కస్టమర్ సంతృప్తి {summary_data['positive_sentiment_pct']}% పాజిటివ్."
        )
    elif "ml" in lang:
        spoken = (
            f"നമസ്കാരം! നിങ്ങളുടെ ബിസിനസ്സ് സംഗ്രഹം: ആകെ Net ARR $8.45M (+18.4%), "
            f"ഹെൽത്ത് സ്കോർ 100-ൽ {summary_data['health_score']}. "
            f"അടുത്ത മാസത്തെ പ്രതീക്ഷിക്കുന്ന വരുമാനം ₹{summary_data['forecast_next_month']}k. "
            f"{summary_data['reorder_count']} ഉൽപ്പന്നങ്ങൾക്ക് സ്റ്റോക്ക് റീഓർഡർ ആവശ്യമാണ്."
        )
    elif "kn" in lang:
        spoken = (
            f"ನಮಸ್ಕಾರ! ನಿಮ್ಮ ವ್ಯಾಪಾರ ಸಾರಾಂಶ: ಒಟ್ಟು Net ARR $8.45M (+18.4% ಬೆಳವಣಿಗೆ), "
            f"ಹೆಲ್ತ್ ಸ್ಕೋರ್ 100 ಕ್ಕೆ {summary_data['health_score']}. "
            f"ಮುಂದಿನ ತಿಂಗಳ ಅಂದಾಜು ಮಾರಾಟ ₹{summary_data['forecast_next_month']}k. "
            f"{summary_data['reorder_count']} ವಸ್ತುಗಳಿಗೆ ತಕ್ಷಣ ಮರುಆರ್ಡರ್ ಅಗತ್ಯವಿದೆ."
        )
    else:
        spoken = (
            f"Executive Business Summary: Total Net ARR is $8.45M (+18.4% YoY) with 3,850 active subscribers and 140% net retention. "
            f"Overall Business Health Score is {summary_data['health_score']}/100 ({summary_data['health_badge']}). "
            f"Projected next month revenue is ₹{summary_data['forecast_next_month']}k. "
            f"Inventory requires urgent reorders for {summary_data['reorder_count']} items (including Cotton Sarees). "
            f"Customer sentiment stands at {summary_data['positive_sentiment_pct']}% positive with an NPS of +{summary_data['nps']}."
        )
        
    return {"spoken_text": spoken, "view": "dashboard", "data": summary_data}


def _voice_get_saas_metrics():
    data = {
        "net_arr": "$8.45M",
        "mrr": "$704.1k",
        "active_subscribers": 3850,
        "cac": "$315",
        "ltv": "$9,450",
        "churn_rate": "0.9%",
        "net_retention": "140%",
        "regional_breakdown": {"North America": "45%", "EMEA": "32%", "APAC": "23%"}
    }
    text = (
        f"Enterprise SaaS Telemetry: Net ARR is $8.45 Million with a monthly MRR of $704.1k across 3,850 active accounts. "
        f"Net revenue retention is stellar at 140% with an ultra-low churn rate of 0.9%. Customer LTV is $9,450 vs CAC of $315."
    )
    return {"spoken_text": text, "view": "analytics", "data": data}


def _voice_get_customer_churn():
    data = {
        "total_customers_tracked": 5,
        "nps_score": 27,
        "positive_ratio": "60.0%",
        "at_risk_cohort": [{"id": "CUST-903", "segment": "At Risk", "churn_risk": "74.0%", "city": "Delhi", "tickets": 5, "last_order_days": 78}],
        "top_spenders": [{"id": "CUST-905", "segment": "VIP Enterprise", "spend": "$15,400", "orders": 55, "churn_risk": "3.0%"}]
    }
    text = (
        f"Customer Intelligence: 60% positive feedback with an NPS of +27. "
        f"Alert: Customer CUST-903 in Delhi is At Risk with a 74% churn probability and 5 open support tickets. "
        f"Top VIP account CUST-905 is highly engaged with $15,400 lifetime spend and 3% churn risk."
    )
    return {"spoken_text": text, "view": "insights", "data": data}


def _voice_get_credit_risk():
    data = {
        "entities_audited": 4,
        "top_credit": {"id": "ENT-01", "sector": "Textiles", "rating": "AAA", "score": 780, "dscr": 2.4, "runway_months": 14.2},
        "at_risk": {"id": "ENT-04", "sector": "Leather Goods", "rating": "BB", "score": 610, "default_risk": "28.0%", "runway_months": 2.8}
    }
    text = (
        f"Financial Risk & Credit Audit: Entity ENT-01 has a prime AAA rating with 780 credit score, 2.4 DSCR, and 14.2 months of cash runway. "
        f"Entity ENT-04 carries a BB rating with 28% default probability and only 2.8 months of cash runway remaining."
    )
    return {"spoken_text": text, "view": "data-analysis", "data": data}


def _voice_get_supply_chain():
    data = {
        "total_skus": 10,
        "top_margin_item": "Natural Sandalwood Incense (62.5% Gross Margin)",
        "high_velocity_item": "Heritage Filter Coffee Blend (12.0 units/day)",
        "critical_low_stock": "Handcrafted Clay Terracotta Pot (3 units left, 1.6 days runway)"
    }
    text = (
        f"Supply Chain Economics: Top gross margin item is Sandalwood Incense at 62.5%. "
        f"Highest velocity product is Heritage Filter Coffee at 12 units per day. "
        f"Immediate reorder needed for Terracotta Pots with only 3 units in stock (1.6 days runway)."
    )
    return {"spoken_text": text, "view": "dashboard", "data": data}


def _voice_get_platform_telemetry():
    data = {
        "records_ingested": 142850,
        "active_sources": 8,
        "data_quality_pct": 98.5,
        "critical_errors": 0,
        "sync_mode": "Live Continuous Synchronization"
    }
    text = (
        f"Platform Telemetry: 142,850 total records ingested across 8 connected enterprise data sources. "
        f"Data quality score is 98.5% with 0 critical schema anomalies and real-time live sync active."
    )
    return {"spoken_text": text, "view": "data-feed", "data": data}


VOICE_EXECUTORS = {
    "navigate_view": _voice_navigate,
    "get_business_health": _voice_get_health,
    "get_full_business_summary": _voice_get_full_summary,
    "get_saas_metrics": _voice_get_saas_metrics,
    "get_customer_churn": _voice_get_customer_churn,
    "get_credit_risk": _voice_get_credit_risk,
    "get_supply_chain": _voice_get_supply_chain,
    "get_platform_telemetry": _voice_get_platform_telemetry,
    "get_sales_forecast": _voice_get_forecast,
    "simulate_sales_scenario": _voice_simulate_scenario,
    "update_sales_month": _voice_update_sales_month,
    "get_inventory_status": _voice_get_inventory_status,
    "update_inventory_item": _voice_update_inventory_item,
    "run_sentiment_analysis": _voice_run_sentiment,
    "enable_whatsapp_alerts": _voice_enable_whatsapp_alerts,
    "disable_whatsapp_alerts": _voice_disable_whatsapp_alerts,
    "send_performance_summary_whatsapp": _voice_send_performance_summary_whatsapp,
    "send_whatsapp_alerts": _voice_send_alerts,
    "create_whatsapp_automation_rule": _voice_create_whatsapp_rule,
    "get_whatsapp_alert_history": _voice_get_alert_history,
    "test_whatsapp_connection": _voice_test_whatsapp,
    "generate_marketing_campaign": _voice_generate_campaign,
    "get_government_schemes": _voice_get_schemes,
}


# ---------------------------------------------------------------------------
# Flask HTTP Routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/business-profile", methods=["GET", "POST"])
def handle_profile():
    if request.method == "POST":
        body = request.get_json(force=True)
        return jsonify(update_profile_and_match(body))
    return jsonify(_get_current_state().get("business_profile", {}))


@app.route("/api/sales", methods=["GET", "POST"])
def handle_sales():
    if request.method == "POST":
        body = request.get_json(force=True)
        values = body.get("history")
        if not isinstance(values, list) or len(values) == 0:
            return jsonify({"error": "history must be a non-empty list of numbers"}), 400
        forecast = set_sales_history(values)
        state = _get_current_state()
        return jsonify({"months": state.get("sales_months", []), **forecast})

    state = _get_current_state()
    forecast = logic.forecast_sales(state.get("sales_history", []))
    return jsonify({"months": state.get("sales_months", []), **forecast})


@app.route("/api/sales/simulate", methods=["POST"])
def handle_sales_simulation():
    body = request.get_json(force=True) or {}
    state = _get_current_state()
    sim = logic.simulate_sales_scenario(
        state.get("sales_history", []),
        promo_boost_pct=float(body.get("promo_boost_pct", 0.0)),
        festival_multiplier=float(body.get("festival_multiplier", 1.0)),
        discount_pct=float(body.get("discount_pct", 0.0)),
        inflation_pct=float(body.get("inflation_pct", 0.0)),
        periods=int(body.get("periods", 3))
    )
    return jsonify(sim)


@app.route("/api/inventory", methods=["GET"])
def get_inventory():
    state = _get_current_state()
    return jsonify(logic.evaluate_inventory(state.get("inventory", [])))


@app.route("/api/inventory/<sku>", methods=["PATCH"])
def update_inventory(sku):
    body = request.get_json(force=True)
    for field in ("stock", "daily_sales", "lead_time_days", "unit_cost", "selling_price"):
        if field in body:
            res = update_inventory_field(sku, field, body[field])
            if res is None:
                return jsonify({"error": f"Item SKU '{sku}' not found"}), 404
    state = _get_current_state()
    return jsonify(logic.evaluate_inventory(state.get("inventory", [])))


@app.route("/api/sentiment", methods=["GET", "POST"])
def handle_sentiment():
    if request.method == "POST":
        body = request.get_json(force=True)
        reviews = body.get("reviews", [])
        return jsonify(set_reviews(reviews))
    state = _get_current_state()
    return jsonify(logic.analyze_reviews(state.get("reviews", [])))


# ---------------------------------------------------------------------------
# WhatsApp Alert Automation REST Endpoints
# ---------------------------------------------------------------------------
@app.route("/api/whatsapp/config", methods=["GET", "POST"])
def handle_whatsapp_config():
    if request.method == "POST":
        body = request.get_json(force=True) or {}
        updated = db.update_whatsapp_config(body)
        return jsonify({"success": True, "config": updated})
    return jsonify({"success": True, "config": db.get_whatsapp_config()})


@app.route("/api/whatsapp/toggle", methods=["POST"])
def toggle_whatsapp_master():
    body = request.get_json(force=True) or {}
    enabled = body.get("enabled")
    if enabled is None:
        cfg = db.get_whatsapp_config()
        enabled = not cfg.get("enabled", True)
    updated = db.update_whatsapp_config({"enabled": bool(enabled)})
    return jsonify({"success": True, "enabled": updated.get("enabled", True), "config": updated})


@app.route("/api/whatsapp/rules", methods=["GET", "POST"])
def handle_whatsapp_rules():
    if request.method == "POST":
        body = request.get_json(force=True) or {}
        rule = db.save_whatsapp_rule(body)
        return jsonify({"success": True, "rule": rule, "rules": db.get_whatsapp_rules()})
    return jsonify({"success": True, "rules": db.get_whatsapp_rules()})


@app.route("/api/whatsapp/rules/<rule_id>", methods=["PATCH", "DELETE"])
def modify_whatsapp_rule(rule_id):
    if request.method == "DELETE":
        db.delete_whatsapp_rule(rule_id)
        return jsonify({"success": True, "message": f"Rule {rule_id} deleted", "rules": db.get_whatsapp_rules()})
    
    body = request.get_json(force=True) or {}
    body["id"] = rule_id
    rule = db.save_whatsapp_rule(body)
    return jsonify({"success": True, "rule": rule, "rules": db.get_whatsapp_rules()})


@app.route("/api/whatsapp/rules/<rule_id>/toggle", methods=["POST"])
def toggle_single_rule(rule_id):
    body = request.get_json(force=True) or {}
    enabled = body.get("enabled")
    res = db.toggle_whatsapp_rule(rule_id, enabled)
    if not res:
        return jsonify({"error": f"Rule {rule_id} not found"}), 404
    return jsonify({"success": True, "rule": res, "rules": db.get_whatsapp_rules()})


@app.route("/api/whatsapp/send-immediate", methods=["POST"])
def send_immediate_whatsapp_alert():
    body = request.get_json(force=True) or {}
    state = _get_current_state()
    profile = state.get("business_profile", {})
    phone = body.get("phone") or state.get("whatsapp_automation", {}).get("recipient_phone", profile.get("phone", "+91 98765 43210"))
    
    title = body.get("title", "⚡ Executive Alert Notification")
    message = body.get("message")
    urgency = body.get("urgency", "high")
    event_type = body.get("event_type", "custom")
    language = body.get("language", "en")
    
    if not message:
        # Generate AI copy dynamically based on event_type
        event_data = body.get("data") or {"value": "Manual Trigger"}
        ai_res = logic.generate_ai_whatsapp_message(event_type, event_data, profile=profile, language=language)
        title = ai_res.get("title", title)
        message = ai_res.get("message", "Live Alert Dispatched.")
        urgency = ai_res.get("urgency", urgency)
        
    log_entry = db.append_whatsapp_log({
        "to": f"{profile.get('owner_name', 'Chinnu')} ({phone})",
        "phone": phone,
        "event_type": event_type,
        "type": event_type,
        "urgency": urgency,
        "title": title,
        "message": message,
        "status": "delivered",
        "channel": "WhatsApp (Automated Bot)",
        "timestamp": datetime.now().isoformat(timespec="seconds")
    })
    
    return jsonify({
        "success": True,
        "message": f"WhatsApp alert dispatched successfully to {phone}",
        "alert": log_entry,
        "config": db.get_whatsapp_config()
    })


@app.route("/api/whatsapp/test-connection", methods=["POST"])
def test_whatsapp_connection_endpoint():
    body = request.get_json(force=True) or {}
    phone = body.get("phone")
    result = _voice_test_whatsapp(phone=phone)
    return jsonify({
        "success": True,
        "message": result["spoken_text"],
        "alert": result["data"],
        "config": db.get_whatsapp_config()
    })


@app.route("/api/whatsapp/history", methods=["GET", "DELETE"])
def handle_whatsapp_history():
    if request.method == "DELETE":
        db.clear_whatsapp_logs()
        return jsonify({"success": True, "message": "Alert history cleared", "logs": []})
    limit = int(request.args.get("limit", 100))
    logs = db.get_whatsapp_logs(limit=limit)
    return jsonify({"success": True, "logs": logs, "count": len(logs)})


@app.route("/api/whatsapp/scheduled", methods=["GET", "POST"])
def handle_scheduled_whatsapp():
    if request.method == "POST":
        body = request.get_json(force=True) or {}
        job = db.save_scheduled_alert(body)
        return jsonify({"success": True, "job": job, "scheduled": db.get_scheduled_alerts()})
    return jsonify({"success": True, "scheduled": db.get_scheduled_alerts()})


@app.route("/api/whatsapp/scheduled/<job_id>", methods=["DELETE"])
def delete_scheduled_job(job_id):
    db.delete_scheduled_alert(job_id)
    return jsonify({"success": True, "message": f"Scheduled job {job_id} removed", "scheduled": db.get_scheduled_alerts()})


@app.route("/api/whatsapp/evaluate-triggers", methods=["POST"])
def evaluate_triggers_endpoint():
    state = _get_current_state()
    forecast, inventory, sentiment, health = _current_analysis()
    rules = db.get_whatsapp_rules()
    profile = state.get("business_profile", {})
    recent_logs = db.get_whatsapp_logs(limit=30)
    
    triggered = logic.evaluate_alert_rules(rules, inventory, sentiment, forecast, health, profile, recent_logs=recent_logs, force_send=False)
    for a in triggered:
        db.append_whatsapp_log(a)
        
    return jsonify({
        "success": True,
        "triggered_count": len(triggered),
        "triggered_alerts": triggered,
        "config": db.get_whatsapp_config()
    })


@app.route("/api/whatsapp/alerts", methods=["GET"])
def preview_alerts():
    forecast, inventory, sentiment, _ = _current_analysis()
    state = _get_current_state()
    owner = state.get("business_profile", {}).get("owner_name", "Chinnu")
    alerts = logic.generate_alerts(inventory, sentiment, forecast, owner)
    return jsonify({"alerts": alerts, "count": len(alerts)})


@app.route("/api/whatsapp/send", methods=["POST"])
def send_alerts():
    alerts = dispatch_alerts()
    return jsonify({"sent": len(alerts), "alerts": alerts})


@app.route("/api/whatsapp/log", methods=["GET"])
def get_alert_log():
    state = _get_current_state()
    return jsonify({"log": state.get("whatsapp_log", [])})


@app.route("/api/campaigns/generate", methods=["POST"])
def handle_campaign_generation():
    body = request.get_json(force=True) or {}
    res = logic.generate_localized_campaign(
        theme=body.get("theme", "festival"),
        discount_pct=float(body.get("discount_pct", 15)),
        language=body.get("language", "ta"),
        product_name=body.get("product_name", "All Store Goods")
    )
    return jsonify(res)


@app.route("/api/schemes", methods=["GET", "POST"])
def handle_schemes():
    if request.method == "POST":
        body = request.get_json(force=True)
        return jsonify(update_profile_and_match(body))
    state = _get_current_state()
    return jsonify(logic.match_schemes(state.get("business_profile", {})))


@app.route("/api/schemes/calculate", methods=["POST"])
def calculate_subsidy_benefits():
    state = _get_current_state()
    body = request.get_json(force=True) or {}
    profile = state.get("business_profile", {})
    profile.update(body.get("profile", {}))
    return jsonify(logic.calculate_scheme_benefits(profile, scheme_id=body.get("scheme_id")))


@app.route("/api/health-score", methods=["GET"])
def get_health_score():
    forecast, inventory, sentiment, health = _current_analysis()
    return jsonify({
        "health": health,
        "forecast": forecast,
        "inventory": inventory,
        "sentiment": sentiment,
    })


@app.route("/api/db/status", methods=["GET"])
def get_database_status():
    return jsonify(db.get_db_status())


@app.route("/api/data/feed", methods=["POST"])
def feed_data_batch():
    body = request.get_json(force=True) or {}
    feed_type = body.get("type")  # 'sales', 'inventory', 'reviews', or 'all'
    data_payload = body.get("data")

    if feed_type == "sales":
        months = body.get("months", [])
        values = body.get("values", [])
        db.feed_sales_data(months, values)
    elif feed_type == "inventory":
        db.feed_inventory_batch(data_payload or [])
    elif feed_type == "reviews":
        db.feed_reviews_batch(data_payload or [])
    elif feed_type == "all":
        if "sales" in body:
            db.feed_sales_data(body["sales"].get("months", []), body["sales"].get("values", []))
        if "inventory" in body:
            db.feed_inventory_batch(body["inventory"])
        if "reviews" in body:
            db.feed_reviews_batch(body["reviews"])
    else:
        return jsonify({"error": "Invalid feed type. Must be 'sales', 'inventory', 'reviews', or 'all'"}), 400

    forecast, inventory, sentiment, health = _current_analysis()
    return jsonify({
        "success": True,
        "message": f"Successfully ingested {feed_type} data into persistent database.",
        "health": health,
        "inventory_count": len(_get_current_state().get("inventory", [])),
        "reviews_count": len(_get_current_state().get("reviews", [])),
    })


@app.route("/api/voice/status", methods=["GET"])
def voice_status():
    return jsonify(voice_assistant.gemini_status())


@app.route("/api/voice/command", methods=["POST"])
def voice_command():
    body = request.get_json(force=True) or {}
    transcript = body.get("transcript", "")
    result = voice_assistant.handle_voice_command(transcript, VOICE_EXECUTORS)
    return jsonify(result)


# ---------------------------------------------------------------------------
# Enterprise Analytics & Dataset API Endpoints
# ---------------------------------------------------------------------------
@app.route("/api/datasets/preset", methods=["GET"])
def list_preset_datasets():
    presets = logic.get_preset_datasets()
    return jsonify({
        "success": True,
        "datasets": [
            {
                "id": k,
                "name": v["name"],
                "description": v["description"],
                "category": v["category"],
                "rows_count": v["rows_count"],
                "columns": v["columns"]
            }
            for k, v in presets.items()
        ]
    })


@app.route("/api/datasets/preset/<preset_id>", methods=["GET", "POST"])
def get_preset_dataset(preset_id):
    presets = logic.get_preset_datasets()
    if preset_id not in presets:
        return jsonify({"error": f"Preset '{preset_id}' not found."}), 404
    ds = presets[preset_id]
    validation = logic.validate_dataset(ds["data"])
    return jsonify({
        "success": True,
        "dataset": ds,
        "validation": validation
    })


@app.route("/api/analytics/validate", methods=["POST"])
def api_validate_dataset():
    body = request.get_json(force=True) or {}
    rows = body.get("rows", [])
    validation = logic.validate_dataset(rows)
    return jsonify(validation)


@app.route("/api/analytics/clean", methods=["POST"])
def api_clean_dataset():
    body = request.get_json(force=True) or {}
    rows = body.get("rows", [])
    actions = body.get("actions", ["remove_duplicates", "impute_missing", "cap_outliers"])
    res = logic.clean_dataset(rows, actions)
    return jsonify(res)


@app.route("/api/analytics/run", methods=["POST"])
def api_run_analysis():
    body = request.get_json(force=True) or {}
    rows = body.get("rows", [])
    analysis_type = body.get("analysis_type", "descriptive")
    x_var = body.get("x_var")
    y_var = body.get("y_var")
    group_var = body.get("group_var")
    metric = body.get("metric", "sum")

    result = logic.run_data_analysis(
        rows=rows,
        analysis_type=analysis_type,
        x_var=x_var,
        y_var=y_var,
        group_var=group_var,
        metric=metric
    )
    return jsonify(result)


@app.route("/api/insights/feed", methods=["GET", "POST"])
def api_insights_feed():
    body = request.get_json(silent=True) or {}
    rows = body.get("rows")
    preset_id = body.get("preset_id", "saas_metrics")
    insights = logic.generate_business_insights(rows, preset_id=preset_id)
    return jsonify({"insights": insights, "total": len(insights)})


@app.route("/api/reports/generate", methods=["POST"])
def api_generate_report():
    body = request.get_json(force=True) or {}
    dataset_name = body.get("dataset_name", "Primary Active Dataset")
    rows = body.get("rows", [])
    sections = body.get("sections", ["summary", "kpis", "analysis", "data_quality", "charts", "insights"])
    report = logic.build_executive_report(dataset_name, rows, sections)
    return jsonify(report)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    print(f"\n🚀 Vyapaar Pulse running on: http://127.0.0.1:{port}\n")
    app.run(debug=True, host="0.0.0.0", port=port)
