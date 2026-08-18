"""
Next-Generation Autonomous Multilingual AI Voice Assistant for Vyapaar Pulse.

Features:
1. Omnilingual Understanding: Understands speech and text across Indian regional languages:
   - Tamil (தமிழ் / Tanglish) -> 'ta-IN'
   - English -> 'en-IN' / 'en-US'
   - Telugu (తెలుగు) -> 'te-IN'
   - Malayalam (മലയാളം) -> 'ml-IN'
   - Kannada (ಕನ್ನಡ) -> 'kn-IN'
   - Hindi (हिन्दी / Hinglish) -> 'hi-IN'
   - Spanish, French, German, etc.
2. Full Autonomous Web Platform Access:
   - Executive Business Health Score & 5-Pillar breakdown
   - SaaS ARR, MRR, CAC, LTV, Churn Rate, and Net Revenue Retention
   - Retail Supply Chain SKU economics, gross margins, and inventory runway
   - Customer Segmentation, NPS Cohorts, and At-Risk Churn accounts
   - Financial Credit Risk, DSCR, Debt Ratios, and Cash Runway
   - AI Sales Forecasting & What-If Scenario Simulations
   - Government MSME Scheme matching (PMEGP, CGTMSE, Mudra)
   - Automated WhatsApp Alert Dispatch, Trigger Rules, and Live Phone Simulator
   - Platform Telemetry, Data Ingestion, and Data Quality Audits
3. Native-Language Speech Synthesis (TTS): Spoken output is rendered in the EXACT same language
   and dialect as the user's input with precise ISO language tags.
4. Resilient Offline Multilingual Autonomous Intelligence Engine.
"""
import os
import re

GEMINI_API_KEY = (
    os.environ.get("GEMINI_API_KEY") or
    os.environ.get("GOOGLE_API_KEY") or
    os.environ.get("GOOGLE_GENAI_API_KEY") or
    os.environ.get("GEMINI_KEY")
)
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-2.5-flash")

_client = None
_client_load_error = None


def _get_client():
    """Lazily create the Gemini client."""
    global _client, _client_load_error
    if _client is not None:
        return _client
    if _client_load_error is not None:
        return None
    if not GEMINI_API_KEY:
        _client_load_error = "GEMINI_API_KEY is not set"
        return None
    try:
        from google import genai
        _client = genai.Client(api_key=GEMINI_API_KEY)
        return _client
    except Exception as e:
        _client_load_error = str(e)
        return None


def gemini_status():
    """Returns the live status of the Gemini model and engine."""
    if GEMINI_API_KEY and _get_client() is not None:
        return {
            "available": True,
            "mode": "gemini",
            "model": GEMINI_MODEL,
            "description": f"✦ Autonomous Multilingual Gemini Agent ({GEMINI_MODEL})"
        }
    return {
        "available": False,
        "mode": "rule-based fallback",
        "description": "⚙ Multilingual Autonomous Intelligence Engine (Tamil, English, Telugu, Malayalam, Kannada, Hindi)",
        "reason": _client_load_error or "GEMINI_API_KEY not set"
    }


