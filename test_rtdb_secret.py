import json
import urllib.request
import urllib.parse

SECRET = "H4XegOo6AxBtoq21kSbdwFGhTTiB0GVNVFBi35G3"

# Test candidate URLs
urls_to_test = [
    "https://vyapaar-pulse-ai-default-rtdb.firebaseio.com",
    "https://vyapaar-pulse-ai-default-rtdb.asia-southeast1.firebasedatabase.app",
    "https://vyapaar-pulse-ai.firebaseio.com"
]

def test_firebase_rtdb():
    payload = {"test": "Vyapaar Pulse Connected", "status": "active"}
    data_bytes = json.dumps(payload).encode("utf-8")
    
    for base_url in urls_to_test:
        url = f"{base_url}/test_connection.json?auth={SECRET}"
        print(f"Testing: {url}")
        try:
            req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"}, method="PUT")
            with urllib.request.urlopen(req, timeout=5) as response:
                res_body = response.read().decode("utf-8")
                print(f"SUCCESS with {base_url}!")
                print(f"Response: {res_body}")
                return base_url
        except Exception as e:
            print(f"Failed on {base_url}: {e}")
            
    return None

if __name__ == "__main__":
    test_firebase_rtdb()
