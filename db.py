"""
Database Layer for Vyapaar Pulse.
Supports Firebase Firestore / Realtime DB integration with automatic
fallback to persistent local JSON storage (data/database.json).
Includes Enterprise WhatsApp Alert Automation persistence and history logging.
"""
import os
import json
import uuid
import urllib.request
import urllib.parse
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOCAL_DB_PATH = os.path.join(DATA_DIR, "database.json")
FIREBASE_CREDS_PATH = os.environ.get("FIREBASE_CREDENTIALS", os.path.join(BASE_DIR, "firebase-credentials.json"))
FIREBASE_DB_URL = os.environ.get("FIREBASE_DB_URL", "https://vyapaar-pulse-ai-default-rtdb.firebaseio.com")
FIREBASE_DB_SECRET = os.environ.get("FIREBASE_DB_SECRET", "H4XegOo6AxBtoq21kSbdwFGhTTiB0GVNVFBi35G3")

# Initial Seed Data
DEFAULT_STATE = {
    "business_profile": {
        "name": "Chinnu Textiles & Home Store",
        "owner_name": "Chinnu",
        "category": "small",
        "sector": "retail",
        "turnover_lakhs": 68.0,
        "state": "Tamil Nadu",
        "phone": "+91 98765 43210",
        "city": "Salem",
        "established_year": 2018
    },
    "sales_history": [182.0, 246.0, 268.0, 195.0, 231.0, 176.0, 168.0, 172.0, 179.0, 188.0, 196.0, 205.0],
    "sales_months": ["Sep'25", "Oct'25", "Nov'25", "Dec'25", "Jan'26", "Feb'26",
                     "Mar'26", "Apr'26", "May'26", "Jun'26", "Jul'26", "Aug'26"],
    "inventory": [
        {"name": "Cotton Sarees", "sku": "TXT-CS-014", "category": "Textiles", "unit_cost": 450, "selling_price": 750, "stock": 38, "daily_sales": 2.1, "lead_time_days": 10},
        {"name": "LED Bulbs (9W)", "sku": "ELE-LB-009", "category": "Electronics", "unit_cost": 65, "selling_price": 120, "stock": 210, "daily_sales": 6.5, "lead_time_days": 5},
        {"name": "Rice — 25kg bag", "sku": "GRO-RC-025", "category": "Groceries", "unit_cost": 1100, "selling_price": 1350, "stock": 14, "daily_sales": 3.4, "lead_time_days": 7},
        {"name": "School Notebooks", "sku": "STA-NB-200", "category": "Stationery", "unit_cost": 25, "selling_price": 45, "stock": 480, "daily_sales": 5.2, "lead_time_days": 12},
        {"name": "Steel Utensil Set", "sku": "HOM-SU-006", "category": "Home Goods", "unit_cost": 850, "selling_price": 1400, "stock": 22, "daily_sales": 0.8, "lead_time_days": 15},
        {"name": "Silk Blend Kurtis", "sku": "TXT-SK-032", "category": "Textiles", "unit_cost": 380, "selling_price": 699, "stock": 55, "daily_sales": 3.0, "lead_time_days": 8},
        {"name": "Cooking Oil 5L Can", "sku": "GRO-CO-005", "category": "Groceries", "unit_cost": 620, "selling_price": 720, "stock": 8, "daily_sales": 2.8, "lead_time_days": 4},
    ],
    "reviews": [
        {"text": "Saree quality romba nalla, super color and finish.", "source": "Google Review", "date": "2026-08-10"},
        {"text": "Delivery was 4 days late, very frustrating experience.", "source": "WhatsApp Feedback", "date": "2026-08-11"},
        {"text": "LED bulbs working perfectly, good price for the quality.", "source": "Google Review", "date": "2026-08-12"},
        {"text": "Item vantha packaging mosam ah irundhuchu, box damaged.", "source": "Direct Message", "date": "2026-08-13"},
        {"text": "Staff mikka friendly and helped me pick the right size.", "source": "Store Walk-in", "date": "2026-08-14"},
        {"text": "Notebooks paper quality is average, not great not bad.", "source": "Google Review", "date": "2026-08-14"},
        {"text": "Worst experience — wrong item sent and no refund yet.", "source": "Google Review", "date": "2026-08-15"},
        {"text": "Rice quality super, will order again next month.", "source": "WhatsApp Feedback", "date": "2026-08-15"},
        {"text": "Price konjam adhigama irukku but service is fast and reliable.", "source": "Google Review", "date": "2026-08-16"},
        {"text": "Utensils looked nice in photo but real quality is poor.", "source": "Direct Message", "date": "2026-08-16"},
        {"text": "Bohot badhiya service aur fast delivery hai! Highly recommended.", "source": "Google Review", "date": "2026-08-17"},
        {"text": "Saman bahut accha hai, pricing bhi reasonable hai.", "source": "Store Walk-in", "date": "2026-08-17"}
    ],
    "whatsapp_automation": {
        "enabled": True,
        "recipient_phone": "+91 98765 43210",
        "recipient_name": "Chinnu (Owner)",
        "provider": "simulator",
        "provider_config": {
            "api_key": "",
            "sender_number": "+14155238886",
            "webhook_url": ""
        },
        "cooldown_minutes": 360,
        "rate_limit_hourly": 10,
        "notify_critical_only": False,
        "rules": [
            {
                "id": "rule-1",
                "name": "Critical Stockout Warning",
                "event_type": "stockout_risk",
                "metric": "days_left",
                "operator": "<",
                "threshold": 5,
                "urgency": "critical",
                "enabled": True,
                "auto_send": True,
                "description": "Trigger alert when stock days left falls below 5 days"
            },
            {
                "id": "rule-2",
                "name": "Customer Satisfaction Alert",
                "event_type": "sentiment_dip",
                "metric": "positive_pct",
                "operator": "<",
                "threshold": 50,
                "urgency": "high",
                "enabled": True,
                "auto_send": True,
                "description": "Notify when customer positive review ratio drops below 50%"
            },
            {
                "id": "rule-3",
                "name": "Sales Drop Anomaly",
                "event_type": "sales_drop",
                "metric": "next_period_pct_change",
                "operator": "<",
                "threshold": -8,
                "urgency": "medium",
                "enabled": True,
                "auto_send": True,
                "description": "Alert when forecast projects >8% decline next month"
            },
            {
                "id": "rule-4",
                "name": "Daily Executive Summary Briefing",
                "event_type": "daily_summary",
                "metric": "schedule",
                "operator": "==",
                "threshold": "09:00",
                "urgency": "info",
                "enabled": True,
                "auto_send": True,
                "description": "Send daily telemetry snapshot every morning at 09:00 AM"
            }
        ],
        "scheduled_alerts": [
            {
                "id": "sched-1",
                "name": "Morning Executive Briefing",
                "time": "09:00 AM",
                "frequency": "Daily",
                "event_type": "daily_summary",
                "enabled": True,
                "last_run": "Today at 09:00 AM"
            },
            {
                "id": "sched-2",
                "name": "Evening Stock Reorder Scan",
                "time": "06:00 PM",
                "frequency": "Daily",
                "event_type": "stockout_risk",
                "enabled": True,
                "last_run": "Today at 06:00 PM"
            }
        ],
        "stats": {
            "total_sent": 4,
            "successful_sent": 4,
            "failed_sent": 0,
            "pending_count": 0
        }
    },
    "whatsapp_log": [
        {
            "id": "alert-init-1",
            "to": "Chinnu (Owner)",
            "phone": "+91 98765 43210",
            "type": "inventory",
            "event_type": "stockout_risk",
            "urgency": "critical",
            "title": "🚨 Critical Stockout Alert: Cooking Oil 5L Can",
            "message": "🚨 *Critical Stockout Alert*\n\nProduct: *Cooking Oil 5L Can* (GRO-CO-005)\n• Stock Remaining: *8 units* (2.9 days left)\n• Stockout Risk: *95.0%*\n• Recommended Reorder: *11 units* (EOQ: 11 units)\n\n⚡ *Recommended Action:* Contact supplier immediately to prevent weekend sales loss.",
            "timestamp": "2026-08-18T08:30:00",
            "status": "delivered",
            "channel": "WhatsApp (Automated Bot)",
            "delivery_status": "delivered"
        },
        {
            "id": "alert-init-2",
            "to": "Chinnu (Owner)",
            "phone": "+91 98765 43210",
            "type": "daily_summary",
            "event_type": "daily_summary",
            "urgency": "info",
            "title": "📊 Daily Business Intelligence Briefing",
            "message": "📊 *Vyapaar Pulse Daily Briefing*\n\n• Health Score: *47/100* (Attention Required)\n• 3M Projected Sales: *₹196.6k*\n• Inventory Alert: *2 items need reorder*\n• Customer Sentiment: *57.1% Positive* (NPS: +21)\n\n💡 *AI Recommendation:* Clear packaging complaints and place urgent grocery stock order.",
            "timestamp": "2026-08-18T09:00:00",
            "status": "delivered",
            "channel": "WhatsApp (Automated Bot)",
            "delivery_status": "delivered"
        },
        {
            "id": "alert-init-3",
            "to": "Chinnu (Owner)",
            "phone": "+91 98765 43210",
            "type": "sentiment",
            "event_type": "sentiment_dip",
            "urgency": "high",
            "title": "⚠️ Customer Sentiment Alert: Delivery Complaints",
            "message": "⚠️ *Customer Satisfaction Alert*\n\n• Issue: *Negative delivery feedback detected*\n• Current NPS: *+21*\n• Negative Ratio: *28.6%*\n\n⚡ *Recommended Action:* Coordinate with courier partner regarding 4-day shipment delays.",
            "timestamp": "2026-08-18T09:45:00",
            "status": "delivered",
            "channel": "WhatsApp (Automated Bot)",
            "delivery_status": "delivered"
        },
        {
            "id": "alert-init-4",
            "to": "Chinnu (Owner)",
            "phone": "+91 98765 43210",
            "type": "sales",
            "event_type": "sales_surge",
            "urgency": "medium",
            "title": "📈 Festive Demand Surge Predicted",
            "message": "📈 *Festive Demand Surge Notification*\n\n• Projected Growth: *+43.7%* for Festive Season\n• Top Category: *Textiles & Sarees*\n\n💡 *Action:* Ensure buffer inventory for Cotton Sarees and Silk Kurtis is stocked.",
            "timestamp": "2026-08-18T10:15:00",
            "status": "delivered",
            "channel": "WhatsApp (Automated Bot)",
            "delivery_status": "delivered"
        }
    ],
    "campaigns": [],
    "last_sync": datetime.now().isoformat()
}