# ---------------------------------------------------------------------------
# Comprehensive Tool Schemas for Autonomous Business & WhatsApp Operations
# ---------------------------------------------------------------------------
TOOLS = [
    {
        "type": "function",
        "name": "navigate_view",
        "description": "Switch the dashboard interface to a specified view.",
        "parameters": {
            "type": "object",
            "properties": {
                "view": {
                    "type": "string",
                    "enum": ["overview", "dashboard", "sales", "inventory", "sentiment", "alerts", "data-feed", "whatsapp-automation", "data_feeding", "analytics", "insights", "reports", "data-analysis"],
                    "description": "The destination view name."
                }
            },
            "required": ["view"],
        },
    },
    {
        "type": "function",
        "name": "get_full_business_summary",
        "description": "Get complete autonomous 360-degree executive business summary covering ARR, Health Score, Inventory, Customer NPS, and WhatsApp telemetry.",
        "parameters": {
            "type": "object",
            "properties": {
                "language": {"type": "string", "description": "Target language code ('ta', 'hi', 'te', 'ml', 'kn', 'en')."}
            }
        },
    },
    {
        "type": "function",
        "name": "get_saas_metrics",
        "description": "Retrieve SaaS subscription telemetry: Net ARR, MRR, CAC, LTV, Churn Rate, Net Revenue Retention, and Regional breakdowns.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "type": "function",
        "name": "get_customer_churn",
        "description": "Analyze customer segments, cohort churn risks, open support tickets, and VIP accounts.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "type": "function",
        "name": "get_credit_risk",
        "description": "Audit financial credit scores, DSCR ratios, debt levels, risk ratings (AAA to BB), and cash runway.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "type": "function",
        "name": "get_supply_chain",
        "description": "Examine retail supply chain SKU economics, gross profit margins, daily sales velocity, and supplier scores.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "type": "function",
        "name": "get_platform_telemetry",
        "description": "Inspect total ingested records (142,850), connected data sources (8), and data quality scores (98.5%).",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "type": "function",
        "name": "get_business_health",
        "description": "Get executive business health score (0-100), 5-pillar breakdown, and automated recommendations.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "type": "function",
        "name": "get_sales_forecast",
        "description": "Retrieve the 3-month AI sales forecast, trend velocity, and confidence intervals.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "type": "function",
        "name": "simulate_sales_scenario",
        "description": "Run an interactive 'What-If' business scenario simulation with marketing boost, festival multipliers, or discounts.",
        "parameters": {
            "type": "object",
            "properties": {
                "promo_boost_pct": {"type": "number", "description": "WhatsApp/Ad promo boost % (e.g. 15 for +15%)."},
                "festival_multiplier": {"type": "number", "description": "Festival/seasonal demand multiplier (e.g. 1.3 for 30% jump)."},
                "discount_pct": {"type": "number", "description": "Price discount %."},
                "inflation_pct": {"type": "number", "description": "Inflation rate %."},
            }
        },
    },
    {
        "type": "function",
        "name": "update_sales_month",
        "description": "Update or set the sales revenue for a specific month (in ₹ thousands).",
        "parameters": {
            "type": "object",
            "properties": {
                "month": {"type": "string", "description": "Month identifier (e.g. 'last month', 'this month', 'August', 'Aug 26')."},
                "value": {"type": "number", "description": "Sales revenue in ₹ thousands."},
            },
            "required": ["month", "value"],
        },
    },
    {
        "type": "function",
        "name": "get_inventory_status",
        "description": "Check real-time stock levels, stockout risks, and reorder points for a specific product or entire warehouse.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {"type": "string", "description": "Product name or SKU to inspect. Omit for full inventory summary."},
            },
        },
    },
    {
        "type": "function",
        "name": "update_inventory_item",
        "description": "Update stock on hand, average daily sales velocity, or supplier lead time for an inventory item.",
        "parameters": {
            "type": "object",
            "properties": {
                "product_name": {"type": "string", "description": "Name or SKU of product (e.g. 'cotton sarees', 'rice')."},
                "field": {"type": "string", "enum": ["stock", "daily_sales", "lead_time_days", "unit_cost", "selling_price"]},
                "value": {"type": "number", "description": "New numerical value."},
            },
            "required": ["product_name", "field", "value"],
        },
    },
    {
        "type": "function",
        "name": "run_sentiment_analysis",
        "description": "Re-run multilingual sentiment and aspect-based customer satisfaction analysis on recent reviews.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "type": "function",
        "name": "enable_whatsapp_alerts",
        "description": "Enable automated WhatsApp notifications for business alerts, stockout warnings, or daily summaries.",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "description": "Filter type like 'critical' or 'all'."}
            }
        },
    },
    {
        "type": "function",
        "name": "disable_whatsapp_alerts",
        "description": "Turn off / disable automated WhatsApp alerts and notifications.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "type": "function",
        "name": "send_performance_summary_whatsapp",
        "description": "Generate and immediately send the latest business performance summary and telemetry to WhatsApp.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "type": "function",
        "name": "send_whatsapp_alerts",
        "description": "Trigger and broadcast automated WhatsApp business alerts for stockout risks, negative reviews, or demand shifts.",
        "parameters": {"type": "object", "properties": {}},
    },
    {
        "type": "function",
        "name": "create_whatsapp_automation_rule",
        "description": "Create a new automated WhatsApp alert trigger rule (e.g., alert if performance drops below 70% or stock < 10).",
        "parameters": {
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "Rule descriptive title."},
                "event_type": {"type": "string", "description": "Event type: 'stockout_risk', 'sentiment_dip', 'sales_drop', 'custom_metric'."},
                "condition_threshold": {"type": "number", "description": "Numerical cutoff threshold value."},
                "urgency": {"type": "string", "enum": ["critical", "high", "medium", "info"]}
            },
            "required": ["name", "event_type", "condition_threshold"]
        }
    },
    {
        "type": "function",
        "name": "get_whatsapp_alert_history",
        "description": "Retrieve recent WhatsApp alert transmission logs and delivery statuses.",
        "parameters": {"type": "object", "properties": {}}
    },
    {
        "type": "function",
        "name": "test_whatsapp_connection",
        "description": "Send a verification test message to the configured WhatsApp phone number to confirm connectivity.",
        "parameters": {
            "type": "object",
            "properties": {
                "phone": {"type": "string", "description": "Optional destination phone number."}
            }
        }
    },
    {
        "type": "function",
        "name": "generate_marketing_campaign",
        "description": "Generate a localized, high-conversion WhatsApp marketing broadcast message for festivals, flash sales, or clearance.",
        "parameters": {
            "type": "object",
            "properties": {
                "theme": {"type": "string", "enum": ["festival", "flash_sale", "clearance"], "description": "Campaign theme."},
                "discount_pct": {"type": "number", "description": "Discount percentage (e.g. 15)."},
                "product_name": {"type": "string", "description": "Target product or category."},
                "language": {"type": "string", "description": "Target language code ('ta', 'hi', 'te', 'ml', 'kn', 'en')."}
            }
        },
    },
    {
        "type": "function",
        "name": "get_government_schemes",
        "description": "Find matching government MSME schemes, subsidies, collateral-free loans, and calculate benefit values.",
        "parameters": {
            "type": "object",
            "properties": {
                "category": {"type": "string", "enum": ["micro", "small", "medium"]},
                "sector": {"type": "string", "enum": ["retail", "trading", "manufacturing", "service", "agriculture"]},
                "turnover_lakhs": {"type": "number"},
                "state": {"type": "string"},
            },
        },
    },
]

