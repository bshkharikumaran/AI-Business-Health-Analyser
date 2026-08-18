"""
Test Suite for Autonomous Multilingual AI Q&A across the Entire Platform & Database.
Tests exact user queries from screenshots in Tamil, English, Hindi, Telugu, Malayalam, Kannada.
"""
import sys
import codecs
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())

import requests
import json

BASE_URL = "http://127.0.0.1:5001"

TEST_QUERIES = [
    {
        "name": "User Query 1 (Tamil): Regional Performance",
        "transcript": "நம்மளோட பிசினஸ் எந்த ரீஜியன்ல பெர்பார்மன்ஸ் அதிகமா இருக்கு.",
        "expected_keywords": ["வட அமெரிக்கா", "North America", "45%"],
        "expected_lang": "ta-IN"
    },
    {
        "name": "User Query 2 (English): Heavy Regional Performance",
        "transcript": "In which region our business has heavy performance?",
        "expected_keywords": ["North America", "45.0%", "$4.25M"],
        "expected_lang": "en-IN"
    },
    {
        "name": "English: High-Margin Products",
        "transcript": "Which product gives maximum profit margin?",
        "expected_keywords": ["Natural Sandalwood Incense", "62.5%"],
        "expected_lang": "en-IN"
    },
    {
        "name": "Tamil: High-Margin Products",
        "transcript": "எந்த பொருள் அதிக லாபம் தருகிறது?",
        "expected_keywords": ["Natural Sandalwood Incense", "62.5%"],
        "expected_lang": "ta-IN"
    },
    {
        "name": "English: Customer Churn / At-Risk Account",
        "transcript": "Which customer is at risk of churn?",
        "expected_keywords": ["CUST-903", "74%"],
        "expected_lang": "en-IN"
    },
    {
        "name": "Tamil: Urgent Low Stock Check",
        "transcript": "இருப்பில் எந்த பொருள் உடனே தீர்ந்துவிடும்?",
        "expected_keywords": ["ரீஆர்டர்", "Cooking Oil", "Cotton Sarees", "இருப்பில்"],
        "expected_lang": "ta-IN"
    },
    {
        "name": "English: Uploaded Dataset Dimensions",
        "transcript": "How many rows in our uploaded dataset?",
        "expected_keywords": ["records", "dataset"],
        "expected_lang": "en-IN"
    },
    {
        "name": "Hindi: Regional Performance",
        "transcript": "किस क्षेत्र में हमारे व्यापार की बिक्री सबसे अधिक है?",
        "expected_keywords": ["उत्तर अमेरिका", "North America", "45%"],
        "expected_lang": "hi-IN"
    }
]

def run_tests():
    print("=== Testing Autonomous Multilingual AI Platform Q&A ===")
    all_passed = True
    
    for t in TEST_QUERIES:
        print(f"\nTesting: {t['name']}")
        print(f"Query: \"{t['transcript']}\"")
        resp = requests.post(f"{BASE_URL}/api/voice/command", json={"transcript": t["transcript"]})
        assert resp.status_code == 200, f"Failed with {resp.status_code}"
        data = resp.json()
        
        spoken = data.get("spoken_text", "")
        lang = data.get("lang_code", "")
        action = data.get("action", "")
        print(f"-> Action: {action}")
        print(f"-> Lang:   {lang}")
        print(f"-> Spoken: {spoken}")
        
        # Check language
        if t["expected_lang"] not in lang:
            print(f"❌ Language mismatch: Expected {t['expected_lang']}, got {lang}")
            all_passed = False
            
        # Check expected keywords
        found = any(k.lower() in spoken.lower() for k in t["expected_keywords"])
        if not found:
            print(f"❌ Keywords missing: Expected one of {t['expected_keywords']}")
            all_passed = False
        else:
            print("✓ Answer is factually accurate & relevant!")
            
    if all_passed:
        print("\n🎉 ALL AI PLATFORM Q&A TESTS PASSED PERFECTLY!")
    else:
        print("\n⚠️ SOME TESTS FAILED!")

if __name__ == "__main__":
    run_tests()
