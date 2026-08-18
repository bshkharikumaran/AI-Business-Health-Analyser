"""
Comprehensive Test Suite for User Authentication, Business Profile Onboarding,
and Government Schemes Matcher & Comparator Hub (using unittest).
"""
import unittest
import json
from app import app
import logic
import db


class TestSchemesAndAuth(unittest.TestCase):
    def setUp(self):
        app.config["TESTING"] = True
        self.client = app.test_client()

    def test_auth_login_demo(self):
        """Test 1-click demo login and credentials authentication."""
        # Test Store Owner Login
        res = self.client.post("/api/auth/login", json={
            "email": "owner@chinnutextiles.in",
            "role": "admin",
            "name": "Chinnu"
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["user"]["role"], "admin")
        self.assertTrue(data["user"]["authenticated"])
        self.assertIn("token", data)

        # Test BI Analyst Login
        res2 = self.client.post("/api/auth/login", json={
            "email": "ananya.patel@enterprise.ai",
            "role": "analyst",
            "name": "Ananya Patel"
        })
        self.assertEqual(res2.status_code, 200)
        data2 = res2.get_json()
        self.assertEqual(data2["user"]["role"], "analyst")

    def test_business_profile_and_scheme_matching(self):
        """Test updating business profile and verifying scheme matching."""
        payload = {
            "name": "Chinnu Textiles & Handlooms",
            "owner_name": "Chinnu",
            "phone": "+91 98765 43210",
            "email": "owner@chinnutextiles.in",
            "category": "micro",
            "sector": "textiles",
            "turnover_lakhs": 68.0,
            "investment_lakhs": 18.5,
            "state": "Tamil Nadu",
            "city": "Salem",
            "udyam_registered": True,
            "gst_registered": True,
            "is_women_owned": True,
            "is_rural": True
        }

        res = self.client.post("/api/business/profile", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["profile"]["category"], "micro")
        self.assertTrue(data["profile"]["is_women_owned"])
        
        matches = data["matched_schemes"]["matches"]
        self.assertGreaterEqual(len(matches), 5)
        
        # Check that PMEGP gives 35% subsidy due to Women/Rural multiplier
        pmegp = next((m for m in matches if m["id"] == "pmegp"), None)
        self.assertIsNotNone(pmegp)
        self.assertEqual(pmegp["subsidy_pct"], 35.0)
        self.assertGreater(pmegp["estimated_subsidy_lakhs"], 0)
        self.assertGreaterEqual(pmegp["match_score_pct"], 90)

        # Check Tamil Nadu NEEDS is matched because state is Tamil Nadu
        tn_needs = next((m for m in matches if m["id"] == "tn_needs"), None)
        self.assertIsNotNone(tn_needs)
        self.assertEqual(tn_needs["subsidy_pct"], 25.0)

    def test_scheme_comparison_endpoint(self):
        """Test side-by-side comparison matrix for selected schemes."""
        res = self.client.post("/api/schemes/compare", json={
            "scheme_ids": ["pmegp", "cgtmse", "tn_needs"]
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        comp = data["comparison"]
        self.assertEqual(len(comp["selected_schemes"]), 3)
        self.assertGreaterEqual(len(comp["comparison_fields"]), 6)

    def test_subsidy_calculator_endpoint(self):
        """Test project subsidy breakdown calculation for ₹25 Lakhs project."""
        res = self.client.post("/api/schemes/calculator", json={
            "project_cost_lakhs": 25.0,
            "scheme_id": "pmegp"
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        calc = data["data"]
        self.assertEqual(calc["project_cost_lakhs"], 25.0)
        self.assertEqual(calc["subsidy_rate_pct"], 35.0)
        self.assertEqual(calc["subsidy_amount_lakhs"], 8.75)
        self.assertEqual(calc["own_contribution_lakhs"], 1.25)
        self.assertEqual(calc["bank_loan_lakhs"], 15.0)
        self.assertGreater(calc["interest_saved_annual_lakhs"], 0)

    def test_whatsapp_scheme_dispatch(self):
        """Test dispatching official scheme guide to WhatsApp."""
        res = self.client.post("/api/schemes/send-whatsapp", json={
            "scheme_id": "pmegp"
        })
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertEqual(data["log"]["event_type"], "scheme_guide")
        self.assertTrue("PMEGP" in data["log"]["title"] or "Government" in data["log"]["title"])

    def test_multilingual_voice_schemes_queries(self):
        """Test voice queries in Tamil, English, and Hindi for government schemes."""
        # Tamil Query
        res_ta = self.client.post("/api/voice/command", json={
            "transcript": "எங்கள் பிசினஸிற்கு என்ன அரசு மானியம் மற்றும் திட்டங்கள் உள்ளன?"
        })
        self.assertEqual(res_ta.status_code, 200)
        data_ta = res_ta.get_json()
        self.assertEqual(data_ta["view"], "govt-schemes")
        self.assertTrue(any(k in data_ta["spoken_text"] for k in ["அரசு", "திட்டங்கள்", "PMEGP", "மானிய"]))

        # English Query
        res_en = self.client.post("/api/voice/command", json={
            "transcript": "Which government scheme gives the highest subsidy for my business?"
        })
        self.assertEqual(res_en.status_code, 200)
        data_en = res_en.get_json()
        self.assertEqual(data_en["view"], "govt-schemes")
        self.assertTrue("PMEGP" in data_en["spoken_text"] or "subsidy" in data_en["spoken_text"].lower())

        # Hindi Query
        res_hi = self.client.post("/api/voice/command", json={
            "transcript": "Hamare vyapar ke liye sarkari subsidy aur schemes dikhao"
        })
        self.assertEqual(res_hi.status_code, 200)
        data_hi = res_hi.get_json()
        self.assertEqual(data_hi["view"], "govt-schemes")
        self.assertTrue(any(k in data_hi["spoken_text"] for k in ["सरकारी", "योजना", "सब्सिडी", "PMEGP"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