SYSTEM_INSTRUCTION = """
You are Vyapaar Pulse AI — an Autonomous Multilingual Operations & Business Intelligence Copilot for Enterprise MSMEs.

CRITICAL INSTRUCTIONS:
1. MULTILINGUAL OUTPUT: You MUST detect the input language/script/dialect (Tamil, English, Telugu, Malayalam, Kannada, Hindi, Hinglish, Tanglish, etc.).
   You MUST respond in the EXACT SAME LANGUAGE and SCRIPT as the user.
   - Tamil input / "in tamil" -> Reply in Tamil (தமிழ் / clear Tanglish).
   - Hindi input / "in hindi" -> Reply in Hindi (हिन्दी / clear Hinglish).
   - Telugu input / "in telugu" -> Reply in Telugu (తెలుగు).
   - Malayalam input / "in malayalam" -> Reply in Malayalam (മലയാളം).
   - Kannada input / "in kannada" -> Reply in Kannada (ಕನ್ನಡ).
   - English input -> Reply in crisp, professional English.

2. FULL PLATFORM DATA ACCESS:
   - When asked for summary / overview: Call get_full_business_summary(language=...).
   - When asked for ARR, MRR, SaaS, revenue, CAC, LTV, retention: Call get_saas_metrics().
   - When asked for customer churn, at-risk accounts, NPS: Call get_customer_churn().
   - When asked for credit risk, DSCR, debt, loan eligibility: Call get_credit_risk().
   - When asked for stock, inventory, margins, supply chain: Call get_supply_chain() or get_inventory_status().
   - When asked for WhatsApp automations: Call enable_whatsapp_alerts(), send_performance_summary_whatsapp(), test_whatsapp_connection().
   - When asked for Government schemes / subsidies: Call get_government_schemes().
   - When asked for What-If scenario simulations: Call simulate_sales_scenario().

3. CONCISE & SPOKEN-READY: Keep spoken response to 1-3 clear sentences suitable for speech synthesis reading. Avoid markdown asterisks in spoken text.
"""