_firestore_client = None
_firebase_enabled = False
_db_status = {"connected": False, "mode": "Local JSON Persistent Storage", "detail": "Using local file database"}


def _sync_firebase_rtdb_put(path, data):
    """PUT data to Firebase Realtime Database using Secret Token."""
    if not FIREBASE_DB_URL or not FIREBASE_DB_SECRET:
        return False
    try:
        url = f"{FIREBASE_DB_URL.rstrip('/')}/{path.lstrip('/')}.json?auth={FIREBASE_DB_SECRET}"
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        req = urllib.request.Request(url, data=body, headers={"Content-Type": "application/json"}, method="PUT")
        with urllib.request.urlopen(req, timeout=6) as resp:
            return resp.status in (200, 204)
    except Exception:
        return False


def _sync_firebase_rtdb_get(path):
    """GET data from Firebase Realtime Database using Secret Token."""
    if not FIREBASE_DB_URL or not FIREBASE_DB_SECRET:
        return None
    try:
        url = f"{FIREBASE_DB_URL.rstrip('/')}/{path.lstrip('/')}.json?auth={FIREBASE_DB_SECRET}"
        req = urllib.request.Request(url, headers={"User-Agent": "VyapaarPulse/1.0"}, method="GET")
        with urllib.request.urlopen(req, timeout=6) as resp:
            content = resp.read().decode('utf-8')
            return json.loads(content) if content and content != 'null' else None
    except Exception:
        return None


