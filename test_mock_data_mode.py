import sys
import json
import urllib.request

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")

BASE_URL = "http://127.0.0.1:5001"

def run_tests():
    print("=== Testing Mock Data Mode & Custom Uploaded Datasets ===")
    
    # 1. Test GET /api/settings/mock-mode
    req = urllib.request.Request(f"{BASE_URL}/api/settings/mock-mode")
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print(f"✓ GET /api/settings/mock-mode: {data}")
        assert "use_mock_data" in data

    # 2. Test POST /api/settings/mock-mode (Toggle OFF)
    req = urllib.request.Request(
        f"{BASE_URL}/api/settings/mock-mode",
        data=json.dumps({"use_mock_data": False}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print(f"✓ POST /api/settings/mock-mode (OFF): {data}")
        assert data["use_mock_data"] is False

    # 3. Test POST /api/datasets/custom (Upload dataset)
    sample_rows = [
        {"Month": "Q1 2026", "Sales_Lakhs": 45.2, "Units": 1200, "Region": "South"},
        {"Month": "Q2 2026", "Sales_Lakhs": 58.6, "Units": 1450, "Region": "South"},
        {"Month": "Q3 2026", "Sales_Lakhs": 62.1, "Units": 1600, "Region": "North"}
    ]
    req = urllib.request.Request(
        f"{BASE_URL}/api/datasets/custom",
        data=json.dumps({"id": "test_ds_01", "name": "q1_q3_actuals.csv", "rows": sample_rows}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print(f"✓ POST /api/datasets/custom: Saved {data['dataset']['name']}")
        assert data["success"] is True
        assert data["dataset"]["rowsCount"] == 3

    # 4. Test GET /api/datasets/custom (List uploaded datasets)
    req = urllib.request.Request(f"{BASE_URL}/api/datasets/custom")
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print(f"✓ GET /api/datasets/custom: Found {len(data['custom_datasets'])} uploaded datasets")
        assert len(data["custom_datasets"]) >= 1

    # 5. Reset mock mode back to True for default state
    req = urllib.request.Request(
        f"{BASE_URL}/api/settings/mock-mode",
        data=json.dumps({"use_mock_data": True}).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode("utf-8"))
        print(f"✓ Reset Mock Mode back to True: {data}")

    print("\n🎉 ALL MOCK MODE & CUSTOM DATASETS TESTS PASSED!")

if __name__ == "__main__":
    run_tests()