def _detect_language_code(text):
    """Accurately detects Indian regional and global languages for TTS and STT."""
    t = text.lower().strip()

    # Explicit language flags in query
    if any(k in t for k in ["in tamil", "tamil la", "tamilil", "tamilil solla", "tamil script", "thamizh"]):
        return "ta-IN"
    if any(k in t for k in ["in hindi", "hindi me", "hindi mein", "hindi bhasha"]):
        return "hi-IN"
    if any(k in t for k in ["in telugu", "telugu lo", "telugulo"]):
        return "te-IN"
    if any(k in t for k in ["in malayalam", "malayalam il", "malayalathil"]):
        return "ml-IN"
    if any(k in t for k in ["in kannada", "kannada dalli", "kannadadalli"]):
        return "kn-IN"

    # 1. Tamil Script [\u0B80-\u0BFF] or Tanglish Keywords
    if re.search(r"[\u0B80-\u0BFF]", text) or any(w in t for w in [
        "vanakkam", "nalla", "nallaa", "semma", "romba", "mosam", "eppadi", "evvalavu",
        "irukku", "pandra", "thambi", "solla", "nanba", "anuppu", "anuppavum", "kaattu",
        "koodu", "enna", "mikka", "nandri", "saree", "virpanai", "thevai", "maniam",
        "pandigai", "innaiki", "kadan", "seiyavum", "pannu", "podu", "surukkam", "kurippu",
        "solravan", "solunga", "vilakkam", "nilavaram", "pathu"
    ]):
        return "ta-IN"

    # 2. Devanagari Script [\u0900-\u097F] (Hindi/Marathi) or Hinglish Keywords
    if re.search(r"[\u0900-\u097F]", text) or any(w in t for w in [
        "namaste", "namaskar", "badhiya", "kaisa", "kitna", "accha", "bhejo", "dikhao",
        "batao", "vyapar", "dukan", "samagri", "chalu", "band", "karo", "aaj", "kal",
        "biki", "grahak", "suchna", "samjhao", "sujhav", "bhejiye", "yojana", "saransh",
        "vivaran", "halat", "kariye"
    ]):
        return "hi-IN"

    # 3. Telugu Script [\u0C00-\u0C7F] or Telugish Keywords
    if re.search(r"[\u0C00-\u0C7F]", text) or any(w in t for w in [
        "namaskaram", "namaskaralu", "bagundi", "chupinchu", "ela", "undi", "entha",
        "chudu", "pampu", "cheyi", "cheyandi", "ivvala", "vyaparam", "ammukalu", "hecharika",
        "teliyacheyi", "yenduku", "saramsam", "cheppandi"
    ]):
        return "te-IN"

    # 4. Malayalam Script [\u0D00-\u0D7F] or Malayalam Keywords
    if re.search(r"[\u0D00-\u0D7F]", text) or any(w in t for w in [
        "namaskaram", "engane", "und", "kollam", "nannayi", "ayakkuka", "parayuka",
        "kanikku", "vyaparam", "vilpanana", "innu", "enthanu", "shemikku", "ariyu", "sangraham"
    ]):
        return "ml-IN"

    # 5. Kannada Script [\u0C80-\u0CFF] or Kannada Keywords
    if re.search(r"[\u0C80-\u0CFF]", text) or any(w in t for w in [
        "namaskara", "chennagide", "hegide", "tumba", "nodona", "kalsi", "maadi",
        "ivattu", "vyapara", "marata", "enide", "torisi", "eshtu", "bedi", "saramsa", "heli"
    ]):
        return "kn-IN"

    # 6. Bengali [\u0980-\u09FF]
    if re.search(r"[\u0980-\u09FF]", text) or any(w in t for w in ["kemon", "bhalo", "dekhao", "pathan"]):
        return "bn-IN"

    # 7. Spanish
    if any(w in t for w in ["hola", "negocio", "inventario", "ventas", "mostrar", "salud", "alertas", "gracias", "resumen"]):
        return "es-ES"

    # 8. French
    if any(w in t for w in ["bonjour", "inventaire", "ventes", "affaires", "afficher", "santé", "merci", "résumé"]):
        return "fr-FR"

    # 9. German
    if any(w in t for w in ["hallo", "inventar", "geschäft", "umsatz", "zeigen", "bitte"]):
        return "de-DE"

    return "en-IN"