def init_firebase():
    """Attempts to initialize Firebase Realtime DB or Firestore."""
    global _firestore_client, _firebase_enabled, _db_status
    if _firebase_enabled:
        return True

    # 1. Firebase Realtime Database with Database Secret (Instant Cloud Sync)
    if FIREBASE_DB_URL and FIREBASE_DB_SECRET:
        try:
            cloud_data = _sync_firebase_rtdb_get("msme_businesses/default_business")
            _firebase_enabled = True
            _db_status = {
                "connected": True,
                "mode": "Firebase Realtime Database Live",
                "detail": f"Connected to {FIREBASE_DB_URL.split('://')[-1]}"
            }
            return True
        except Exception:
            pass

    # 2. Firebase Firestore with Service Account Key File
    if os.path.exists(FIREBASE_CREDS_PATH):
        try:
            import firebase_admin
            from firebase_admin import credentials, firestore

            if not firebase_admin._apps:
                cred = credentials.Certificate(FIREBASE_CREDS_PATH)
                firebase_admin.initialize_app(cred)
            _firestore_client = firestore.client()
            _firebase_enabled = True
            _db_status = {
                "connected": True,
                "mode": "Firebase Firestore Live",
                "detail": f"Connected via {os.path.basename(FIREBASE_CREDS_PATH)}"
            }
            return _firestore_client
        except Exception as e:
            _db_status = {
                "connected": False,
                "mode": "Local JSON Persistent Storage",
                "detail": f"Firebase init error: {str(e)}. Using fallback database."
            }
            return None

    _db_status = {
        "connected": False,
        "mode": "Local JSON Persistent Storage",
        "detail": "Provide Firebase credentials or secret to enable cloud sync."
    }
    return None