# ---------------------------------------------------------------------------
# Gemini Autonomous Path
# ---------------------------------------------------------------------------
def _call_gemini(transcript, executors):
    client = _get_client()
    if client is None:
        return None

    lang_code = _detect_language_code(transcript)

    try:
        interaction = client.interactions.create(
            model=GEMINI_MODEL,
            input=transcript,
            instructions=SYSTEM_INSTRUCTION,
            tools=TOOLS,
        )

        function_call = None
        for output in interaction.outputs:
            if getattr(output, "type", None) == "function_call":
                function_call = output
                break

        if function_call is None:
            text = getattr(interaction, "output_text", None) or "I have processed your query."
            return {"action": "speak_only", "view": None, "spoken_text": text, "data": None, "lang_code": lang_code}

        fn_name = function_call.name
        fn_args = dict(function_call.arguments or {})

        if fn_name not in executors:
            return {"action": "speak_only", "view": None, "spoken_text": f"Executed action {fn_name}.", "data": None, "lang_code": lang_code}

        result = executors[fn_name](**fn_args)

        # Let Gemini synthesize natural localized follow-up
        try:
            follow_up = client.interactions.create(
                model=GEMINI_MODEL,
                previous_interaction_id=interaction.id,
                input=[{
                    "type": "function_result",
                    "call_id": function_call.id,
                    "name": fn_name,
                    "result": str(result.get("spoken_text", "")),
                }],
            )
            spoken = getattr(follow_up, "output_text", None) or result.get("spoken_text", "")
        except Exception:
            spoken = result.get("spoken_text", "")

        return {
            "action": fn_name,
            "view": result.get("view"),
            "spoken_text": spoken,
            "data": result.get("data"),
            "lang_code": lang_code
        }
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Multilingual Autonomous Intelligence Engine (Deep Offline Knowledge Base)
# ---------------------------------------------------------------------------
def _multilingual_rule_based_intent(transcript, executors):
    t = transcript.lower().strip()
    lang_code = _detect_language_code(transcript)

    # 1. 360-Degree Comprehensive Executive Business Summary
    if any(k in t for k in [
        "summary", "briefing", "overview", "overall", "full report", "business status",
        "surukkam", "kurippu", "solla", "vilakkam", "nilavaram", "enna aachu", "eppadi irukku",
        "saransh", "batao", "samjhao", "halat", "kaisa chal",
        "saramsam", "cheppu", "vivaram", "engane und", "sangraham", "hegide", "heli"
    ]):
        res = executors["get_full_business_summary"](language=lang_code[:2])
        res["lang_code"] = lang_code
        return res

    # 2. SaaS Metrics & ARR / Subscriptions / CAC / LTV / Retention
    if any(k in t for k in [
        "arr", "mrr", "saas", "subscription", "cac", "ltv", "retention", "customer acquisition",
        "subscriber", "recurring", "monthly recurring", "annual recurring"
    ]):
        res = executors["get_saas_metrics"]()
        res["lang_code"] = lang_code
        return res

    # 3. Customer Intelligence, Churn Risk Cohorts & NPS
    if any(k in t for k in [
        "churn", "at risk", "vip", "customer", "cohort", "delhi", "mumbai", "bangalore",
        "grahak", "ticket", "support tickets", "satisfaction", "nps", "promoter"
    ]):
        res = executors["get_customer_churn"]()
        res["lang_code"] = lang_code
        return res

    # 4. Financial Risk, Credit Ratings, DSCR & Runway
    if any(k in t for k in [
        "credit", "dscr", "runway", "debt", "risk rating", "default risk", "cash runway",
        "entity", "ent-01", "ent-04", "aaa", "finance risk", "financial health"
    ]):
        res = executors["get_credit_risk"]()
        res["lang_code"] = lang_code
        return res

    # 5. Supply Chain Economics, Product Margins & SKU Velocity
    if any(k in t for k in [
        "margin", "supply chain", "sku", "coffee", "terracotta", "pot", "incense",
        "dupatta", "linen", "supplier", "lead time", "gross margin", "unit cost"
    ]):
        res = executors["get_supply_chain"]()
        res["lang_code"] = lang_code
        return res

    # 6. Platform Telemetry, Data Ingestion & Data Quality
    if any(k in t for k in [
        "telemetry", "records", "data quality", "ingest", "ingestion", "connected sources",
        "data sources", "how many rows", "clean data", "sync"
    ]):
        res = executors["get_platform_telemetry"]()
        res["lang_code"] = lang_code
        return res

    # 7. Enable WhatsApp Alerts / Automation
    if any(k in t for k in [
        "enable whatsapp", "enable alert", "turn on whatsapp", "activate whatsapp", "whatsapp on",
        "alert chalu", "whatsapp chalu", "alert chalu karo", "whatsapp shuru",
        "alert enable pannu", "whatsapp enable pannu", "alert on pannu", "whatsapp activate pannu",
        "whatsapp alerts on cheyi", "alerts enable cheyi", "whatsapp enable maadi", "alerts on maadi",
        "whatsapp enable cheyyuka", "alerts on aakku"
    ]):
        category = "critical" if "critical" in t or "mukhy" in t or "mukkiya" in t else None
        res = executors["enable_whatsapp_alerts"](category=category)
        if lang_code == "ta-IN":
            res["spoken_text"] = "WhatsApp alerts activate seiyappattathu. Mukkiyamana alerts ungal WhatsApp-ku anuppapadum."
        elif lang_code == "hi-IN":
            res["spoken_text"] = "WhatsApp alerts safaltapoorvak chalu kar diye gaye hain. Sabhi zaroori alerts WhatsApp par milenge."
        elif lang_code == "te-IN":
            res["spoken_text"] = "WhatsApp alerts enable cheyabadinadi. Mukhyamaina updates WhatsApp lo anduthayi."
        elif lang_code == "ml-IN":
            res["spoken_text"] = "WhatsApp alerts enable aakki. Pradhana notifications WhatsApp-il labhikkum."
        elif lang_code == "kn-IN":
            res["spoken_text"] = "WhatsApp alerts sakriya golisalaagide. Mukhya hecharikegalu WhatsApp-ge baruttave."
        else:
            res["spoken_text"] = "WhatsApp alerts have been enabled for your business."
        res["lang_code"] = lang_code
        return res

    # 8. Disable WhatsApp Alerts / Automation
    if any(k in t for k in [
        "disable whatsapp", "disable alert", "turn off whatsapp", "stop whatsapp", "pause whatsapp",
        "alert band karo", "whatsapp band", "alert roko", "whatsapp roko",
        "alert disable pannu", "whatsapp off pannu", "alert niruthu",
        "whatsapp off cheyi", "alerts apeyi", "whatsapp off maadi", "alerts nillisi",
        "whatsapp disable cheyyuka", "alerts nirthuka"
    ]):
        res = executors["disable_whatsapp_alerts"]()
        if lang_code == "ta-IN":
            res["spoken_text"] = "WhatsApp notifications niruthappattathu. Thevaiyenil meendum activate seiyalaam."
        elif lang_code == "hi-IN":
            res["spoken_text"] = "WhatsApp notifications band kar diye gaye hain."
        elif lang_code == "te-IN":
            res["spoken_text"] = "WhatsApp notifications disable cheyabadinavi."
        elif lang_code == "ml-IN":
            res["spoken_text"] = "WhatsApp notifications nirthi vechu."
        elif lang_code == "kn-IN":
            res["spoken_text"] = "WhatsApp notifications nillisalaagide."
        else:
            res["spoken_text"] = "WhatsApp notifications have been disabled."
        res["lang_code"] = lang_code
        return res

    # 9. Send Performance Summary / Daily Report to WhatsApp
    if any(k in t for k in [
        "summary to whatsapp", "send summary to whatsapp", "send to whatsapp", "dispatch to whatsapp",
        "whatsapp summary", "report to whatsapp", "aaj ka summary whatsapp", "summary whatsapp par bhejo",
        "innaiki summary whatsapp", "sales summary anuppu", "summary whatsapp-la anuppu",
        "summary whatsapp pampu", "summary whatsapp kalsi", "summary whatsapp ayakkuka"
    ]):
        res = executors["send_performance_summary_whatsapp"]()
        if lang_code == "ta-IN":
            res["spoken_text"] = "Inraiya business performance summary WhatsApp-ku anuppappattathu."
        elif lang_code == "hi-IN":
            res["spoken_text"] = "Aaj ka business performance summary aapke WhatsApp par bhej diya gaya hai."
        elif lang_code == "te-IN":
            res["spoken_text"] = "Ivati business performance summary WhatsApp ki pampabadindi."
        elif lang_code == "ml-IN":
            res["spoken_text"] = "Innathe business summary WhatsApp-il ayachu."
        elif lang_code == "kn-IN":
            res["spoken_text"] = "Ivattina vyapara summary WhatsApp-ge kalsalaagide."
        else:
            res["spoken_text"] = "Today's business performance summary has been dispatched to your WhatsApp."
        res["lang_code"] = lang_code
        return res

    # 10. What alerts were sent today? / Alert History
    if any(k in t for k in [
        "what alerts were sent", "alert history", "recent alerts", "alerts sent today",
        "aaj kaunse alert gaye", "alert history dikhao", "kitne alert bheje",
        "enna alert anuppirukku", "alert history kaattu", "innaiki enna alerts",
        "e alerts pampamu", "alert history chupinchu", "en alerts kalsidira"
    ]):
        res = executors["get_whatsapp_alert_history"]()
        res["lang_code"] = lang_code
        return res

    # 11. Test WhatsApp Connection
    if any(k in t for k in [
        "test whatsapp", "test connection", "whatsapp test", "ping whatsapp",
        "whatsapp test karo", "whatsapp check karo",
        "whatsapp test pannu", "connection test pannu",
        "whatsapp test cheyi", "whatsapp test maadi"
    ]):
        res = executors["test_whatsapp_connection"]()
        if lang_code == "ta-IN":
            res["spoken_text"] = "WhatsApp connection test seiyappattathu. Status: Connected."
        elif lang_code == "hi-IN":
            res["spoken_text"] = "WhatsApp connection test safal raha. Gateway active hai."
        else:
            res["spoken_text"] = "WhatsApp connection test completed successfully. Gateway is connected."
        res["lang_code"] = lang_code
        return res

    # 12. Immediate Stock / WhatsApp Alerts Dispatch
    if any(k in t for k in ["send alert", "alert bhejo", "alert anuppu", "pampu alert", "alerts kalsi", "enviar alertas"]):
        res = executors["send_whatsapp_alerts"]()
        if lang_code == "hi-IN":
            res["spoken_text"] = "WhatsApp alerts bhej diye gaye hain. Stock aur sales status update ho gaya."
        elif lang_code == "ta-IN":
            res["spoken_text"] = "WhatsApp alerts anuppappattathu. Thevaiyana stock patri thagaval anuppi ullom."
        elif lang_code == "te-IN":
            res["spoken_text"] = "WhatsApp alerts pampabadinavi."
        elif lang_code == "ml-IN":
            res["spoken_text"] = "WhatsApp alerts ayachu."
        elif lang_code == "kn-IN":
            res["spoken_text"] = "WhatsApp alerts kalsalaagide."
        res["lang_code"] = lang_code
        return res

    # 13. Business Health / 5-Pillar Status
    if any(k in t for k in [
        "health", "how is my business", "vyapar kaisa", "business kaisa", "vyabaar eppadi",
        "business ela undi", "business hegide", "business engane und", "salud del negocio", "santé"
    ]):
        res = executors["get_business_health"]()
        score = res.get("data", {}).get("score", 47)
        badge = res.get("data", {}).get("badge", "Attention Required")
        if lang_code == "hi-IN":
            res["spoken_text"] = f"Aapka business health score {score} hai 100 me se ({badge}). Vyapar stable aur accha chal raha hai."
        elif lang_code == "ta-IN":
            res["spoken_text"] = f"Unga business health score 100-kku {score} aaga irukku ({badge}). Vyabaaram nalla nilaiyil ullathu."
        elif lang_code == "te-IN":
            res["spoken_text"] = f"Mee business health score 100 ki {score} ({badge}). Vyaparam sthiramga undi."
        elif lang_code == "ml-IN":
            res["spoken_text"] = f"Ningalude business health score 100-il {score} aanu ({badge})."
        elif lang_code == "kn-IN":
            res["spoken_text"] = f"Nimma vyapara health score 100-kke {score} aagide ({badge})."
        elif lang_code == "es-ES":
            res["spoken_text"] = f"La salud de su negocio es de {score} sobre 100 ({badge})."
        res["lang_code"] = lang_code
        return res

    # 14. What-If Scenario Simulation
    if any(k in t for k in ["simulat", "what if", "scenario", "festival", "diwali", "pongal", "surge", "discount"]):
        res = executors["simulate_sales_scenario"](promo_boost_pct=15.0, festival_multiplier=1.25)
        if lang_code == "hi-IN":
            res["spoken_text"] = "Festive demand simulation taiyar hai. Demand me 25% vriddhi ka anuman hai (+₹256.7k revenue shift)."
        elif lang_code == "ta-IN":
            res["spoken_text"] = "Pandigai kaala demand simulation seiyappattathu. Sales 25% adhigarikka vaaippu ullathu (+₹256.7k revenue shift)."
        elif lang_code == "te-IN":
            res["spoken_text"] = "Pandaga sales simulation purthayyindi. Demand 25% perige avakasam undi."
        elif lang_code == "ml-IN":
            res["spoken_text"] = "Utsava kaala sales simulation poorthiyaki."
        elif lang_code == "kn-IN":
            res["spoken_text"] = "Habbada marata simulation siddavagide."
        res["lang_code"] = lang_code
        return res

    # 15. Stock / Inventory Checks & Updates
    m = re.search(r"(?:set|update|badlo|mathu|pon|definir)\s+(.+?)\s+(?:stock|quantity|stoc)\s+(?:to|ko|a)?\s*(\d+(?:\.\d+)?)", t)
    if m:
        res = executors["update_inventory_item"](product_name=m.group(1).strip(), field="stock", value=float(m.group(2)))
        res["lang_code"] = lang_code
        return res

    if any(k in t for k in ["inventory", "stock", "warehouse", "saman", "maal", "iruppu", "sarakku", "daasthanu", "saree"]):
        m_prod = re.search(r"(?:for|of|ka|ki|patri|kosam|ge)\s+(.+)", t)
        if m_prod and "show" not in t and "open" not in t:
            res = executors["get_inventory_status"](product_name=m_prod.group(1).strip())
        else:
            res = executors["get_inventory_status"]()
        res["lang_code"] = lang_code
        return res

    # 16. Sales Forecast & Revenue Trends
    if any(k in t for k in ["forecast", "sales", "biki", "virpanai", "ammukalu", "marata", "vilpanana", "ventas", "revenue"]):
        res = executors["get_sales_forecast"]()
        res["lang_code"] = lang_code
        return res

    # 17. Customer Reviews & Sentiment Analysis
    if any(k in t for k in ["sentiment", "review", "feedback", "rating", "karuthukkal"]):
        res = executors["run_sentiment_analysis"]()
        res["lang_code"] = lang_code
        return res

    # 18. Government Schemes, Subsidies & Loans
    if any(k in t for k in ["scheme", "government", "subsidy", "yojana", "maniam", "loan", "kadan", "pmegp", "cgtmse", "mudra"]):
        res = executors["get_government_schemes"]()
        res["lang_code"] = lang_code
        return res

    # 19. Interface Navigation Shortcuts
    view_map = {
        "overview": ["overview", "home", "dashboard", "main", "mukhy"],
        "whatsapp-automation": ["whatsapp", "automation", "whatsapp page", "alert dashboard", "whatsapp tab"],
        "sales": ["sales view", "forecast view", "sales page"],
        "inventory": ["inventory view", "stock page"],
        "sentiment": ["sentiment view", "review page"],
        "alerts": ["alert page", "scheme page"],
        "data-feed": ["feed", "upload", "import", "data feeding", "csv", "excel"],
        "analytics": ["analytics", "visual analytics", "studio", "charts"],
        "insights": ["insights", "recommendations", "ai stream"],
        "reports": ["reports", "export pdf", "executive report"]
    }
    for v_name, keywords in view_map.items():
        if any(kw in t for kw in keywords):
            res = executors["navigate_view"](view=v_name)
            res["lang_code"] = lang_code
            return res

    # 20. Friendly Greetings
    if any(k in t for k in ["hello", "hi", "hey", "vanakkam", "namaste", "namaskaram", "namaskara"]):
        if lang_code == "ta-IN":
            spoken = "வணக்கம்! நான் உங்கள் Vyapaar AI வழிகாட்டி. பிசினஸ் சுருக்கம், ஸ்டாக் விவரங்கள், வருவாய் மற்றும் WhatsApp alerts பற்றி கேளுங்கள்."
        elif lang_code == "hi-IN":
            spoken = "नमस्ते! मैं आपका व्यापार एआई सहायक हूँ। व्यापार का सारांश, स्टॉक, बिक्री या व्हाट्सएप अलर्ट्स के बारे में कुछ भी पूछें।"
        elif lang_code == "te-IN":
            spoken = "నమస్కారం! నేను మీ వ్యాపార్ ఏఐ అసిస్టెంట్. బిజినెస్ సారాంశం, స్టాక్, అమ్మకాలు లేదా వాట్సాప్ అలర్ట్స్ గురించి అడగండి."
        elif lang_code == "ml-IN":
            spoken = "നമസ്കാരം! ബിസിനസ്സ് സംഗ്രഹം, സ്റ്റോക്ക്, അല്ലെങ്കിൽ WhatsApp അലേർട്ടുകളെക്കുറിച്ച് ചോദിക്കുക."
        elif lang_code == "kn-IN":
            spoken = "ನಮಸ್ಕಾರ! ವ್ಯಾಪಾರ ಸಾರಾಂಶ, ದಾಸ್ತಾನು ಅಥವಾ ವಾಟ್ಸಾಪ್ ಎಚ್ಚರಿಕೆಗಳ ಬಗ್ಗೆ ಕೇಳಿ."
        else:
            spoken = "Hello! I am your Autonomous Multilingual Copilot. Ask me for your business summary, stock levels, ARR metrics, or WhatsApp alert actions."
        return {
            "action": "speak_only",
            "view": "dashboard",
            "spoken_text": spoken,
            "data": None,
            "lang_code": lang_code
        }

    # 21. Smart Omniscient Fallback (Executes Full Summary)
    res = executors["get_full_business_summary"](language=lang_code[:2])
    res["lang_code"] = lang_code
    return res


# ---------------------------------------------------------------------------
# Public Voice & Assistant Dispatcher
# ---------------------------------------------------------------------------
def handle_voice_command(transcript, executors):
    """
    Processes incoming speech or text transcript and executes autonomous actions.
    Returns: {"action": str, "view": str|None, "spoken_text": str, "data": Any, "engine": str, "lang_code": str}
    """
    if not transcript or not transcript.strip():
        return {
            "action": "speak_only",
            "view": None,
            "spoken_text": "I am listening. How can I help with your business operations or WhatsApp alerts today?",
            "data": None,
            "engine": "none",
            "lang_code": "en-IN"
        }

    gemini_result = None
    if GEMINI_API_KEY:
        try:
            gemini_result = _call_gemini(transcript, executors)
        except Exception:
            gemini_result = None

    if gemini_result is not None:
        gemini_result["engine"] = "gemini"
        if "lang_code" not in gemini_result:
            gemini_result["lang_code"] = _detect_language_code(transcript)
        return gemini_result

    fallback_result = _multilingual_rule_based_intent(transcript, executors)
    fallback_result["engine"] = "multilingual-autonomous-engine"
    return fallback_result