def get_db_status():
    """Returns the current database engine status."""
    init_firebase()
    status = dict(_db_status)
    state = load_state()
    status["stats"] = {
        "inventory_count": len(state.get("inventory", [])),
        "reviews_count": len(state.get("reviews", [])),
        "sales_months_count": len(state.get("sales_months", [])),
        "alerts_count": len(state.get("whatsapp_log", [])),
        "whatsapp_automation_enabled": state.get("whatsapp_automation", {}).get("enabled", False),
        "last_sync": state.get("last_sync", "N/A")
    }
    return status


def load_state():
    """Loads state from Firebase Realtime DB, Firestore, or Local JSON DB."""
    init_firebase()

    # 1. Try Firebase Realtime Database
    if FIREBASE_DB_URL and FIREBASE_DB_SECRET:
        try:
            cloud_data = _sync_firebase_rtdb_get("msme_businesses/default_business")
            if cloud_data and isinstance(cloud_data, dict):
                # Ensure whatsapp_automation exists
                if "whatsapp_automation" not in cloud_data:
                    cloud_data["whatsapp_automation"] = DEFAULT_STATE["whatsapp_automation"]
                # Mirror to local backup
                os.makedirs(DATA_DIR, exist_ok=True)
                with open(LOCAL_DB_PATH, "w", encoding="utf-8") as f:
                    json.dump(cloud_data, f, indent=2, ensure_ascii=False)
                return cloud_data
            else:
                # Seed cloud database
                save_state(DEFAULT_STATE)
                return DEFAULT_STATE
        except Exception:
            pass

    # 2. Try Firestore Client
    if _firestore_client:
        try:
            doc_ref = _firestore_client.collection("msme_businesses").document("default_business")
            doc = doc_ref.get()
            if doc.exists:
                data = doc.to_dict()
                if "whatsapp_automation" not in data:
                    data["whatsapp_automation"] = DEFAULT_STATE["whatsapp_automation"]
                return data
            else:
                save_state(DEFAULT_STATE)
                return DEFAULT_STATE
        except Exception:
            pass

    # 3. Local JSON fallback
    if os.path.exists(LOCAL_DB_PATH):
        try:
            with open(LOCAL_DB_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
                for k, v in DEFAULT_STATE.items():
                    if k not in data:
                        data[k] = v
                if "whatsapp_automation" not in data or not data["whatsapp_automation"]:
                    data["whatsapp_automation"] = DEFAULT_STATE["whatsapp_automation"]
                return data
        except Exception:
            pass

    os.makedirs(DATA_DIR, exist_ok=True)
    with open(LOCAL_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_STATE, f, indent=2, ensure_ascii=False)
    return dict(DEFAULT_STATE)


def save_state(state):
    """Saves state to Firebase Cloud and Local JSON DB."""
    state["last_sync"] = datetime.now().isoformat()

    # 1. Sync to Firebase Realtime Database
    if FIREBASE_DB_URL and FIREBASE_DB_SECRET:
        try:
            _sync_firebase_rtdb_put("msme_businesses/default_business", state)
        except Exception:
            pass

    # 2. Sync to Firestore
    if _firestore_client:
        try:
            doc_ref = _firestore_client.collection("msme_businesses").document("default_business")
            doc_ref.set(state)
        except Exception:
            pass

    # 3. Mirror to Local Backup
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(LOCAL_DB_PATH, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    return state


# ---------------------------------------------------------------------------
# WhatsApp Automation & Rules Persistence Helpers
# ---------------------------------------------------------------------------
def get_whatsapp_config():
    state = load_state()
    auto = state.get("whatsapp_automation", DEFAULT_STATE["whatsapp_automation"])
    logs = state.get("whatsapp_log", [])
    
    total = len(logs)
    successful = sum(1 for l in logs if l.get("status") in ("delivered", "sent", "success"))
    failed = sum(1 for l in logs if l.get("status") == "failed")
    
    auto["stats"] = {
        "total_sent": total,
        "successful_sent": successful,
        "failed_sent": failed,
        "pending_count": 0
    }
    return auto


def update_whatsapp_config(updates):
    state = load_state()
    auto = state.setdefault("whatsapp_automation", dict(DEFAULT_STATE["whatsapp_automation"]))
    for k, v in updates.items():
        if k in ("enabled", "recipient_phone", "recipient_name", "provider", "provider_config", "cooldown_minutes", "rate_limit_hourly", "notify_critical_only"):
            auto[k] = v
    save_state(state)
    return get_whatsapp_config()


def get_whatsapp_rules():
    state = load_state()
    return state.get("whatsapp_automation", {}).get("rules", DEFAULT_STATE["whatsapp_automation"]["rules"])


def save_whatsapp_rule(rule_data):
    state = load_state()
    auto = state.setdefault("whatsapp_automation", dict(DEFAULT_STATE["whatsapp_automation"]))
    rules = auto.setdefault("rules", [])
    
    rule_id = rule_data.get("id") or f"rule-{uuid.uuid4().hex[:6]}"
    existing_idx = next((i for i, r in enumerate(rules) if r.get("id") == rule_id), None)
    
    clean_rule = {
        "id": rule_id,
        "name": str(rule_data.get("name", "Custom Alert Rule")),
        "event_type": str(rule_data.get("event_type", "custom_metric")),
        "metric": str(rule_data.get("metric", "value")),
        "operator": str(rule_data.get("operator", "<")),
        "threshold": rule_data.get("threshold", 0),
        "urgency": str(rule_data.get("urgency", "high")),
        "enabled": bool(rule_data.get("enabled", True)),
        "auto_send": bool(rule_data.get("auto_send", True)),
        "description": str(rule_data.get("description", "User-defined automated rule"))
    }
    
    if existing_idx is not None:
        rules[existing_idx] = clean_rule
    else:
        rules.append(clean_rule)
        
    save_state(state)
    return clean_rule


def delete_whatsapp_rule(rule_id):
    state = load_state()
    auto = state.setdefault("whatsapp_automation", dict(DEFAULT_STATE["whatsapp_automation"]))
    rules = auto.setdefault("rules", [])
    auto["rules"] = [r for r in rules if r.get("id") != rule_id]
    save_state(state)
    return True


def toggle_whatsapp_rule(rule_id, enabled=None):
    state = load_state()
    auto = state.setdefault("whatsapp_automation", dict(DEFAULT_STATE["whatsapp_automation"]))
    rules = auto.setdefault("rules", [])
    for r in rules:
        if r.get("id") == rule_id:
            r["enabled"] = not r["enabled"] if enabled is None else bool(enabled)
            save_state(state)
            return r
    return None


def append_whatsapp_log(alert_entry):
    state = load_state()
    logs = state.setdefault("whatsapp_log", [])
    
    if not alert_entry.get("id"):
        alert_entry["id"] = f"alert-{uuid.uuid4().hex[:8]}"
    if not alert_entry.get("timestamp"):
        alert_entry["timestamp"] = datetime.now().isoformat(timespec="seconds")
    if not alert_entry.get("channel"):
        alert_entry["channel"] = "WhatsApp (Automated Bot)"
    if not alert_entry.get("status"):
        alert_entry["status"] = "delivered"
        
    logs.insert(0, alert_entry)
    state["whatsapp_log"] = logs[:200]  # keep recent 200 logs
    save_state(state)
    return alert_entry


def get_whatsapp_logs(limit=50):
    state = load_state()
    return state.get("whatsapp_log", [])[:limit]


def clear_whatsapp_logs():
    state = load_state()
    state["whatsapp_log"] = []
    save_state(state)
    return True


def get_scheduled_alerts():
    state = load_state()
    return state.get("whatsapp_automation", {}).get("scheduled_alerts", DEFAULT_STATE["whatsapp_automation"]["scheduled_alerts"])


def save_scheduled_alert(job_data):
    state = load_state()
    auto = state.setdefault("whatsapp_automation", dict(DEFAULT_STATE["whatsapp_automation"]))
    schedules = auto.setdefault("scheduled_alerts", [])
    
    job_id = job_data.get("id") or f"sched-{uuid.uuid4().hex[:6]}"
    existing_idx = next((i for i, s in enumerate(schedules) if s.get("id") == job_id), None)
    
    clean_job = {
        "id": job_id,
        "name": str(job_data.get("name", "Scheduled Alert")),
        "time": str(job_data.get("time", "09:00 AM")),
        "frequency": str(job_data.get("frequency", "Daily")),
        "event_type": str(job_data.get("event_type", "daily_summary")),
        "enabled": bool(job_data.get("enabled", True)),
        "last_run": str(job_data.get("last_run", "Never"))
    }
    
    if existing_idx is not None:
        schedules[existing_idx] = clean_job
    else:
        schedules.append(clean_job)
        
    save_state(state)
    return clean_job


def delete_scheduled_alert(job_id):
    state = load_state()
    auto = state.setdefault("whatsapp_automation", dict(DEFAULT_STATE["whatsapp_automation"]))
    schedules = auto.setdefault("scheduled_alerts", [])
    auto["scheduled_alerts"] = [s for s in schedules if s.get("id") != job_id]
    save_state(state)
    return True


# ---------------------------------------------------------------------------
# Data Feeding & Batch Ingestion Helpers
# ---------------------------------------------------------------------------
def feed_sales_data(new_months, new_values):
    """Feeds new monthly sales records."""
    state = load_state()
    months = list(state.get("sales_months", []))
    history = [float(x) for x in state.get("sales_history", [])]

    for m, v in zip(new_months, new_values):
        if m in months:
            idx = months.index(m)
            history[idx] = float(v)
        else:
            months.append(m)
            history.append(float(v))

    # Keep last 24 months maximum for performance
    if len(months) > 24:
        months = months[-24:]
        history = history[-24:]

    state["sales_months"] = months
    state["sales_history"] = history
    return save_state(state)


def feed_inventory_batch(items_list):
    """
    Batch inserts or updates inventory items.
    Item schema: {name, sku, category, unit_cost, selling_price, stock, daily_sales, lead_time_days}
    """
    state = load_state()
    inv_map = {item["sku"]: item for item in state.get("inventory", [])}

    for item in items_list:
        sku = str(item.get("sku", "")).strip().upper()
        if not sku:
            sku = "SKU-" + str(len(inv_map) + 1).zfill(3)

        existing = inv_map.get(sku, {})
        merged = {
            "name": str(item.get("name", existing.get("name", "Product Item"))),
            "sku": sku,
            "category": str(item.get("category", existing.get("category", "General"))),
            "unit_cost": float(item.get("unit_cost", existing.get("unit_cost", 100))),
            "selling_price": float(item.get("selling_price", existing.get("selling_price", 150))),
            "stock": max(0.0, float(item.get("stock", existing.get("stock", 0)))),
            "daily_sales": max(0.1, float(item.get("daily_sales", existing.get("daily_sales", 1.0)))),
            "lead_time_days": max(1.0, float(item.get("lead_time_days", existing.get("lead_time_days", 7))))
        }
        inv_map[sku] = merged

    state["inventory"] = list(inv_map.values())
    return save_state(state)


def feed_reviews_batch(reviews_list):
    """
    Batch inserts new customer reviews.
    Can be list of strings or list of dicts {text, source, date}.
    """
    state = load_state()
    current_reviews = state.get("reviews", [])
    now_str = datetime.now().strftime("%Y-%m-%d")

    for r in reviews_list:
        if isinstance(r, str):
            if r.strip():
                current_reviews.append({"text": r.strip(), "source": "Direct Feed", "date": now_str})
        elif isinstance(r, dict) and r.get("text"):
            current_reviews.append({
                "text": str(r.get("text")).strip(),
                "source": str(r.get("source", "Direct Feed")),
                "date": str(r.get("date", now_str))
            })

    state["reviews"] = current_reviews[-100:]  # keep recent 100
    return save_state(state)
